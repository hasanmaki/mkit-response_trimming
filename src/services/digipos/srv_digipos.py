from urllib.parse import urljoin

from httpx import AsyncClient
from loguru import logger
from src.config.cfg_api_digipos import DigiposConfig, DigiposEndpoints
from src.core.http_manager import cst_get


class DigiposService:
    """Service Layer untuk semua interaksi dengan Digipos API."""

    def __init__(self, client: AsyncClient, config: DigiposConfig):
        self.client = client
        self.config = config

        # Simpan komponen yang dibutuhkan
        self._base_url = config.api.base_url
        self._endpoints: DigiposEndpoints = config.endpoints  # DigiposEndpoints
        self._timeout = config.api.timeout
        self._username = config.api.username
        self._pin = config.api.pin
        self._password = config.api.password

    def _build_url(self, endpoint: str) -> str:
        """Buat URL lengkap untuk endpoint tertentu."""
        return urljoin(self._base_url, endpoint)

    async def get_balance(self) -> dict:
        """Ambil saldo dari Digipos API."""
        if self._endpoints.balance is None:
            raise ValueError("Balance endpoint is not configured (None)")
        url = self._build_url(self._endpoints.balance)
        logger.debug(f"Fetching balance from URL: {url}")
        payload = {
            "username": self._username,
        }
        logger.debug(f" sending request full url {url} with payload {payload}")
        response = await cst_get(
            self.client, url, params=payload, timeout=self._timeout
        )
        return response.json()
