from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
ALLOWED_API_KEYS = {os.getenv("OPENAI_API_KEY", "default-openai-api-key")}


def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key not in ALLOWED_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return key
