from dataclasses import dataclass

from valve_guardian.features import Representation
from valve_guardian_contract import MetricSummary

from valve_guardian_training.estimators import Candidate


@dataclass(frozen=True)
class Result:
    representation: Representation
    candidate: Candidate
    columns: int
    cross_validation: dict[str, MetricSummary]

    @property
    def f1(self) -> MetricSummary:
        return self.cross_validation["f1"]

    @property
    def simplicity(self) -> tuple[int, int]:
        return (self.candidate.complexity, self.columns)
