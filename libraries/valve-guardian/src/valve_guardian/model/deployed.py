from pathlib import Path
from typing import Final

from xgboost import XGBClassifier

from valve_guardian.features import FeatureSpecification

DEPLOYED_FEATURES: Final = FeatureSpecification(fourier=True)
DEPLOYED_MODEL: Final = Path(__file__).parent / "cached" / "model.ubj"
TRAINING_SEED: Final = 392
TREES: Final = 200


class DeployedModel:
    @staticmethod
    def untrained() -> XGBClassifier:
        return XGBClassifier(
            n_estimators=TREES,
            eval_metric="logloss",
            random_state=TRAINING_SEED,
        )

    @staticmethod
    def load(path: Path = DEPLOYED_MODEL) -> XGBClassifier:
        model = XGBClassifier()
        model.load_model(path)
        return model

    @staticmethod
    def save(model: XGBClassifier, path: Path = DEPLOYED_MODEL) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        model.save_model(path)
