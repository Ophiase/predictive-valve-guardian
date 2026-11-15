from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from valve_guardian.inference import ModelArtifact


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VALVE_GUARDIAN_API_")

    host: str = Field(default="127.0.0.1", description="Interface to bind.")
    port: int = Field(default=8000, ge=1, le=65_535)
    model_directory: Path = Field(
        default=ModelArtifact().directory,
        description="Folder holding model.onnx and model-card.json.",
    )
