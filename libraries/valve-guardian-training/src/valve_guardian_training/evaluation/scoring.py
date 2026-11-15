from types import MappingProxyType
from typing import Final

SCORERS: Final = MappingProxyType({
    "accuracy": "accuracy",
    "f1": "f1",
    "roc_auc": "roc_auc",
    "brier": "neg_brier_score",
})
NEGATED: Final = frozenset({"brier"})
FOLDS: Final = 5
REPEATS: Final = 3
SEED: Final = 7
