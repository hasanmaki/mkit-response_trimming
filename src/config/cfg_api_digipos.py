from urllib.parse import urljoin

from pydantic import BaseModel, Field

from config.cfg_shared import BaseApiSettings


class DigiposAccounts(BaseApiSettings):
    username: str
    password: str
    pin: str


class DigiposEndpoints(BaseModel):
    login: str = Field("/login", description="Endpoint for login")
    logout: str = Field("/logout", description="Endpoint for logout")
    balance: str = Field("/balance", description="Endpoint for balance")
    profile: str = Field("/profile", description="Endpoint for profile")
    list_paket: str = Field("/list_paket", description="Endpoint for list paket")
    paket: str = Field("/paket", description="Endpoint for paket")


class DigiposConfig(BaseModel):
    api: DigiposAccounts
    endpoints: DigiposEndpoints = Field(
        default_factory=lambda: DigiposEndpoints()  # type: ignore
    )

    def build_url(self, endpoint: str) -> str:
        return urljoin(self.api.base_url, endpoint or "")
