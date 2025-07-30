from fastapi import APIRouter, Depends, Request
from app.core.auth import verify_api_key
from app.schemas.prompt import PromptRequest, PromptResponse
from app.core.router import route_to_model

router = APIRouter()

@router.post("/llm", response_model=PromptResponse)
async def handle_prompt(
    request_data: PromptRequest,
    request: Request,
    api_key: str = Depends(verify_api_key),
):
    result = await route_to_model(request_data)
    return PromptResponse(response=result)
