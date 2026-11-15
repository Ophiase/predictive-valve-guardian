from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Final
from uuid import uuid4

from valve_guardian_web.analysis.analysis import Analysis

CAPACITY: Final = 3


@dataclass
class AnalysisStore:
    """The latest analyses in memory; the oldest is dropped past `capacity`."""

    capacity: int = CAPACITY
    analyses: OrderedDict[str, Analysis] = field(default_factory=OrderedDict)

    def add(self, analysis: Analysis) -> str:
        identifier = uuid4().hex
        self.analyses[identifier] = analysis
        while len(self.analyses) > self.capacity:
            self.analyses.popitem(last=False)
        return identifier

    def get(self, identifier: str) -> Analysis | None:
        return self.analyses.get(identifier)
