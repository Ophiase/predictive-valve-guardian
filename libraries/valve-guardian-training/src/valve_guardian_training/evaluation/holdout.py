from sklearn.metrics import accuracy_score, brier_score_loss, f1_score, roc_auc_score
from sklearn.pipeline import Pipeline

from valve_guardian_training.dataset import Split


class Holdout:
    """Trained on the first cycles, scored on the last, in recording order."""

    @staticmethod
    def scores(pipeline: Pipeline, split: Split) -> dict[str, float]:
        pipeline.fit(split.training_features, split.training_labels)
        labels = pipeline.predict(split.test_features)
        probabilities = pipeline.predict_proba(split.test_features)[:, 1]
        return {
            "accuracy": float(accuracy_score(split.test_labels, labels)),
            "f1": float(f1_score(split.test_labels, labels)),
            "roc_auc": float(roc_auc_score(split.test_labels, probabilities)),
            "brier": float(brier_score_loss(split.test_labels, probabilities)),
        }
