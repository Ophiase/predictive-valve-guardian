from dataclasses import dataclass

import numpy as np

from valve_guardian.arrays import FeatureMatrix, Signals
from valve_guardian.features.order import DerivativeOrder
from valve_guardian.features.representation import Representation
from valve_guardian.features.statistics import CycleStatistics

DEFAULT_FOURIER_COEFFICIENTS = 20


@dataclass(frozen=True)
class FeatureSpecification(Representation):
    order: DerivativeOrder = DerivativeOrder.SIGNAL
    fourier: bool = False
    fourier_coefficients: int = DEFAULT_FOURIER_COEFFICIENTS

    def matrix(self, pressure: Signals, flow: Signals) -> FeatureMatrix:
        return np.hstack([self.of_signal(pressure), self.of_signal(flow)])

    def of_signal(self, signals: Signals) -> FeatureMatrix:
        columns = [CycleStatistics.of(signals)]
        derivative = signals
        for _ in range(self.order):
            derivative = np.diff(derivative, axis=1)
            columns.append(CycleStatistics.of(derivative))
        if self.fourier:
            columns.append(self.spectrum(signals))
        return np.hstack(columns)

    def spectrum(self, signals: Signals) -> FeatureMatrix:
        magnitudes = np.abs(np.fft.rfft(signals, axis=1))
        return magnitudes[:, : self.fourier_coefficients]

    @property
    def columns_per_signal(self) -> int:
        statistics = CycleStatistics.COLUMNS * (self.order + 1)
        return statistics + (self.fourier_coefficients if self.fourier else 0)

    @property
    def name(self) -> str:
        fourier = f" + {self.fourier_coefficients} fourier" if self.fourier else ""
        return f"statistics to {self.order.name.lower()}{fourier}"
