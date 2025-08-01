import openai
from app.core.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def call_openai(prompt: str, model: str = "gpt-4", temperature: float = 0.7) -> str:
    """
    Calls the OpenAI API with the given prompt and parameters.
    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model name to use.
        temperature (float): The sampling temperature.
    Returns:
        str: The generated response from the model.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]
