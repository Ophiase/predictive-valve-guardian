import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from valve_guardian.arrays import FeatureMatrix, Labels
from valve_guardian_contract import MetricSummary

from valve_guardian_training.evaluation.scoring import (
    FOLDS,
    NEGATED,
    REPEATS,
    SCORERS,
    SEED,
)


class CrossValidation:
    """Repeated stratified k-fold; stateless features leak nothing across folds."""

    @staticmethod
    def summary(
        pipeline: Pipeline, features: FeatureMatrix, labels: Labels
    ) -> dict[str, MetricSummary]:
        folds = RepeatedStratifiedKFold(
            n_splits=FOLDS, n_repeats=REPEATS, random_state=SEED
        )
        scores = cross_validate(
            pipeline, features, labels, cv=folds, scoring=dict(SCORERS), n_jobs=-1
        )
        return {
            name: CrossValidation.summarize(scores[f"test_{name}"], name in NEGATED)
            for name in SCORERS
        }

    @staticmethod
    def summarize(values: np.ndarray, negated: bool) -> MetricSummary:
        signed = -values if negated else values
        return MetricSummary(mean=float(signed.mean()), deviation=float(signed.std()))
