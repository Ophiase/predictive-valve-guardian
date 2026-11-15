import numpy as np
from valve_guardian.dataset import Split

CYCLES = 10
TRAINING = CYCLES - 3


def test_the_split_is_chronological() -> None:
    features = np.arange(CYCLES, dtype=np.float64).reshape(-1, 1)
    split = Split.chronological(features, np.arange(CYCLES), training_cycles=TRAINING)
    assert split.training_features[-1, 0] < split.test_features[0, 0]
    assert len(split.training_labels) + len(split.test_labels) == CYCLES
