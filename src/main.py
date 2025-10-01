from contextlib import asynccontextmanager
from venv import logger

import uvicorn
from fastapi import FastAPI

from src.config.cfg_logging import setup_logging
from src.config.settings import AppSettings, get_settings

setup_logging()
settings: AppSettings = get_settings(toml_file_path="config.toml")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    app.state.settings = settings
    logger.debug(f"App settings: {app.state.settings}")
    yield
    app.state.settings = None
    logger.info("Stopping application...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True)
