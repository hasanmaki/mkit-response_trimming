"""digipos service account repository."""

from httpx import AsyncClient

from domain.digipos.dg_repos import DigiposRepos
from src.domain.digipos.sch_config import DigiposConfig


class DigiposAccountService:
    def __init__(self, client: AsyncClient, config: DigiposConfig):
        self.repo = DigiposRepos(client, config)

    async def get_balance(self, username: str):
        # check id username is not none and match with config
        if username is None or username != self.repo.config.api.username:
            raise ValueError("Invalid username")
        return await self.repo.get_balance(username=username)
