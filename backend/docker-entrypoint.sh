#!/usr/bin/env bash
set -e

# If the models folder is empty, run the download script (download_models.py)
if [ -z "$(ls -A /app/models 2>/dev/null)" ]; then
  echo "Models directory empty — downloading models..."
  python /app/download_models.py
else
  echo "Models already present in /app/models"
fi

# Start your app (adjust command to your app's start command)
exec uvicorn main:app --host 0.0.0.0 --port 8000
