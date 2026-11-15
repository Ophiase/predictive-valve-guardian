from types import MappingProxyType
from typing import Final

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from valve_guardian.features import (
    DerivativeOrder,
    FeatureSpecification,
    RawSignals,
    Representation,
)
from valve_guardian.model import Classifier

SEED: Final = 42
TREES: Final = 200
LOGISTIC_ITERATIONS: Final = 1_000

REPRESENTATIONS: Final[tuple[Representation, ...]] = (
    RawSignals(),
    FeatureSpecification(order=DerivativeOrder.SLOPE),
    FeatureSpecification(order=DerivativeOrder.CURVATURE),
    FeatureSpecification(fourier=True),
    FeatureSpecification(order=DerivativeOrder.CURVATURE, fourier=True),
)


class Candidates:
    @staticmethod
    def models() -> MappingProxyType[str, Classifier]:
        """Fresh, unfitted models, by name."""
        return MappingProxyType({
            "LogisticRegression": LogisticRegression(max_iter=LOGISTIC_ITERATIONS),
            "RandomForest": RandomForestClassifier(
                n_estimators=TREES, random_state=SEED
            ),
            "XGBoost": XGBClassifier(
                n_estimators=TREES, eval_metric="logloss", random_state=SEED
            ),
        })
