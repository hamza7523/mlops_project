import boto3
import zipfile
import os
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download

load_dotenv()

BUCKET_NAME = "mlopsmodel"
ZIP_NAME = "flora_deployment_package.zip"
MODEL_DIR = os.getenv("MODEL_DIR", ".")
GGUF_REPO = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
GGUF_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"


def setup_models():
    print(f"🚀 Connecting to S3 Bucket: {BUCKET_NAME}...")
    s3 = boto3.client("s3")

    cv_path = os.path.join(MODEL_DIR, "flora_cv_model")
    rag_path = os.path.join(MODEL_DIR, "flora_rag_db")
    gguf_path = os.path.join(MODEL_DIR, GGUF_FILE)

    # 1. Download CV & RAG Models from S3
    if os.path.exists(cv_path) and os.path.exists(rag_path):
        print(f"✅ CV & RAG Models already present in {MODEL_DIR}.")
    else:
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)

        zip_path = os.path.join(MODEL_DIR, ZIP_NAME)

        try:
            print(f"⬇️ Downloading models to {MODEL_DIR} (this takes time)...")
            s3.download_file(BUCKET_NAME, ZIP_NAME, zip_path)
            print("✅ Downloaded. Unzipping...")

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(MODEL_DIR)

            os.remove(zip_path)
            print("🎉 CV & RAG Models ready!")

        except Exception as e:
            print(f"❌ Error downloading from S3: {e}")
            print("⚠️ Make sure you run 'aws configure' on the server!")

    # 2. Download GGUF LLM from Hugging Face
    if os.path.exists(gguf_path):
        print(f"✅ GGUF Model already present: {gguf_path}")
    else:
        print(f"⬇️ Downloading GGUF Model ({GGUF_FILE})...")
        try:
            hf_hub_download(
                repo_id=GGUF_REPO,
                filename=GGUF_FILE,
                local_dir=MODEL_DIR,
                local_dir_use_symlinks=False,
            )
            print("🎉 GGUF Model ready!")
        except Exception as e:
            print(f"❌ Error downloading GGUF: {e}")


if __name__ == "__main__":
    setup_models()
