from pydantic import BaseModel
from src.config.cfg_api_base import BaseApiSettings


# Digipos Specific Settings
class DigiposAccounts(BaseApiSettings):
    username: str
    password: str
    pin: str


class DigiposConfig(BaseModel):
    api: list[DigiposAccounts]
