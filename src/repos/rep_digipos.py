from httpx import AsyncClient, Response

from src.config.cfg_api_digipos import DigiposConfig
from src.core.http_manager import cst_get


class DigiposRepository:
    """Repository untuk handle request ke Digipos API."""

    def __init__(self, client: AsyncClient, config: DigiposConfig):
        self.client: AsyncClient = client
        self.config: DigiposConfig = config

    async def get_balance(self, username: str) -> Response:
        url = self.config.build_url(self.config.endpoints.balance)
        response = await cst_get(
            client=self.client,
            url=url,
            params={"username": username},
            timeout=self.config.api.timeout,
        )
        return response
