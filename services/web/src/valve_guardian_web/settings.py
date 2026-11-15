from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WebSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VALVE_GUARDIAN_WEB_")

    api_url: AnyHttpUrl = Field(description="Where the valve guardian API answers.")
    host: str = Field(default="127.0.0.1", description="Interface to bind.")
    port: int = Field(default=8080, ge=1, le=65_535)
