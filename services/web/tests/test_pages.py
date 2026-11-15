import json
from collections.abc import Iterator

import httpx
import numpy as np
import pytest
from fastapi.testclient import TestClient
from valve_guardian_contract import FLOW_SAMPLES, PRESSURE_SAMPLES
from valve_guardian_web.api import ApiClient
from valve_guardian_web.application import create

CYCLES = 3
CARD = {
    "identifier": "fake",
    "estimator": "fake",
    "features": {"order": 0, "fourier_coefficients": 0},
    "cross_validation": {"f1": {"mean": 1.0, "deviation": 0.0}},
    "holdout": {"f1": 1.0},
    "dataset_sha256": "0",
    "trained_at": "2026-01-01T00:00:00Z",
    "versions": {},
}


def fake_api(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/model":
        return httpx.Response(200, json=CARD)
    cycles = json.loads(request.content)["cycles"]
    predictions = [
        {"optimal": index % 2 == 0, "probability": 0.5} for index in range(len(cycles))
    ]
    return httpx.Response(200, json={"model": "fake", "predictions": predictions})


@pytest.fixture
def web() -> Iterator[TestClient]:
    transport = httpx.MockTransport(fake_api)
    # hardcoded-url: the mock transport answers, nothing is dialled
    http = httpx.Client(transport=transport, base_url="http://api.invalid")
    with TestClient(create(ApiClient(http))) as client:
        yield client


def upload(samples: int) -> bytes:
    rows = np.ones((CYCLES, samples))
    return "\n".join(" ".join(map(str, row)) for row in rows).encode()


def test_an_upload_lands_on_its_analysis(web: TestClient) -> None:
    files = {"pressure": upload(PRESSURE_SAMPLES), "flow": upload(FLOW_SAMPLES)}
    page = web.post("/analyses", files=files)
    assert page.status_code == 200
    rows = web.get(f"{page.url.path}/predictions.csv").text.splitlines()[1:]
    verdicts = [row.split(",")[1] == "True" for row in rows]
    assert verdicts == [index % 2 == 0 for index in range(CYCLES)]


def test_a_misshapen_upload_is_explained(web: TestClient) -> None:
    files = {"pressure": upload(PRESSURE_SAMPLES - 1), "flow": upload(FLOW_SAMPLES)}
    assert "samples per cycle" in web.post("/analyses", files=files).text
