from pathlib import Path
from typing import Annotated, Final

import httpx
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from valve_guardian_web.analysis import Analysis, AnalysisStore, UploadedSignals
from valve_guardian_web.api import ApiClient
from valve_guardian_web.pages import figures

TEMPLATES: Final = Jinja2Templates(directory=Path(__file__).parent / "templates")

router = APIRouter()


def client(request: Request) -> ApiClient:
    return request.app.state.client


def store(request: Request) -> AnalysisStore:
    return request.app.state.store


type Client = Annotated[ApiClient, Depends(client)]
type Store = Annotated[AnalysisStore, Depends(store)]


@router.get("/", response_class=HTMLResponse)
def index(request: Request, api: Client, error: str | None = None) -> HTMLResponse:
    try:
        card = api.card()
    except httpx.HTTPError:
        card = None
    context = {"card": card, "error": error}
    return TEMPLATES.TemplateResponse(request, "index.html", context)


@router.post("/analyses", response_model=None)
def analyse(
    request: Request,
    api: Client,
    analyses: Store,
    pressure: Annotated[UploadFile, File()],
    flow: Annotated[UploadFile, File()],
) -> HTMLResponse | RedirectResponse:
    try:
        signals = UploadedSignals.parse(pressure.file.read(), flow.file.read())
    except ValueError as error:
        return index(request, api, error=str(error))
    response = api.predict(signals.pressure, signals.flow)
    analysis = Analysis(signals, tuple(response.predictions), response.model)
    return RedirectResponse(f"/analyses/{analyses.add(analysis)}", status_code=303)


def found(analyses: AnalysisStore, identifier: str) -> Analysis:
    analysis = analyses.get(identifier)
    if analysis is None:
        raise HTTPException(404, "This analysis expired; upload the files again.")
    return analysis


@router.get("/analyses/{identifier}", response_class=HTMLResponse)
def show(
    request: Request, analyses: Store, identifier: str, cycle: int = 0
) -> HTMLResponse:
    analysis = found(analyses, identifier)
    cycle = min(max(cycle, 0), analysis.signals.cycles - 1)
    context = {
        "identifier": identifier,
        "analysis": analysis,
        "cycle": cycle,
        "prediction": analysis.predictions[cycle],
        "pressure": figures.Chart.of(analysis.signals.pressure[cycle]),
        "flow": figures.Chart.of(analysis.signals.flow[cycle]),
        "figure": figures,
    }
    return TEMPLATES.TemplateResponse(request, "analysis.html", context)


@router.get("/analyses/{identifier}/predictions.csv")
def download(analyses: Store, identifier: str) -> PlainTextResponse:
    return PlainTextResponse(
        found(analyses, identifier).csv(),
        media_type="text/csv",
        headers={"content-disposition": "attachment; filename=predictions.csv"},
    )


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
