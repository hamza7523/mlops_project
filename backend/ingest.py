# this is a pipeline for importing documents eg text and pdf
# In this script, I built a modular pipeline to prepare and index plant-disease
# knowledge using a hybrid retrieval approach. I load raw JSON data, convert it
# into structured documents, and split them into meaningful chunks for embedding.
# I then generate a fresh Chroma vector database and combine it with BM25 to
# create a hybrid retriever, verifying the full search pipeline with a test query.


# type: ignore
# flake8: noqa
# ruff: noqa
# pylint: skip-file

import os
import sys

import os
import sys
import json
import shutil
import time
from typing import List

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

DATA_PATH = "data/dataset_json"
DB_OUTPUT_PATH = "flora_rag_db"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass


def load_documents(source_path: str) -> List[Document]:
    """
    Step 1: Load raw JSON data and extract metadata for Hybrid Search.
    """
    documents = []

    if not os.path.exists(source_path):
        print(f" Error: Data path '{source_path}' not found.")
        return []

    files = [f for f in os.listdir(source_path) if f.endswith(".json")]
    print(f"Found {len(files)} JSON files in '{source_path}'...")

    for filename in files:
        file_path = os.path.join(source_path, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                entries = data if isinstance(data, list) else [data]

                for entry in entries:
                    text_content = (
                        f"Disease: {entry.get('model_class', 'Unknown')}\n"
                        f"Content: {entry.get('content', '')}"
                    )

                    meta = {
                        "source": filename,
                        "source_url": entry.get("source_url", "local"),
                        "disease": entry.get("model_class", "unknown"),
                        "is_healthy": str(entry.get("is_healthy", False)),
                    }

                    doc = Document(page_content=text_content, metadata=meta)
                    documents.append(doc)

        except Exception as e:
            print(f"⚠️ Warning: Failed to process {filename}: {e}")

    print(f" Loaded {len(documents)} raw documents.")
    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Step 2: Split text into chunks.
    """
    print(f"✂️ Splitting documents (Chunk Size: {CHUNK_SIZE})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"   -> Generated {len(chunks)} text chunks.")
    return chunks


def build_vector_store(chunks: List[Document], output_path: str):
    """
    Step 3: Embed chunks and save to ChromaDB.
    """
    print(f"🧠 Initializing Embedding Model ({EMBED_MODEL_NAME})...")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)

    if os.path.exists(output_path):
        print(f"   Removing old database at {output_path}...")
        shutil.rmtree(output_path)

    print(f"💾 Creating persistent ChromaDB at '{output_path}'...")
    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embedding_model, persist_directory=output_path
    )
    vectordb.persist()
    print("Vector Database successfully built.")
    return vectordb


def verify_pipeline(vectordb, chunks):
    """
    Step 4: Verify Hybrid Search capability (Sanity Check).
    """
    print("\nVerifying Hybrid Retrieval Pipeline...")

    try:
        bm25_retriever = BM25Retriever.from_documents(chunks)
        bm25_retriever.k = 3

        chroma_retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, chroma_retriever], weights=[0.4, 0.6]
        )

        query = "tomato bacterial spot treatment"
        start = time.time()
        docs = ensemble_retriever.invoke(query)
        latency = time.time() - start

        if docs:
            print(f"    Hybrid Search Test Passed (Latency: {latency:.4f}s)")
            print(f"   Top Result: {docs[0].page_content[:100]}...")
        else:
            print("    Warning: Retriever returned no results.")

    except Exception as e:
        print(f"    Hybrid Verification Failed: {e}")


if __name__ == "__main__":

    raw_docs = load_documents(DATA_PATH)

    if raw_docs:
        doc_chunks = split_documents(raw_docs)
        vdb = build_vector_store(doc_chunks, DB_OUTPUT_PATH)
        verify_pipeline(vdb, doc_chunks)
    else:
        print("Pipeline aborted: No documents found.")
