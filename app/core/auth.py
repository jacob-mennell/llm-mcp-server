from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()
ALLOWED_API_KEYS = {os.getenv("API_KEY", "default-api-key")}
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Dependency to verify the API key from the x-api-key header using FastAPI's Security.
    Args:
        api_key (str): The API key from the header.
    Returns:
        str: The validated API key.
    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    if not api_key or api_key not in ALLOWED_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
