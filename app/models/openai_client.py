import openai
from app.core.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def call_openai(prompt, model="gpt-4", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]
