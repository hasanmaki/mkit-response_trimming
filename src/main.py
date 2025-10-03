import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from loguru import logger

from core.http_utils import build_http_client
from src.api import register_routes
from src.config import AppSettings, get_settings
from src.config.cfg_logging import setup_logging
from src.custom.exceptions import (
    AppExceptionError,
    HTTPGenricError,
    global_exception_handler,
)
from src.custom.middlewares import LoggingMiddleware
from src.deps import HttpClientDep

logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.INFO)
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler to setup and teardown resources."""
    settings: AppSettings = get_settings(toml_file_path="config.toml")
    app.state.settings = settings
    app.state.http_client = build_http_client(settings)
    yield
    await app.state.http_client.aclose()
    logger.info("Stopping application...")


app = FastAPI(lifespan=lifespan)


# middlewares
app.add_middleware(LoggingMiddleware)


# exceptions
app.add_exception_handler(AppExceptionError, global_exception_handler)  # type: ignore


@app.get("/")
async def root():
    return {"message": "Hello World"}


# testing async client
@app.get("/test-client")
async def test_client(
    client: HttpClientDep,
):
    try:
        response = await client.get("http://10.0.0.3:10003")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPGenricError(cause=e)


@app.get("/test-request")
async def test_request(request: Request):
    return {
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "client": request.client.host if request.client else "unknown",
        "client_port": request.client.port if request.client else "unknown",
        "method": request.method,
        "url": str(request.url),
    }


register_routes(app)

if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
