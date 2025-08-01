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
) -> PromptResponse:
    """
    Handles the /llm endpoint for processing LLM prompts.
    Args:
        request_data (PromptRequest): The prompt request payload.
        request (Request): The incoming HTTP request.
        api_key (str): The validated API key from dependency.
    Returns:
        PromptResponse: The response containing the model's output.
    """
    result: str = await route_to_model(request_data)
    return PromptResponse(response=result)
