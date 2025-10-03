from httpx import AsyncClient, Response

from core.http_utils import cst_get
from domain.digipos.sch_config import DigiposConfig


class DigiposRepos:
    """Repository untuk handle request ke Digipos API."""

    def __init__(self, client: AsyncClient, config: DigiposConfig):
        self.client: AsyncClient = client
        self.config: DigiposConfig = config
        self.default_timeout = self.config.api.timeout or self.client.timeout

    async def get_balance(self, username: str) -> Response:
        url = self.config.build_url(self.config.endpoints.balance)
        return await cst_get(
            client=self.client,
            url=url,
            params={"username": username},
            timeout=self.default_timeout,
        )
