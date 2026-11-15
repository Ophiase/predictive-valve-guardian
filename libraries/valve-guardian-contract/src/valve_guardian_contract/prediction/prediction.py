from pydantic import BaseModel, Field


class Prediction(BaseModel):
    optimal: bool = Field(description="True when the valve is predicted at 100 %.")
    probability: float = Field(ge=0, le=1, description="P(valve optimal).")
