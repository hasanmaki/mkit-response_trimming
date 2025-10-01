from urllib.parse import urljoin

from httpx import AsyncClient
from src.config.cfg_api_digipos import DigiposConfig


class DigiposService:
    """Service Layer untuk semua interaksi dengan Digipos API."""

    def __init__(self, client: AsyncClient, config: DigiposConfig):
        self.client = client
        self.config = config

        # Simpan komponen yang dibutuhkan
        self._base_url = config.api.base_url
        self._endpoints = config.endpoints  # DigiposEndpoints
        self._timeout = config.api.timeout
        self._username = config.api.username
        self._pin = config.api.pin
        self._password = config.api.password

    def _build_url(self, endpoint: str) -> str:
        """Buat URL lengkap untuk endpoint tertentu."""
        # Jika endpoint_path dari config sudah pasti string (bukan None),
        # Anda bisa langsung mendapatkan path dari attribute (seperti yang Anda lakukan di login/balance)

        # urljoin sudah menangani slashes dengan baik
        return urljoin(self._base_url, endpoint)

    async def get_balance(self) -> dict:
        """Ambil saldo dari Digipos API."""
        if self._endpoints.balance is None:
            raise ValueError("Balance endpoint is not configured (None)")
        url = self._build_url(self._endpoints.balance)
        payload = {
            "username": self._username,
        }
        response = await self.client.get(url, params=payload, timeout=self._timeout)
        response.raise_for_status()
        return response.json()
