from urllib.parse import urlparse

from pydantic import BaseModel, field_validator


class BaseApiSettings(BaseModel):
    base_url: str
    retries: int = 3
    timeout: int = 10
    wait: int = 10

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid URL format")
        return v


# Digipos Specific Settings
class DigiposCredential(BaseApiSettings):
    username: str
    password: str
    pin: str


class DigiposSettings(BaseModel):
    # Nama model harus sama dengan sub header semisal [digipos.---] / [isimple.---]
    api: DigiposCredential


# Isimple Spesific Settings
class IsimpleCredential(BaseApiSettings):
    msisdn: str
    pin: str


class IsimpleSettings(BaseModel):
    # Nama model harus sama dengan sub header semisal [digipos.---] / [isimple.---]
    api: IsimpleCredential
