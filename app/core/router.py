from app.models import openai_client, anthropic_client, local_model
from app.services.prompt_utils import clean_prompt

from app.schemas.prompt import PromptRequest


async def route_to_model(prompt_data: PromptRequest) -> str:
    """
    Routes the prompt to the appropriate model based on its content.
    Args:
        prompt_data (PromptRequest): The incoming prompt request.
    Returns:
        str: The model's response.
    """
    prompt: str = clean_prompt(prompt_data.prompt)

    if "summarize" in prompt:
        return openai_client.call_openai(prompt, model="gpt-4")
    elif "legal" in prompt:
        return anthropic_client.call_claude(prompt)
    else:
        return local_model.run_model(prompt)
