from pydantic import BaseModel, Field

from valve_guardian_contract.prediction.prediction import Prediction


class PredictionResponse(BaseModel):
    model: str = Field(description="The identifier of the model card that answered.")
    predictions: list[Prediction] = Field(description="One per cycle, in order.")
