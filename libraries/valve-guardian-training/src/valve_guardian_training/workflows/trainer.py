from datetime import UTC, datetime
from hashlib import sha256
from importlib.metadata import version
from typing import Final

from valve_guardian.features import FeatureSpecification
from valve_guardian.inference import ModelArtifact
from valve_guardian_contract import ModelCard

from valve_guardian_training.dataset import Cycles, HydraulicArchive, Split
from valve_guardian_training.estimators import OnnxExport
from valve_guardian_training.evaluation import Holdout, Result, Selection
from valve_guardian_training.tracking import RunRecord
from valve_guardian_training.workflows.benchmark import Benchmark
from valve_guardian_training.workflows.report import Report
from valve_guardian_training.workflows.space import DEPLOYABLE

LIBRARIES: Final = ("numpy", "scikit-learn", "xgboost-cpu", "skl2onnx", "onnxruntime")


class Trainer:
    """Select the simplest sufficient model, fit it on every cycle and export it."""

    @staticmethod
    def train(archive: HydraulicArchive, artifact: ModelArtifact) -> RunRecord:
        cycles = Cycles.load(archive)
        results = Benchmark.run(cycles, DEPLOYABLE)
        chosen = Selection.simplest(results)
        specification = chosen.representation
        if not isinstance(specification, FeatureSpecification):
            raise TypeError("only a feature specification can be served")
        features = specification.matrix(cycles.pressure, cycles.flow)
        holdout = Holdout.scores(
            chosen.candidate.pipeline(),
            Split.chronological(features, cycles.optimal_valve),
        )
        pipeline = chosen.candidate.pipeline().fit(features, cycles.optimal_valve)
        model = OnnxExport.of(pipeline, features)
        card = Trainer.card(
            chosen, specification, model, holdout, archive.fingerprint()
        )
        artifact.write(model, card)
        return Trainer.record(chosen, card, artifact, Report.markdown(results, chosen))

    @staticmethod
    def card(
        chosen: Result,
        specification: FeatureSpecification,
        model: bytes,
        holdout: dict[str, float],
        dataset: str,
    ) -> ModelCard:
        return ModelCard(
            identifier=sha256(model).hexdigest()[:12],
            estimator=chosen.candidate.name,
            features=specification.settings,
            cross_validation=chosen.cross_validation,
            holdout=holdout,
            dataset_sha256=dataset,
            trained_at=datetime.now(UTC),
            versions={library: version(library) for library in LIBRARIES},
        )

    @staticmethod
    def record(
        chosen: Result, card: ModelCard, artifact: ModelArtifact, report: str
    ) -> RunRecord:
        metrics = {
            f"cv_{name}": score.mean for name, score in card.cross_validation.items()
        }
        metrics |= {f"holdout_{name}": score for name, score in card.holdout.items()}
        return RunRecord(
            name=f"{chosen.candidate.name}, {chosen.representation.name}",
            parameters={
                "estimator": card.estimator,
                "order": card.features.order,
                "fourier_coefficients": card.features.fourier_coefficients,
                "dataset_sha256": card.dataset_sha256,
            },
            metrics=metrics,
            card=card,
            artifact=artifact.directory,
            report=report,
        )
