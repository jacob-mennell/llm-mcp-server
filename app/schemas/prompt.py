from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str
    model: str = "gpt-4"
    temperature: float = 0.7

class PromptResponse(BaseModel):
    response: str
