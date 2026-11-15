from typing import Protocol, Self

from valve_guardian.arrays import FeatureMatrix, Labels


class Classifier(Protocol):
    def fit(self, features: FeatureMatrix, labels: Labels, /) -> Self: ...
    def predict(self, features: FeatureMatrix, /) -> Labels: ...
