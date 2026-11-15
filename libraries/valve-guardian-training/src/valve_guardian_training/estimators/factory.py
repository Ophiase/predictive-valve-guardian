from typing import Protocol

from sklearn.pipeline import Pipeline


class PipelineFactory(Protocol):
    def __call__(self) -> Pipeline: ...
