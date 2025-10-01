from pydantic import BaseModel

from config.cfg_shared import BaseApiSettings


# Digipos Specific Settings
class DigiposAccounts(BaseApiSettings):
    username: str
    password: str
    pin: str


class DigiposConfig(BaseModel):
    api: DigiposAccounts
