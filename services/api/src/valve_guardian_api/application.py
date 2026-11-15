from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from importlib.metadata import version

import uvicorn
from fastapi import FastAPI
from valve_guardian.inference import ModelArtifact, Predictor

from valve_guardian_api.routes import router
from valve_guardian_api.settings import ApiSettings


def create(settings: ApiSettings) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncGenerator[None]:
        application.state.predictor = Predictor.load(
            ModelArtifact(settings.model_directory)
        )
        yield

    application = FastAPI(
        title="Valve Guardian API",
        version=version("valve-guardian-api"),
        lifespan=lifespan,
    )
    application.include_router(router)
    return application


def main() -> None:
    settings = ApiSettings()
    uvicorn.run(create(settings), host=settings.host, port=settings.port)
