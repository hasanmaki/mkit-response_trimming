"""settings Loader and validator using pydantic_settings.

settings ini akan di store pada app state.settings untuk di akses pada seluruh bagian aplikasi.
"""

# ruff: noqa
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict, TomlConfigSettingsSource
from src.domain.digipos.schemas.cfg_digipos import DigiposConfig


class AppSettings(BaseSettings):
    """pastikan nama kelas adalah nama bagian header pada file toml. sebelum prefix
    contoh: [digipos.api] -> class Digipos: ApiSettings
    """

    digipos: DigiposConfig

    model_config = SettingsConfigDict(
        toml_file="",  # akan di set saat applikasi start
        extra="forbid",
        validate_assignment=True,
        from_attributes=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ) -> tuple[TomlConfigSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


@lru_cache
def get_settings(toml_file_path: str | None) -> AppSettings:
    """Get application settings with caching, without mutating global config."""
    try:
        if not toml_file_path:
            raise ValueError("TOML file path must be provided")
    except Exception as e:
        raise RuntimeError(f"Error obtaining TOML file path: {e}")
    AppSettings.model_config["toml_file"] = toml_file_path
    return AppSettings()  # type: ignore
