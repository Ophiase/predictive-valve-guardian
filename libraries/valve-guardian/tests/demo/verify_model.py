from typing import Final

import numpy as np
from valve_guardian.dataset import TRAINING_CYCLES, Cycles, HydraulicArchive
from valve_guardian.model import Predictor

MINIMUM_TEST_ACCURACY: Final = 0.95


def verify_model() -> None:
    cycles = Cycles.load(HydraulicArchive())
    verdicts = Predictor.deployed().optimal_valve(
        cycles.pressure[TRAINING_CYCLES:], cycles.flow[TRAINING_CYCLES:]
    )
    expected = cycles.optimal_valve[TRAINING_CYCLES:].astype(bool)
    accuracy = float(np.mean(np.array(verdicts) == expected))
    print(f"Accuracy on the {len(expected)} test cycles: {accuracy:.3f}")
    assert accuracy >= MINIMUM_TEST_ACCURACY


if __name__ == "__main__":
    verify_model()
