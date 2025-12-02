import sys
import os
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Add backend to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the heavy dependencies BEFORE importing app
# This prevents the app from trying to load the model on import
sys.modules["llama_cpp"] = MagicMock()
sys.modules["optimum.onnxruntime"] = MagicMock()
sys.modules["transformers"] = MagicMock()
sys.modules["langchain_community.embeddings"] = MagicMock()
sys.modules["langchain_community.vectorstores"] = MagicMock()

# Now we can import the app
from backend.app import app, sys_comps  # noqa: E402

client = TestClient(app)


def test_chat_endpoint_structure():
    """
    Test the /chat endpoint.
    We mock the LLM inference so we don't need the actual model file.
    """
    # Mock the LLM component in sys_comps
    mock_llm = MagicMock()
    mock_llm.return_value = {
        "choices": [{"text": "This is a mocked response from Dr. Flora."}]
    }

    # Inject the mock
    sys_comps["llm"] = mock_llm

    payload = {
        "question": "How do I treat this?",
        "context": "Apple Scab is a fungal disease.",
        "diagnosis": "Apple Scab",
    }

    response = client.post("/chat", json=payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "This is a mocked response from Dr. Flora."
