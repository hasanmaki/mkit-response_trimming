from src.config.settings import AppSettings
from src.services.clients.base_client import BaseApiClient


class DigiposClient(BaseApiClient):
    """Digipos API client."""

    def __init__(self, settings: AppSettings):
        super().__init__(
            base_url=settings.clients.digipos.base_url,
            timeout=settings.clients.digipos.timeout,
            headers=settings.clients.digipos.headers,
        )
        self.username = settings.clients.digipos.username
        self.password = settings.clients.digipos.password
        self.pin = settings.clients.digipos.pin
