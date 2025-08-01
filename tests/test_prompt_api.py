import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_prompt():
    api_key = os.getenv("API_KEY", "default-api-key")
    response = client.post(
        "/v1/llm",
        headers={"x-api-key": api_key},
        json={"prompt": "Say hello!", "model": "gpt-4"},
    )
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert "hello" in response.json()["response"].lower()


def test_summarize_prompt():
    api_key = os.getenv("API_KEY", "default-api-key")
    summarize_text = (
        "summarize: The quick brown fox jumps over the lazy dog. "
        "This sentence contains every letter of the alphabet and is often used as a typing exercise."
    )
    response = client.post(
        "/v1/llm",
        headers={"x-api-key": api_key},
        json={"prompt": summarize_text},
    )
    print("Summarize Response JSON:", response.json())
    assert response.status_code == 200
    assert (
        "fox" in response.json()["response"].lower()
        or "alphabet" in response.json()["response"].lower()
    )
