from typing import Annotated

import numpy as np
from fastapi import APIRouter, Depends, Request
from valve_guardian.inference import Predictor
from valve_guardian_contract import ModelCard, PredictionRequest, PredictionResponse

router = APIRouter()


def predictor(request: Request) -> Predictor:
    return request.app.state.predictor


type LoadedPredictor = Annotated[Predictor, Depends(predictor)]


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/model")
def model(loaded: LoadedPredictor) -> ModelCard:
    return loaded.card


@router.post("/predictions")
def predictions(
    request: PredictionRequest, loaded: LoadedPredictor
) -> PredictionResponse:
    pressure = np.array([cycle.pressure for cycle in request.cycles])
    flow = np.array([cycle.flow for cycle in request.cycles])
    return PredictionResponse(
        model=loaded.card.identifier,
        predictions=list(loaded.predict(pressure, flow)),
    )
