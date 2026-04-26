from abc import ABC, abstractmethod

from eval.domain import PipelineOutput, EvalSample, QuestionResult


class Evaluator(ABC):
    """
    Scores a batch of PipelineOutputs and returns one QuestionResult per output.
    Owns the mapping from raw outputs back to EvalSamples (for tags, metadata).
    """

    @abstractmethod
    async def evaluate(self, outputs: list[PipelineOutput], samples: dict[str, EvalSample]) -> list[QuestionResult]:
        pass