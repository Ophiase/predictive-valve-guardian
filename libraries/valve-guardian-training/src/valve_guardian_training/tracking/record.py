from dataclasses import dataclass
from pathlib import Path

from valve_guardian_contract import ModelCard


@dataclass(frozen=True)
class RunRecord:
    name: str
    parameters: dict[str, str | int | float]
    metrics: dict[str, float]
    card: ModelCard
    artifact: Path
    report: str
