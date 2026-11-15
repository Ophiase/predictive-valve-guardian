from pydantic import BaseModel, Field


class MetricSummary(BaseModel):
    mean: float
    deviation: float = Field(description="Standard deviation across folds.")
