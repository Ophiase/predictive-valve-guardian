import math
from dataclasses import dataclass
from typing import Final

NICE_STEPS: Final = (1.0, 2.0, 2.5, 5.0, 10.0)


@dataclass(frozen=True)
class Tick:
    position: float
    label: str

    @staticmethod
    def step(span: float, count: int) -> float:
        """The smallest 1, 2, 2.5 or 5 times a power of ten within `count` steps."""
        raw = (span or 1.0) / count
        magnitude = 10 ** math.floor(math.log10(raw))
        return next(nice * magnitude for nice in NICE_STEPS if nice * magnitude >= raw)

    @staticmethod
    def label_of(value: float, step: float) -> str:
        decimals = max(0, -math.floor(math.log10(step))) if step < 1 else 0
        return f"{value:.{decimals}f}"
