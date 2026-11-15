import logging

from valve_guardian.dataset import Cycles, HydraulicArchive, Split
from valve_guardian.model import DEPLOYED_FEATURES, DeployedModel

logger = logging.getLogger(__name__)


def train() -> None:
    cycles = Cycles.load(HydraulicArchive())
    features = DEPLOYED_FEATURES.matrix(cycles.pressure, cycles.flow)
    split = Split.chronological(features, cycles.optimal_valve)
    model = DeployedModel.untrained()
    model.fit(split.training_features, split.training_labels)
    DeployedModel.save(model)
    logger.info("Model saved")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train()
