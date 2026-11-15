import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from valve_guardian_training.tracking.record import RunRecord
from valve_guardian_training.tracking.tracker import Tracker


@dataclass(frozen=True)
class LocalTracker(Tracker):
    """One folder per run under `root`: parameters, metrics, report, model."""

    root: Path = Path("runs")

    def record(self, run: RunRecord) -> str:
        stamp = run.card.trained_at.strftime("%Y%m%dT%H%M%SZ")
        folder = self.root / f"{stamp}-{run.card.identifier}"
        shutil.copytree(run.artifact, folder / "model", dirs_exist_ok=True)
        summary = {
            "name": run.name,
            "parameters": run.parameters,
            "metrics": run.metrics,
        }
        (folder / "run.json").write_text(json.dumps(summary, indent=2) + "\n")
        (folder / "report.md").write_text(run.report)
        return str(folder)
