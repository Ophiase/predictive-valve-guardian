from collections.abc import Iterator, Sequence

from valve_guardian.features import Representation

from valve_guardian_training.dataset import Cycles
from valve_guardian_training.estimators import CANDIDATES
from valve_guardian_training.evaluation import CrossValidation, Result


class Benchmark:
    """Every candidate on every representation, scored by repeated cross-validation."""

    @classmethod
    def run(
        cls, cycles: Cycles, representations: Sequence[Representation]
    ) -> tuple[Result, ...]:
        return tuple(
            result for each in representations for result in cls.of(cycles, each)
        )

    @staticmethod
    def of(cycles: Cycles, representation: Representation) -> Iterator[Result]:
        features = representation.matrix(cycles.pressure, cycles.flow)
        for candidate in CANDIDATES:
            yield Result(
                representation=representation,
                candidate=candidate,
                columns=features.shape[1],
                cross_validation=CrossValidation.summary(
                    candidate.pipeline(), features, cycles.optimal_valve
                ),
            )
