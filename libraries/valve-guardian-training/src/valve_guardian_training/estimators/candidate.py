from dataclasses import dataclass

from sklearn.pipeline import Pipeline

from valve_guardian_training.estimators.factory import PipelineFactory


@dataclass(frozen=True)
class Candidate:
    """An estimator family; a lower `complexity` wins a tie in the selection."""

    name: str
    complexity: int
    build: PipelineFactory

    def pipeline(self) -> Pipeline:
        return self.build()
