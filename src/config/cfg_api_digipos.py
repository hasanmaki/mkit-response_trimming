from pydantic import BaseModel, Field

from config.cfg_shared import BaseApiSettings


# Digipos Specific Settings
class DigiposAccounts(BaseApiSettings):
    username: str
    password: str
    pin: str


class DigiposEndpoints(BaseModel):
    login: str | None = Field("/login", description="Endpoint for login")
    logout: str | None = Field("/logout", description="Endpoint for logout")
    balance: str | None = Field("/balance", description="Endpoint for balance")
    profile: str | None = Field("/profile", description="Endpoint for profile")
    list_paket: str | None = Field("/list_paket", description="Endpoint for list paket")
    paket: str | None = Field("/paket", description="Endpoint for paket")


class DigiposConfig(BaseModel):
    api: DigiposAccounts
    endpoints: DigiposEndpoints = Field(
        default_factory=lambda: DigiposEndpoints()  # type: ignore
    )
