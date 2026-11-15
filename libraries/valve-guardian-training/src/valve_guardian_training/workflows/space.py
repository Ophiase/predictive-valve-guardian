from itertools import product
from typing import Final

from valve_guardian.features import (
    DerivativeOrder,
    FeatureSpecification,
    RawSignals,
    Representation,
)

FOURIER_COEFFICIENTS: Final = 20

DEPLOYABLE: Final[tuple[FeatureSpecification, ...]] = tuple(
    FeatureSpecification(order, coefficients)
    for order, coefficients in product(DerivativeOrder, (0, FOURIER_COEFFICIENTS))
)
BENCHMARKED: Final[tuple[Representation, ...]] = (RawSignals(), *DEPLOYABLE)
