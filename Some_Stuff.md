Write package in requirements-dev.in, then run the following command to generate the requirements-dev.txt file

pip-compile requirements-dev.in -o requirements-dev.txt


Activating the virtual environment
source .venv/Scripts/activate

Uvicorn server start, run this from root directory, after venv
uvicorn src.app.main:app --reload
