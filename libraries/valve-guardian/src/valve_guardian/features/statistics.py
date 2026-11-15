from typing import Final

import numpy as np

from valve_guardian.arrays import FeatureMatrix, Signals

LOW_QUANTILE: Final = 0.1
HIGH_QUANTILE: Final = 0.9


class CycleStatistics:
    """Seven columns per cycle: mean, std, min, max, low and high quantiles, energy."""

    COLUMNS: Final = 7

    @staticmethod
    def of(signals: Signals) -> FeatureMatrix:
        return np.stack(
            [
                signals.mean(axis=1),
                signals.std(axis=1),
                signals.min(axis=1),
                signals.max(axis=1),
                np.quantile(signals, LOW_QUANTILE, axis=1),
                np.quantile(signals, HIGH_QUANTILE, axis=1),
                np.sum(signals**2, axis=1),
            ],
            axis=1,
        )
