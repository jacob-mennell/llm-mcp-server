from fastapi import FastAPI, Request, Response
from app.api.v1 import router as api_v1_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("server.log"), logging.StreamHandler()],
)

app: FastAPI = FastAPI(title="LLM MCP Server")


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    """
    Middleware to log every HTTP request and response status.
    Logs the HTTP method and URL before processing, and the response status after.
    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next handler in the middleware chain.
    Returns:
        Response: The HTTP response from the next handler.
    """
    logging.info(f"Request: {request.method} {request.url}")
    response: Response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response


def include_v1_router(app: FastAPI) -> None:
    """
    Includes the v1 API router with the /v1 prefix into the FastAPI app.
    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(api_v1_router, prefix="/v1")


include_v1_router(app)
