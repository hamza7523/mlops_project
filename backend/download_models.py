import boto3
import zipfile
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = "mlopsmodel"
ZIP_NAME = "flora_deployment_package.zip"
MODEL_DIR = os.getenv("MODEL_DIR", ".")


def setup_models():
    print(f"🚀 Connecting to S3 Bucket: {BUCKET_NAME}...")
    s3 = boto3.client("s3")

    cv_path = os.path.join(MODEL_DIR, "flora_cv_model")
    rag_path = os.path.join(MODEL_DIR, "flora_rag_db")

    if os.path.exists(cv_path) and os.path.exists(rag_path):
        print(f"✅ Models already present in {MODEL_DIR}.")
        return

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
        print("🎉 Models ready!")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️ Make sure you run 'aws configure' on the server!")


if __name__ == "__main__":
    setup_models()
