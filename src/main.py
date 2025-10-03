from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger

from core.http_utils import build_http_client
from src.api import register_routes
from src.config import AppSettings, get_settings
from src.config.cfg_logging import setup_logging
from src.custom.exceptions import AppExceptionError
from src.deps import HttpClientDep

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


# exceptions
@app.exception_handler(AppExceptionError)
async def app_exception_handler(request: Request, exc: AppExceptionError):  # noqa: RUF029
    """Dynamic response handler for AppExceptionError.

    - Default: JSON
    - Plain text: if header X-Response-Format=text or query param format=text
    """
    log_context = {
        "path": str(request.url.path),
        "method": request.method,
        "client": request.client.host if request.client else None,
        "status_code": exc.status_code,
        "context": exc.context,
        "cause": str(exc.__cause__) if exc.__cause__ else None,
    }
    logger.bind(**log_context).error(exc.message)
    response_format = request.headers.get(
        "X-Response-Format"
    ) or request.query_params.get("format", "json")

    if response_format.lower() == "text":
        text = f"[{exc.__class__.__name__}] {exc.message}"
        if exc.context:
            text += f" | context={exc.context}"
        if exc.__cause__:
            text += f" | cause={exc.__cause__}"
        return PlainTextResponse(text, status_code=exc.status_code)

    return JSONResponse(content=exc.to_dict(), status_code=exc.status_code)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# testing async client
@app.get("/test-client")
async def test_client(
    client: HttpClientDep,
):
    response = await client.get("https://httpbin.org/get")
    response.raise_for_status()
    return response.json()


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
