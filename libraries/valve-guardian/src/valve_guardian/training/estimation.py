import logging
import time
from collections.abc import Iterator
from dataclasses import asdict
from typing import Final

import pandas as pd

from valve_guardian.dataset import Cycles, HydraulicArchive, Split
from valve_guardian.features import Representation
from valve_guardian.training.candidates import REPRESENTATIONS, Candidates
from valve_guardian.training.measure import Measure

RANKING: Final = ["f1", "accuracy", "prediction_seconds"]
DESCENDING: Final = [False, False, True]


class Benchmark:
    """Every candidate model on every representation, best first."""

    @classmethod
    def table(cls, cycles: Cycles) -> pd.DataFrame:
        rows = [row for each in REPRESENTATIONS for row in cls.rows(cycles, each)]
        return pd.DataFrame(rows).sort_values(by=RANKING, ascending=DESCENDING)

    @staticmethod
    def rows(
        cycles: Cycles, representation: Representation
    ) -> Iterator[dict[str, object]]:
        start = time.perf_counter()
        features = representation.matrix(cycles.pressure, cycles.flow)
        feature_seconds = time.perf_counter() - start
        split = Split.chronological(features, cycles.optimal_valve)
        for name, model in Candidates.models().items():
            yield {
                "representation": representation.name,
                "model": name,
                "feature_seconds": feature_seconds,
                **asdict(Measure.of(model, split)),
            }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(Benchmark.table(Cycles.load(HydraulicArchive())).to_string(index=False))
