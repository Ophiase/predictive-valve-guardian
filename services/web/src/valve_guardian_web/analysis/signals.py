from dataclasses import dataclass
from io import BytesIO
from typing import Self

import numpy as np
from valve_guardian_contract import FLOW_SAMPLES, PRESSURE_SAMPLES


@dataclass(frozen=True)
class UploadedSignals:
    """One row per cycle, as the UCI files lay them out: PS2 and FS1."""

    pressure: np.ndarray
    flow: np.ndarray

    @classmethod
    def parse(cls, pressure: bytes, flow: bytes) -> Self:
        signals = cls(pressure=cls.rows(pressure), flow=cls.rows(flow))
        signals.validate()
        return signals

    @staticmethod
    def rows(content: bytes) -> np.ndarray:
        return np.atleast_2d(np.loadtxt(BytesIO(content), dtype=np.float32))

    def validate(self) -> None:
        if self.pressure.shape[1] != PRESSURE_SAMPLES:
            raise ValueError(f"PS2 needs {PRESSURE_SAMPLES} samples per cycle")
        if self.flow.shape[1] != FLOW_SAMPLES:
            raise ValueError(f"FS1 needs {FLOW_SAMPLES} samples per cycle")
        if len(self.pressure) != len(self.flow):
            raise ValueError("PS2 and FS1 must hold the same number of cycles")

    @property
    def cycles(self) -> int:
        return len(self.pressure)
