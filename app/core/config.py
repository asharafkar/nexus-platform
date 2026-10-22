
from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NEXUS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    service_name: str = "Nexus Platform"
    service_description: str = (
        "A production-oriented microservices and AI platform."
    )
    app_version: str = "0.1.0"
    environment: Literal["development", "testing", "production"] = "development"
    debug: bool = False
    database_url: str | None = None

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.environment == "production" and self.debug:
            raise ValueError("Debug mode must be disabled in production.")

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
