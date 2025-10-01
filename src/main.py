from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.config.cfg_logging import setup_logging
from src.config.settings import AppSettings, get_settings
from src.services.clients.client_digipos import DigiposClient

setup_logging()
settings: AppSettings = get_settings(toml_file_path="config.toml")
# singleton client
digipos_client = DigiposClient(settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    app.state.settings = settings
    app.state.client_digipos = digipos_client

    logger.bind(settings=settings).info("Application started")
    yield
    await digipos_client.close()
    logger.info("Stopping application...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
