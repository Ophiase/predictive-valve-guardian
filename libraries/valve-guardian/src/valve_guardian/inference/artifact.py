from dataclasses import dataclass
from pathlib import Path
from typing import Final

from valve_guardian_contract import ModelCard

PACKAGED: Final = Path(__file__).parent.parent / "artifact"


@dataclass(frozen=True)
class ModelArtifact:
    """A folder holding the ONNX model and the card that describes it."""

    directory: Path = PACKAGED

    @property
    def model(self) -> Path:
        return self.directory / "model.onnx"

    @property
    def card_path(self) -> Path:
        return self.directory / "model-card.json"

    def card(self) -> ModelCard:
        return ModelCard.model_validate_json(self.card_path.read_text())

    def write(self, model: bytes, card: ModelCard) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        self.model.write_bytes(model)
        self.card_path.write_text(card.model_dump_json(indent=2) + "\n")
