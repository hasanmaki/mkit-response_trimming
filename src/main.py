from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from httpx import AsyncClient, Limits
from loguru import logger

from src.config import AppSettings, get_settings
from src.config.cfg_logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: AppSettings = get_settings(toml_file_path="config.toml")
    logger.bind(settings=settings.model_dump()).info(
        " loaded settings from config.toml"
    )
    app.state.http_client = AsyncClient(
        headers=settings.clients.headers,
        limits=Limits(max_connections=settings.clients.max_connections),
        timeout=settings.clients.timeout,
        http2=settings.clients.http2,
    )
    yield
    await app.state.http_client.aclose()
    logger.info("Stopping application...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
