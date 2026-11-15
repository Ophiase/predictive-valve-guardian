from typing import Annotated, Final

from pydantic import BaseModel, Field

from valve_guardian_contract.prediction.cycle import Cycle

MAXIMUM_BATCH: Final = 256


class PredictionRequest(BaseModel):
    cycles: Annotated[list[Cycle], Field(min_length=1, max_length=MAXIMUM_BATCH)]
