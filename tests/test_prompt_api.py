import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_prompt():
    api_key = os.getenv("OPENAI_API_KEY", "default-openai-api-key")
    response = client.post(
        "/v1/llm",
        headers={"x-api-key": api_key},
        json={"prompt": "Say hello!", "model": "gpt-4"},
    )
    assert response.status_code == 200
    assert "hello" in response.json()["response"].lower()
