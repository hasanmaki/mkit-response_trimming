from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from deps import HttpClientDep
from src.api import register_routes
from src.config import AppSettings, get_settings
from src.config.cfg_logging import setup_logging
from src.core.http_manager import build_http_client

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


register_routes(app)

if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
