# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for building llama-cpp-python and other tools
# build-essential: for gcc/g++ compilers
# cmake: for building llama.cpp
# curl: for healthchecks or downloading tools
# libgl1, libglib2.0-0: required for opencv/image processing libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# 1. Install CPU-only PyTorch (saves ~2GB)
# 2. Install the rest of the requirements
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy the models directory into the container
// COPY models /app/models
# (keep your existing lines up to copying code)
WORKDIR /app

# copy app code and helper script
COPY download_models.py /app/download_models.py
COPY . /app

# Ensure /app/models exists (will be mounted at runtime by ACI)
RUN mkdir -p /app/models

# Use a tiny shell script as entrypoint: download only if empty, then start uvicorn
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]


# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable for Model Directory
# This matches where we will mount the volume
ENV MODEL_DIR=/app/models

# Command to run the application
# host 0.0.0.0 is crucial for Docker networking
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
