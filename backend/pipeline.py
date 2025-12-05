# In this pipeline, I set up and trained a Swin-Tiny image classification model
# to identify plant diseases using the PlantVillage dataset. I also configured
# MLflow tracking to log each stage of the experiment. After training, I built
# a hybrid RAG system by ingesting JSON knowledge files and combining BM25 with
# dense embeddings, creating a retrieval setup that supports disease-specific answers.


# type: ignore
# flake8: noqa
# ruff: noqa
# pylint: skip-file

import os
import sys

__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os

os.environ["WANDB_DISABLED"] = "true"

import mlflow

os.environ["MLFLOW_TRACKING_URI"] = "file:///kaggle/working/mlruns"
os.environ["MLFLOW_EXPERIMENT_NAME"] = "Flora_Care_Production_Pipeline"

import zipfile
import json
import torch
import gc
import shutil
import time
import numpy as np
from PIL import Image
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
)
from torchvision.transforms import (
    Compose,
    Normalize,
    RandomResizedCrop,
    RandomHorizontalFlip,
    RandomRotation,
    ColorJitter,
    ToTensor,
    Resize,
    CenterCrop,
)

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

CV_MODEL_CHECKPOINT = "microsoft/swin-tiny-patch4-window7-224"
DATASET_PATH = "PlantVillage/train"
JSON_FOLDER_PATH = "ragdatazip/dataset_json"


USE_FULL_DATA = True
BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 2e-5

print("⚙️ System check...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"   Device: {device}")


def train_cv_model():
    print("\n--- STEP 1: CV TRAINING ---")

    all_images, all_labels = [], []
    if not os.path.exists(DATASET_PATH):
        print("Error: Dataset not found.")
        return

    classes = sorted(os.listdir(DATASET_PATH))
    for label in classes:
        label_folder = os.path.join(DATASET_PATH, label)
        if os.path.isdir(label_folder):
            for img in os.listdir(label_folder):
                all_images.append(os.path.join(label_folder, img))
                all_labels.append(label)

    test_size = 0.01 if USE_FULL_DATA else 0.80
    train_imgs, val_imgs, train_lbls, val_lbls = train_test_split(
        all_images,
        all_labels,
        test_size=test_size,
        stratify=all_labels,
        random_state=42,
    )

    train_ds = Dataset.from_dict({"image": train_imgs, "label": train_lbls})
    val_ds = Dataset.from_dict({"image": val_imgs, "label": val_lbls})

    label2id = {c: i for i, c in enumerate(classes)}
    id2label = {i: c for c, i in label2id.items()}

    image_processor = AutoImageProcessor.from_pretrained(CV_MODEL_CHECKPOINT)
    normalize = Normalize(
        mean=image_processor.image_mean, std=image_processor.image_std
    )
    size = (224, 224)

    _train_transforms = Compose(
        [
            RandomResizedCrop(size),
            RandomHorizontalFlip(),
            RandomRotation(15),
            ColorJitter(brightness=0.1, contrast=0.1),
            ToTensor(),
            normalize,
        ]
    )
    _val_transforms = Compose([Resize(size), CenterCrop(size), ToTensor(), normalize])

    def transform_train(example):
        example["pixel_values"] = [
            _train_transforms(Image.open(x).convert("RGB")) for x in example["image"]
        ]
        example["label"] = [label2id[y] for y in example["label"]]
        return example

    def transform_val(example):
        example["pixel_values"] = [
            _val_transforms(Image.open(x).convert("RGB")) for x in example["image"]
        ]
        example["label"] = [label2id[y] for y in example["label"]]
        return example

    train_ds.set_transform(transform_train)
    val_ds.set_transform(transform_val)

    print("   Starting Trainer...")
    model = AutoModelForImageClassification.from_pretrained(
        CV_MODEL_CHECKPOINT,
        num_labels=len(classes),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    args = TrainingArguments(
        output_dir="swin_cv_model",
        remove_unused_columns=False,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        num_train_epochs=NUM_EPOCHS,
        warmup_ratio=0.1,
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        save_total_limit=2,
        fp16=torch.cuda.is_available(),
        report_to=["mlflow"],
        dataloader_num_workers=2,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )

    trainer.train()

    model.save_pretrained("flora_cv_model")
    image_processor.save_pretrained("flora_cv_model")

    with mlflow.start_run(run_name="CV_Model_Architecture"):
        mlflow.log_param("backbone", CV_MODEL_CHECKPOINT)
        mlflow.log_param("num_classes", len(classes))

    del model, trainer
    torch.cuda.empty_cache()
    gc.collect()
    print("✅ CV Model Trained.")


def build_rag_db():
    print("\n📚 --- STEP 2: HYBRID RAG INGESTION ---")

    with mlflow.start_run(run_name="RAG_Ingestion_Setup"):
        documents = []
        CHUNK_SIZE = 800
        HYBRID_WEIGHTS = [0.4, 0.6]

        mlflow.log_param("chunk_size", CHUNK_SIZE)
        mlflow.log_param("retriever_type", "Hybrid_BM25_Chroma")
        mlflow.log_param("hybrid_weights", str(HYBRID_WEIGHTS))

        if os.path.exists(JSON_FOLDER_PATH):
            files = [f for f in os.listdir(JSON_FOLDER_PATH) if f.endswith(".json")]
            for filename in files:
                try:
                    with open(os.path.join(JSON_FOLDER_PATH, filename), "r") as f:
                        data = json.load(f)
                        entries = data if isinstance(data, list) else [data]

                        for entry in entries:

                            content = f"Disease: {entry.get('model_class', 'Unknown')}\nContent: {entry.get('content', '')}"

                            meta = {
                                "source": entry.get("source_url", filename),
                                "disease": entry.get("model_class", "unknown"),
                                "is_healthy": str(entry.get("is_healthy", False)),
                            }
                            documents.append(
                                Document(page_content=content, metadata=meta)
                            )
                except:
                    pass

        if not documents:
            print("❌ No docs found.")
            return

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=100
        )
        docs = splitter.split_documents(documents)
        mlflow.log_metric("total_chunks", len(docs))

        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        if os.path.exists("flora_rag_db"):
            shutil.rmtree("flora_rag_db")
        vectordb = Chroma.from_documents(
            docs, embedding_model, persist_directory="flora_rag_db"
        )
        vectordb.persist()

        print("   Verifying Hybrid Retriever & Logging Latency...")

        bm25_retriever = BM25Retriever.from_documents(docs)
        bm25_retriever.k = 3
        chroma_retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, chroma_retriever], weights=HYBRID_WEIGHTS
        )

        test_query = "tomato bacterial spot treatment"
        start_time = time.time()
        results = ensemble_retriever.invoke(test_query)
        latency = time.time() - start_time

        mlflow.log_metric("test_query_latency_seconds", latency)

        if results:
            mlflow.log_text(results[0].page_content, "sample_retrieval_output.txt")
            print(f"   Latency: {latency:.4f}s")
            print(f"  sample Logged: {results[0].page_content[:100]}...")
        else:
            print("   Warning: Retriever returned no results.")

        print("RAG DB Built & Hybrid Retriever Verified.")


if __name__ == "__main__":
    train_cv_model()
    build_rag_db()
    export_everything()
