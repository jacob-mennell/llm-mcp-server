import openai
from app.core.config import OPENAI_API_KEY


def call_openai(prompt: str, model: str = "gpt-4", temperature: float = 0.7) -> str:
    """
    Calls the OpenAI API with the given prompt and parameters using the new openai>=1.0.0 interface.
    Falls back to a local response when no real API key is configured or the request fails.
    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model name to use.
        temperature (float): The sampling temperature.
    Returns:
        str: The generated response from the model.
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY == "default-openai-api-key":
        return f"OpenAI API key not configured; using local fallback for: {prompt}"

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        content = response.choices[0].message.content
        if content:
            return content
    except Exception:
        pass

    return f"OpenAI request failed; using local fallback for: {prompt}"
