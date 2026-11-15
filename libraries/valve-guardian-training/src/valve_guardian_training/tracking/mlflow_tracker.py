import os
from dataclasses import dataclass
from typing import Final

from valve_guardian_training.tracking.record import RunRecord
from valve_guardian_training.tracking.tracker import Tracker

EXPERIMENT: Final = "valve-guardian"
REGISTERED_MODEL: Final = "valve-guardian"


@dataclass(frozen=True)
class MlflowTracker(Tracker):
    """Needs the `mlflow` extra and MLFLOW_TRACKING_URI; registers the ONNX model."""

    experiment: str = EXPERIMENT

    def record(self, run: RunRecord) -> str:
        os.environ.setdefault("MLFLOW_DISABLE_TELEMETRY", "true")
        import mlflow
        import onnx

        mlflow.set_experiment(self.experiment)
        with mlflow.start_run(run_name=run.name) as active:
            mlflow.log_params(run.parameters)
            mlflow.log_metrics(run.metrics)
            mlflow.log_dict(run.card.model_dump(mode="json"), "model-card.json")
            mlflow.log_text(run.report, "report.md")
            mlflow.onnx.log_model(
                onnx.load(run.artifact / "model.onnx"),
                name="model",
                registered_model_name=REGISTERED_MODEL,
            )
            return f"{mlflow.get_tracking_uri()} run {active.info.run_id}"
