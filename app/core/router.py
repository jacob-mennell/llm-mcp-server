from app.models import openai_client, anthropic_client, local_model
from app.services.prompt_utils import clean_prompt

async def route_to_model(prompt_data):
    prompt = clean_prompt(prompt_data.prompt)

    if "summarize" in prompt:
        return openai_client.call_openai(prompt, model="gpt-3.5-turbo")
    elif "legal" in prompt:
        return anthropic_client.call_claude(prompt)
    else:
        return local_model.run_model(prompt)
