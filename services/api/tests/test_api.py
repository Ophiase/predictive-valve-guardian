from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from valve_guardian_api.application import create
from valve_guardian_api.settings import ApiSettings
from valve_guardian_contract import FLOW_SAMPLES, MAXIMUM_BATCH, PRESSURE_SAMPLES

CYCLES = 3


@pytest.fixture(scope="module")
def api() -> Iterator[TestClient]:
    with TestClient(create(ApiSettings())) as client:
        yield client


def cycle(pressure: int = PRESSURE_SAMPLES) -> dict[str, list[float]]:
    return {"pressure": [150.0] * pressure, "flow": [8.0] * FLOW_SAMPLES}


def test_one_prediction_per_cycle(api: TestClient) -> None:
    response = api.post("/predictions", json={"cycles": [cycle()] * CYCLES})
    assert response.status_code == 200
    assert len(response.json()["predictions"]) == CYCLES
    assert response.json()["model"] == api.get("/model").json()["identifier"]


@pytest.mark.parametrize(
    "cycles",
    [[], [cycle(PRESSURE_SAMPLES - 1)], [cycle()] * (MAXIMUM_BATCH + 1)],
)
def test_a_malformed_request_is_refused(api: TestClient, cycles: list) -> None:
    assert api.post("/predictions", json={"cycles": cycles}).status_code == 422
