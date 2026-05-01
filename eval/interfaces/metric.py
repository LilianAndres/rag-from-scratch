from abc import ABC, abstractmethod

from eval.domain.pipeline_output import PipelineOutput


class Metric(ABC):
    """
    A single scoreable criterion.
    Returns a float in [0.0, 1.0] for one PipelineOutput.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def score(self, output: PipelineOutput) -> float:
        pass