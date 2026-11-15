from dataclasses import dataclass
from typing import Final, Self

import numpy as np

from valve_guardian_web.pages.figures.tick import Tick

WIDTH: Final = 720
HEIGHT: Final = 180
LEFT: Final = 52
BOTTOM: Final = 24
TOP: Final = 8
RIGHT: Final = 12
CYCLE_SECONDS: Final = 60
SECONDS_STEP: Final = 10
VALUE_TICKS: Final = 4
POINTS: Final = 720


@dataclass(frozen=True)
class Chart:
    """One signal over its 60 s cycle: an SVG line and ticks in a WIDTH x HEIGHT box."""

    line: str
    values: tuple[Tick, ...]
    seconds: tuple[Tick, ...]

    @classmethod
    def of(cls, signal: np.ndarray) -> Self:
        sampled = signal[:: max(1, len(signal) // POINTS)]
        step = Tick.step(float(sampled.max() - sampled.min()), VALUE_TICKS)
        low = np.floor(sampled.min() / step) * step
        high = max(np.ceil(sampled.max() / step) * step, low + step)
        abscissa = np.linspace(LEFT, WIDTH - RIGHT, len(sampled))
        ordinate = cls.vertical(sampled, low, high)
        points = " ".join(
            f"{x:.1f},{y:.1f}" for x, y in zip(abscissa, ordinate, strict=True)
        )
        return cls(
            line=points,
            values=tuple(
                Tick(
                    float(cls.vertical(np.array([value]), low, high)[0]),
                    Tick.label_of(value, step),
                )
                for value in np.arange(low, high + step / 2, step)
            ),
            seconds=tuple(
                Tick(
                    LEFT + second / CYCLE_SECONDS * (WIDTH - LEFT - RIGHT),
                    f"{second} s",
                )
                for second in range(0, CYCLE_SECONDS + 1, SECONDS_STEP)
            ),
        )

    @staticmethod
    def vertical(values: np.ndarray, low: float, high: float) -> np.ndarray:
        return HEIGHT - BOTTOM - (values - low) / (high - low) * (HEIGHT - BOTTOM - TOP)
