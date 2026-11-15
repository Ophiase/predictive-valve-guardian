from dataclasses import dataclass
from typing import Self

from valve_guardian.arrays import Signals
from valve_guardian.features import Representation
from valve_guardian.model.classifier import Classifier
from valve_guardian.model.deployed import DEPLOYED_FEATURES, DeployedModel


@dataclass(frozen=True)
class Predictor:
    model: Classifier
    representation: Representation

    @classmethod
    def deployed(cls) -> Self:
        return cls(model=DeployedModel.load(), representation=DEPLOYED_FEATURES)

    def optimal_valve(self, pressure: Signals, flow: Signals) -> tuple[bool, ...]:
        """One verdict per cycle: True when the valve is predicted at 100 %."""
        features = self.representation.matrix(pressure, flow)
        return tuple(bool(label) for label in self.model.predict(features))
