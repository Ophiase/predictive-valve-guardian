import time
from dataclasses import dataclass
from typing import Self

from sklearn.metrics import accuracy_score, f1_score

from valve_guardian.dataset import Split
from valve_guardian.model import Classifier


@dataclass(frozen=True)
class Measure:
    accuracy: float
    f1: float
    training_seconds: float
    prediction_seconds: float

    @classmethod
    def of(cls, model: Classifier, split: Split) -> Self:
        start = time.perf_counter()
        model.fit(split.training_features, split.training_labels)
        trained = time.perf_counter()
        predicted_labels = model.predict(split.test_features)
        predicted = time.perf_counter()
        return cls(
            accuracy=float(accuracy_score(split.test_labels, predicted_labels)),
            f1=float(f1_score(split.test_labels, predicted_labels)),
            training_seconds=trained - start,
            prediction_seconds=predicted - trained,
        )
