from typing import Annotated, Final

from pydantic import BaseModel, Field

PRESSURE_SAMPLES: Final = 6_000
FLOW_SAMPLES: Final = 600

type PressureSignal = Annotated[
    list[float],
    Field(
        min_length=PRESSURE_SAMPLES,
        max_length=PRESSURE_SAMPLES,
        description="PS2, in bar, sampled at 100 Hz over one 60 s cycle.",
    ),
]
type FlowSignal = Annotated[
    list[float],
    Field(
        min_length=FLOW_SAMPLES,
        max_length=FLOW_SAMPLES,
        description="FS1, in l/min, sampled at 10 Hz over one 60 s cycle.",
    ),
]


class Cycle(BaseModel):
    pressure: PressureSignal
    flow: FlowSignal
