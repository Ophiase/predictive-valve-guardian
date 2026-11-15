from abc import ABC, abstractmethod

from valve_guardian_training.tracking.record import RunRecord


class Tracker(ABC):
    @abstractmethod
    def record(self, run: RunRecord) -> str:
        """Store the run; returns where it can be found."""
