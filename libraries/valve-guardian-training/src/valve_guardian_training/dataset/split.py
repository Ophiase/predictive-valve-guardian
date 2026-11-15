from dataclasses import dataclass
from typing import Final, Self

from valve_guardian.arrays import FeatureMatrix, Labels

TRAINING_CYCLES: Final = 2_000


@dataclass(frozen=True)
class Split:
    training_features: FeatureMatrix
    training_labels: Labels
    test_features: FeatureMatrix
    test_labels: Labels

    @classmethod
    def chronological(
        cls,
        features: FeatureMatrix,
        labels: Labels,
        training_cycles: int = TRAINING_CYCLES,
    ) -> Self:
        """The first `training_cycles` cycles train, the rest test: no shuffle."""
        return cls(
            training_features=features[:training_cycles],
            training_labels=labels[:training_cycles],
            test_features=features[training_cycles:],
            test_labels=labels[training_cycles:],
        )
