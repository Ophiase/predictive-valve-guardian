from typing import Final

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from valve_guardian_training.estimators.candidate import Candidate

SEED: Final = 42
TREES: Final = 200
LOGISTIC_ITERATIONS: Final = 2_000


def logistic() -> Pipeline:
    return make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=LOGISTIC_ITERATIONS)
    )


def forest() -> Pipeline:
    return make_pipeline(RandomForestClassifier(n_estimators=TREES, random_state=SEED))


def boosting() -> Pipeline:
    return make_pipeline(XGBClassifier(n_estimators=TREES, random_state=SEED))


CANDIDATES: Final[tuple[Candidate, ...]] = (
    Candidate("logistic regression", complexity=1, build=logistic),
    Candidate("random forest", complexity=2, build=forest),
    Candidate("xgboost", complexity=3, build=boosting),
)
