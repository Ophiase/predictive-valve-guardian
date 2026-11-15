from dataclasses import dataclass
from typing import Final, Self

from valve_guardian_contract import ModelCard, Prediction

from valve_guardian.arrays import Signals
from valve_guardian.features import FeatureSpecification
from valve_guardian.inference.artifact import ModelArtifact
from valve_guardian.inference.onnx_classifier import OnnxClassifier

THRESHOLD: Final = 0.5


@dataclass(frozen=True)
class Predictor:
    classifier: OnnxClassifier
    features: FeatureSpecification
    card: ModelCard

    @classmethod
    def load(cls, artifact: ModelArtifact) -> Self:
        card = artifact.card()
        return cls(
            classifier=OnnxClassifier.load(artifact.model),
            features=FeatureSpecification.of(card.features),
            card=card,
        )

    def predict(self, pressure: Signals, flow: Signals) -> tuple[Prediction, ...]:
        probabilities = self.classifier.optimal_probability(
            self.features.matrix(pressure, flow)
        )
        return tuple(
            Prediction(
                optimal=bool(probability >= THRESHOLD), probability=float(probability)
            )
            for probability in probabilities
        )
