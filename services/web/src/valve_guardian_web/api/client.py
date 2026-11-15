from dataclasses import dataclass
from typing import Final

import httpx
import numpy as np
from valve_guardian_contract import (
    Cycle,
    ModelCard,
    PredictionRequest,
    PredictionResponse,
)

BATCH: Final = 64
TIMEOUT_SECONDS: Final = 60


@dataclass(frozen=True)
class ApiClient:
    http: httpx.Client

    def card(self) -> ModelCard:
        response = self.http.get("/model", timeout=TIMEOUT_SECONDS)
        return ModelCard.model_validate_json(response.raise_for_status().content)

    def predict(self, pressure: np.ndarray, flow: np.ndarray) -> PredictionResponse:
        """Every cycle, in batches; the answer names the model of the last batch."""
        responses = [
            self.batch(pressure[start : start + BATCH], flow[start : start + BATCH])
            for start in range(0, len(pressure), BATCH)
        ]
        return PredictionResponse(
            model=responses[-1].model,
            predictions=[
                each for response in responses for each in response.predictions
            ],
        )

    def batch(self, pressure: np.ndarray, flow: np.ndarray) -> PredictionResponse:
        request = PredictionRequest.model_construct(
            cycles=[
                Cycle.model_construct(pressure=each.tolist(), flow=other.tolist())
                for each, other in zip(pressure, flow, strict=True)
            ]
        )
        response = self.http.post(
            "/predictions",
            content=request.model_dump_json(),
            headers={"content-type": "application/json"},
            timeout=TIMEOUT_SECONDS,
        )
        return PredictionResponse.model_validate_json(
            response.raise_for_status().content
        )
