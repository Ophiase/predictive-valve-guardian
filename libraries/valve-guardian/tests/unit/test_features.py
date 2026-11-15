import numpy as np
import pytest
from valve_guardian.features import DerivativeOrder, FeatureSpecification, RawSignals

CYCLES = 5
PRESSURE_SAMPLES = 60
FLOW_SAMPLES = 6


def signals(samples: int) -> np.ndarray:
    return np.random.default_rng(0).normal(size=(CYCLES, samples))


@pytest.mark.parametrize("order", list(DerivativeOrder))
@pytest.mark.parametrize("fourier", [False, True])
def test_columns_follow_the_specification(
    order: DerivativeOrder, fourier: bool
) -> None:
    specification = FeatureSpecification(
        order=order, fourier=fourier, fourier_coefficients=3
    )
    features = specification.matrix(signals(PRESSURE_SAMPLES), signals(FLOW_SAMPLES))
    assert features.shape == (CYCLES, 2 * specification.columns_per_signal)


def test_raw_signals_keep_every_sample() -> None:
    features = RawSignals().matrix(signals(PRESSURE_SAMPLES), signals(FLOW_SAMPLES))
    assert features.shape == (CYCLES, PRESSURE_SAMPLES + FLOW_SAMPLES)


def test_a_constant_signal_has_no_slope() -> None:
    constant = np.ones((CYCLES, PRESSURE_SAMPLES))
    slope = FeatureSpecification(order=DerivativeOrder.SLOPE).of_signal(constant)
    assert np.allclose(slope[:, -FeatureSpecification().columns_per_signal :], 0)
