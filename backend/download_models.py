import boto3
import zipfile
import os

BUCKET_NAME = "mlopsmodel"
ZIP_NAME = "flora_deployment_package.zip"


def setup_models():
    print(f"🚀 Connecting to S3 Bucket: {BUCKET_NAME}...")
    s3 = boto3.client("s3")

    if os.path.exists("flora_cv_model") and os.path.exists("flora_rag_db"):
        print("✅ Models already present.")
        return

    try:
        print("⬇️ Downloading models (this takes time)...")
        s3.download_file(BUCKET_NAME, ZIP_NAME, ZIP_NAME)
        print("✅ Downloaded. Unzipping...")

        with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
            zip_ref.extractall(".")

        os.remove(ZIP_NAME)
        print("🎉 Models ready!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️ Make sure you run 'aws configure' on the server!")


if __name__ == "__main__":
    setup_models()
