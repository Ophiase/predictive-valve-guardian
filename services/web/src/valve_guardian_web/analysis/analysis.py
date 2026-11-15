from dataclasses import dataclass

from valve_guardian_contract import Prediction

from valve_guardian_web.analysis.signals import UploadedSignals


@dataclass(frozen=True)
class Analysis:
    signals: UploadedSignals
    predictions: tuple[Prediction, ...]
    model: str

    @property
    def optimal(self) -> int:
        return sum(prediction.optimal for prediction in self.predictions)

    def csv(self) -> str:
        rows = (
            f"{cycle},{prediction.optimal},{prediction.probability:.6f}"
            for cycle, prediction in enumerate(self.predictions)
        )
        return "cycle,valve_optimal,probability\n" + "\n".join(rows) + "\n"
