import os
from optimum.onnxruntime import ORTModelForImageClassification
from transformers import AutoImageProcessor
from dotenv import load_dotenv

load_dotenv()

MODEL_DIR = os.getenv("MODEL_DIR", ".")
CV_DIR = os.path.join(MODEL_DIR, "flora_cv_model")
ONNX_DIR = os.path.join(MODEL_DIR, "flora_cv_onnx")

print(f"Exporting model from {CV_DIR} to {ONNX_DIR}...")

# Load the model and export it to ONNX
model = ORTModelForImageClassification.from_pretrained(CV_DIR, export=True)
processor = AutoImageProcessor.from_pretrained(CV_DIR)

# Save the ONNX model and processor
model.save_pretrained(ONNX_DIR)
processor.save_pretrained(ONNX_DIR)

print("Export complete! ONNX model saved.")
