from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.config.cfg_logging import setup_logging
from src.config.settings import AppSettings, get_settings
from src.utils.client_utils import build_async_client

setup_logging()
settings: AppSettings = get_settings(toml_file_path="config.toml")
# singleton client
client_digipos = build_async_client(
    base_url=settings.clients.digipos.base_url,
    timeout=settings.clients.digipos.timeout,
    headers=settings.clients.digipos.headers,
    backoff_factor=settings.clients.digipos.wait,
    retries=settings.clients.digipos.retries,
)

client_isimple = build_async_client(
    base_url=settings.clients.isimple.base_url,
    timeout=settings.clients.isimple.timeout,
    headers=settings.clients.isimple.headers,
    backoff_factor=settings.clients.isimple.wait,
    retries=settings.clients.isimple.retries,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    app.state.settings = settings
    app.state.client_digipos = client_digipos
    app.state.client_isimple = client_isimple
    logger.bind(settings=settings).info("Application started")
    yield
    await client_digipos.aclose()
    await client_isimple.aclose()
    logger.info("Stopping application...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
