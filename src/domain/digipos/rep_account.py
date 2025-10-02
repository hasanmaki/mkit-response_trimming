from httpx import AsyncClient, Response

from domain.digipos.sch_config import DigiposConfig
from src.core.http_manager import cst_get


class DigiposRepos:
    """Repository untuk handle request ke Digipos API untuk fitur account."""

    def __init__(self, client: AsyncClient, config: DigiposConfig):
        self.client: AsyncClient = client
        self.config: DigiposConfig = config
        self.default_timeout = self.config.api.timeout or self.client.timeout

    async def get_balance(self) -> Response:
        url = self.config.build_url(self.config.endpoints.balance)
        username = self.config.api.username
        response = await cst_get(
            client=self.client,
            url=url,
            params={"username": username},
            timeout=self.default_timeout,
        )
        return response.json()

    async def login(self) -> Response:
        url = self.config.build_url(self.config.endpoints.login)
        username = self.config.api.username
        password = self.config.api.password
        response = await cst_get(
            client=self.client,
            url=url,
            params={"username": username, "password": password},
            timeout=self.default_timeout,
        )
        return response.json()
