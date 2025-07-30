from fastapi import FastAPI
from app.api.v1 import router as api_v1_router

app = FastAPI(title="LLM MCP Server")
app.include_router(api_v1_router, prefix="/v1")
