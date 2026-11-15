from dataclasses import dataclass
from typing import Self

import numpy as np
from valve_guardian_contract import FeatureSettings

from valve_guardian.arrays import FeatureMatrix, Signals
from valve_guardian.features.order import DerivativeOrder
from valve_guardian.features.representation import Representation
from valve_guardian.features.statistics import CycleStatistics


@dataclass(frozen=True)
class FeatureSpecification(Representation):
    order: DerivativeOrder = DerivativeOrder.SIGNAL
    fourier_coefficients: int = 0

    @classmethod
    def of(cls, settings: FeatureSettings) -> Self:
        return cls(DerivativeOrder(settings.order), settings.fourier_coefficients)

    @property
    def settings(self) -> FeatureSettings:
        return FeatureSettings(
            order=self.order, fourier_coefficients=self.fourier_coefficients
        )

    def matrix(self, pressure: Signals, flow: Signals) -> FeatureMatrix:
        return np.hstack([self.of_signal(pressure), self.of_signal(flow)])

    def of_signal(self, signals: Signals) -> FeatureMatrix:
        columns = [CycleStatistics.of(signals)]
        derivative = signals
        for _ in range(self.order):
            derivative = np.diff(derivative, axis=1)
            columns.append(CycleStatistics.of(derivative))
        columns.append(self.spectrum(signals))
        return np.hstack(columns)

    def spectrum(self, signals: Signals) -> FeatureMatrix:
        magnitudes = np.abs(np.fft.rfft(signals, axis=1))
        return magnitudes[:, : self.fourier_coefficients]

    @property
    def columns_per_signal(self) -> int:
        return CycleStatistics.COLUMNS * (self.order + 1) + self.fourier_coefficients

    @property
    def name(self) -> str:
        fourier = (
            f" + {self.fourier_coefficients} fourier"
            if self.fourier_coefficients
            else ""
        )
        return f"statistics to {self.order.name.lower()}{fourier}"
