from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
ALLOWED_API_KEYS = {os.getenv("API_KEY", "default-api-key")}


def verify_api_key(request: Request) -> str:
    """
    Dependency to verify the API key from the request headers.
    Args:
        request (Request): The incoming HTTP request.
    Returns:
        str: The validated API key.
    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    key: str = request.headers.get("x-api-key", "")
    if key not in ALLOWED_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return key
