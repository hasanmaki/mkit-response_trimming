from pydantic import BaseModel, Field


class ReqBalance(BaseModel):
    """model untuk request balance digipos."""

    username: str = Field(
        description="Username Digipos, harus match dengan username yang di setup di settings",
    )


class ResReqBalance(BaseModel):
    """model untuk response balance digipos."""

    ngrs: dict[str, str] = Field(description="NGRS balance")

    linkaja: str = Field(description="LinkAja balance")
    finpay: str = Field(
        description="Finpay balance",
    )

    model_config = {"from_attributes": True}
