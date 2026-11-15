import argparse
import logging
import os
from pathlib import Path

from valve_guardian.inference import ModelArtifact

from valve_guardian_training.dataset import Cycles, HydraulicArchive
from valve_guardian_training.evaluation import Selection
from valve_guardian_training.tracking import LocalTracker, MlflowTracker, Tracker
from valve_guardian_training.workflows.benchmark import Benchmark
from valve_guardian_training.workflows.report import Report
from valve_guardian_training.workflows.space import BENCHMARKED
from valve_guardian_training.workflows.trainer import Trainer

logger = logging.getLogger("valve_guardian_training")


def tracker(name: str) -> Tracker:
    return MlflowTracker() if name == "mlflow" else LocalTracker()


def benchmark(arguments: argparse.Namespace) -> None:
    results = Benchmark.run(Cycles.load(HydraulicArchive()), BENCHMARKED)
    arguments.output.write_text(Report.markdown(results, Selection.simplest(results)))
    logger.info("Benchmark written to %s", arguments.output)


def train(arguments: argparse.Namespace) -> None:
    run = Trainer.train(HydraulicArchive(), ModelArtifact(arguments.artifact))
    logger.info("Deployed %s: %s", run.card.identifier, run.name)
    logger.info("Tracked at %s", tracker(arguments.tracker).record(run))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="valve-guardian-training")
    commands = root.add_subparsers(required=True)
    commands.add_parser("data", help="download the UCI dataset").set_defaults(
        action=lambda _: HydraulicArchive().ensure()
    )
    bench = commands.add_parser("benchmark", help="every model on every representation")
    bench.add_argument("--output", type=Path, default=Path("docs/benchmark.md"))
    bench.set_defaults(action=benchmark)
    fit = commands.add_parser("train", help="select, fit, export and track the model")
    fit.add_argument("--artifact", type=Path, default=ModelArtifact().directory)
    fit.add_argument(
        "--tracker",
        choices=("local", "mlflow"),
        default="mlflow" if os.environ.get("MLFLOW_TRACKING_URI") else "local",
    )
    fit.set_defaults(action=train)
    return root


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    arguments = parser().parse_args()
    arguments.action(arguments)
