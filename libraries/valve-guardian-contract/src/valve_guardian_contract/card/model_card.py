from datetime import datetime

from pydantic import BaseModel, Field

from valve_guardian_contract.card.features import FeatureSettings
from valve_guardian_contract.card.metric import MetricSummary


class ModelCard(BaseModel):
    identifier: str = Field(description="Content hash of the ONNX file.")
    estimator: str = Field(description="The candidate chosen by the selection.")
    features: FeatureSettings
    cross_validation: dict[str, MetricSummary] = Field(
        description="Repeated stratified k-fold over every cycle."
    )
    holdout: dict[str, float] = Field(
        description="Trained on the first cycles, scored on the last ones."
    )
    dataset_sha256: str = Field(description="Hash of the three source files.")
    trained_at: datetime
    versions: dict[str, str] = Field(description="Library versions at training.")
