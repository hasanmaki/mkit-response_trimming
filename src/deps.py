# src/dependencies.py

from typing import Annotated

from fastapi import Depends, Request

from src.config.settings import AppSettings


# Dependency untuk injeksi global settings
def get_app_settings(request: Request) -> AppSettings:
    """Mengambil settings dari app.state."""
    # Selalu ambil dari app.state
    return request.app.state.settings


AppSettingsDep = Annotated[AppSettings, Depends(get_app_settings)]


# Dependency untuk injeksi Digipos Config spesifik
def get_digipos_config(settings: AppSettingsDep):
    """Mengambil konfigurasi Digipos API spesifik."""
    return settings.digipos.api
