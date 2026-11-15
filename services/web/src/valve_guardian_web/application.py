from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from valve_guardian_web.analysis import AnalysisStore
from valve_guardian_web.api import ApiClient
from valve_guardian_web.pages.routes import router
from valve_guardian_web.settings import WebSettings

STATIC = Path(__file__).parent / "pages" / "static"


def create(client: ApiClient) -> FastAPI:
    application = FastAPI(title="Valve Guardian", docs_url=None, redoc_url=None)
    application.state.client = client
    application.state.store = AnalysisStore()
    application.mount("/static", StaticFiles(directory=STATIC), name="static")
    application.include_router(router)
    return application


def main() -> None:
    settings = WebSettings()
    client = ApiClient(httpx.Client(base_url=str(settings.api_url)))
    uvicorn.run(create(client), host=settings.host, port=settings.port)
