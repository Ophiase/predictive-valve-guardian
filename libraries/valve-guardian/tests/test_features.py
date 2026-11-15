import numpy as np
import pytest
from valve_guardian.features import DerivativeOrder, FeatureSpecification, RawSignals

CYCLES = 5
PRESSURE_SAMPLES = 60
FLOW_SAMPLES = 6
COEFFICIENTS = 3


def signals(samples: int) -> np.ndarray:
    return np.random.default_rng(0).normal(size=(CYCLES, samples))


@pytest.mark.parametrize("order", list(DerivativeOrder))
@pytest.mark.parametrize("coefficients", [0, COEFFICIENTS])
def test_columns_follow_the_specification(
    order: DerivativeOrder, coefficients: int
) -> None:
    specification = FeatureSpecification(order, coefficients)
    features = specification.matrix(signals(PRESSURE_SAMPLES), signals(FLOW_SAMPLES))
    assert features.shape == (CYCLES, 2 * specification.columns_per_signal)


def test_settings_round_trip() -> None:
    specification = FeatureSpecification(DerivativeOrder.CURVATURE, COEFFICIENTS)
    assert FeatureSpecification.of(specification.settings) == specification


def test_raw_signals_keep_every_sample() -> None:
    features = RawSignals().matrix(signals(PRESSURE_SAMPLES), signals(FLOW_SAMPLES))
    assert features.shape == (CYCLES, PRESSURE_SAMPLES + FLOW_SAMPLES)


def test_a_constant_signal_has_no_slope() -> None:
    constant = np.ones((CYCLES, PRESSURE_SAMPLES))
    slope = FeatureSpecification(DerivativeOrder.SLOPE).of_signal(constant)
    assert np.allclose(slope[:, -FeatureSpecification().columns_per_signal :], 0)
