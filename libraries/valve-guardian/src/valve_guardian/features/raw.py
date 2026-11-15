import numpy as np

from valve_guardian.arrays import FeatureMatrix, Signals
from valve_guardian.features.representation import Representation


class RawSignals(Representation):
    """The two signals side by side, every sample a column."""

    def matrix(self, pressure: Signals, flow: Signals) -> FeatureMatrix:
        return np.hstack([pressure, flow])

    @property
    def name(self) -> str:
        return "raw"
