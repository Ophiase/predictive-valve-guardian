from dataclasses import dataclass
from typing import Final, Self

import numpy as np
from valve_guardian.arrays import Labels, Profiles, Signals

from valve_guardian_training.dataset.archive import HydraulicArchive

VALVE_COLUMN: Final = 1
OPTIMAL_VALVE: Final = 100


@dataclass(frozen=True)
class Cycles:
    pressure: Signals
    flow: Signals
    profile: Profiles

    @classmethod
    def load(cls, archive: HydraulicArchive) -> Self:
        archive.ensure()
        return cls(
            pressure=np.loadtxt(archive.pressure),
            flow=np.loadtxt(archive.flow),
            profile=np.loadtxt(archive.profile),
        )

    @property
    def optimal_valve(self) -> Labels:
        return (self.profile[:, VALVE_COLUMN] == OPTIMAL_VALVE).astype(np.int64)
