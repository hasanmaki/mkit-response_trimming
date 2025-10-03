# src/dependencies.py

from typing import Annotated

from fastapi import Depends, Request
from httpx import AsyncClient

from domain.digipos.dg_repos import DigiposRepos
from domain.digipos.sch_config import DigiposConfig
from src.config.settings import AppSettings


def get_app_settings(request: Request) -> AppSettings:
    """Ambil AppSettings dari app.state (layer: config)."""
    return request.app.state.settings


AppSettingsDep = Annotated[AppSettings, Depends(get_app_settings)]


def get_http_client(request: Request) -> AsyncClient:
    """Ambil shared AsyncClient dari app.state (layer: infra)."""
    return request.app.state.http_client


HttpClientDep = Annotated[AsyncClient, Depends(get_http_client)]


# digipos specific
def get_digipos_config(request: Request) -> DigiposConfig:
    """Ambil DigiposConfig langsung dari app.state."""
    return request.app.state.settings.digipos


DigiposConfigDep = Annotated[DigiposConfig, Depends(get_digipos_config)]


# digipos services
def get_digipos_repository(
    client: Annotated[AsyncClient, Depends(get_http_client)],
    config: Annotated[DigiposConfig, Depends(get_digipos_config)],
) -> DigiposRepos:
    """Factory function untuk membuat instance DigiposAccountServices."""
    return DigiposRepos(client, config)


DigiposRepoDep = Annotated[DigiposRepos, Depends(get_digipos_repository)]
