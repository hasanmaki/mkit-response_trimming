from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.config.cfg_logging import setup_logging
from src.config.settings import AppSettings, get_settings

setup_logging()
settings: AppSettings = get_settings(toml_file_path="config.toml")
# digipos_client = DigiposClient(settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    # app.state.client_digipos = digipos_client

    # logger.bind(digipos_client=digipos_client).info("Digipos client initialized")
    yield
    # await digipos_client.close()
    logger.info("Stopping application...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
