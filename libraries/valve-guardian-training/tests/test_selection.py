from valve_guardian.features import FeatureSpecification
from valve_guardian_contract import MetricSummary
from valve_guardian_training.estimators import Candidate
from valve_guardian_training.estimators.catalogue import logistic
from valve_guardian_training.evaluation import Result, Selection

BEST = 0.99
DEVIATION = 0.01


def result(complexity: int, columns: int, mean: float) -> Result:
    candidate = Candidate(str(complexity), complexity, build=logistic)
    summary = MetricSummary(mean=mean, deviation=DEVIATION)
    return Result(FeatureSpecification(), candidate, columns, {"f1": summary})


def test_the_simplest_sufficient_result_wins() -> None:
    best = result(complexity=3, columns=10, mean=BEST)
    close = result(complexity=1, columns=50, mean=BEST - DEVIATION / 2)
    far = result(complexity=1, columns=5, mean=BEST - 2 * DEVIATION)
    assert Selection.simplest([best, close, far]) is close
