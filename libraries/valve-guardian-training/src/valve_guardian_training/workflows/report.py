from collections.abc import Sequence
from typing import Final

from valve_guardian_training.evaluation import Result

TITLE: Final = (
    "# Benchmark\n\n"
    "Repeated stratified 5-fold cross-validation, three repeats, over every cycle;\n"
    "mean ± standard deviation across the 15 folds. Written by `just benchmark`.\n\n"
)
HEADER: Final = (
    "| Representation | Columns | Model | F1 | ROC AUC | Brier | |\n"
    "| --- | --- | --- | --- | --- | --- | --- |\n"
)


class Report:
    @staticmethod
    def markdown(results: Sequence[Result], chosen: Result) -> str:
        ranked = sorted(
            results, key=lambda result: (-result.f1.mean, result.simplicity)
        )
        return (
            TITLE
            + HEADER
            + "".join(Report.row(result, result is chosen) for result in ranked)
        )

    @staticmethod
    def row(result: Result, chosen: bool) -> str:
        scores = result.cross_validation
        cells = (
            result.representation.name,
            str(result.columns),
            result.candidate.name,
            *(
                f"{scores[name].mean:.4f} ± {scores[name].deviation:.4f}"
                for name in ("f1", "roc_auc", "brier")
            ),
            "**deployed**" if chosen else "",
        )
        return "| " + " | ".join(cells) + " |\n"
