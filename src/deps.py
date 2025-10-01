# src/dependencies.py

from typing import Annotated

from fastapi import Depends, Request
from httpx import AsyncClient

from src.config.cfg_api_digipos import DigiposConfig
from src.config.settings import AppSettings
from src.services.digipos.srv_digipos import DigiposService


def get_app_settings(request: Request) -> AppSettings:
    """Ambil AppSettings dari app.state (layer: config)."""
    return request.app.state.settings


AppSettingsDep = Annotated[AppSettings, Depends(get_app_settings)]


def get_http_client(request: Request) -> AsyncClient:
    """Ambil shared AsyncClient dari app.state (layer: infra)."""
    return request.app.state.http_client


HttpClientDep = Annotated[AsyncClient, Depends(get_http_client)]


# digipos specific
def get_digipos_config(settings: AppSettings) -> DigiposConfig:
    """Ambil DigiposConfig dari AppSettings (AppSettings diambil dari app.state via dependency chain)."""
    return settings.digipos


DigiposConfigDep = Annotated[DigiposConfig, Depends(get_digipos_config)]


def get_digipos_service(
    client: HttpClientDep,
    config: DigiposConfigDep,
) -> DigiposService:
    """Inisialisasi DigiposService (layer: service) dengan dependency explicit."""
    return DigiposService(client=client, config=config)


DigiposServiceDep = Annotated[DigiposService, Depends(get_digipos_service)]
