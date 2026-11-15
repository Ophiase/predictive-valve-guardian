from abc import ABC, abstractmethod

from valve_guardian.arrays import FeatureMatrix, Signals


class Representation(ABC):
    @abstractmethod
    def matrix(self, pressure: Signals, flow: Signals) -> FeatureMatrix: ...

    @property
    @abstractmethod
    def name(self) -> str: ...
