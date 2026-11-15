from dataclasses import dataclass
from pathlib import Path
from typing import Final, Self

import numpy as np
import onnxruntime

from valve_guardian.arrays import FeatureMatrix, Probabilities

PROBABILITIES_OUTPUT: Final = "probabilities"
OPTIMAL_CLASS: Final = 1


@dataclass(frozen=True)
class OnnxClassifier:
    session: onnxruntime.InferenceSession

    @classmethod
    def load(cls, path: Path) -> Self:
        options = onnxruntime.SessionOptions()
        options.log_severity_level = 3
        return cls(
            onnxruntime.InferenceSession(path, options, ["CPUExecutionProvider"])
        )

    def optimal_probability(self, features: FeatureMatrix) -> Probabilities:
        feed = {self.session.get_inputs()[0].name: features.astype(np.float32)}
        (probabilities,) = self.session.run([PROBABILITIES_OUTPUT], feed)
        return np.asarray(probabilities)[:, OPTIMAL_CLASS]
