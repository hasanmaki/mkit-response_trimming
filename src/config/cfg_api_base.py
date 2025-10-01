from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator

default_headers = {
    "User-Agent": "MyApp/1.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class BaseApiSettings(BaseModel):
    base_url: str
    timeout: int = 10
    headers: dict[str, str] | None = Field(default_headers)

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid URL format")
        return v
