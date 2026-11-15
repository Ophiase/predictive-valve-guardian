from collections.abc import Sequence

from valve_guardian_training.evaluation.result import Result


class Selection:
    @staticmethod
    def simplest(results: Sequence[Result]) -> Result:
        """The simplest result whose mean F1 is within one deviation of the best one."""
        best = max(results, key=lambda result: result.f1.mean)
        floor = best.f1.mean - best.f1.deviation
        eligible = [result for result in results if result.f1.mean >= floor]
        return min(eligible, key=lambda result: result.simplicity)
