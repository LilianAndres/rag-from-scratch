from abc import ABC, abstractmethod

from eval.domain.eval_sample import EvalSample
from eval.domain.pipeline_output import PipelineOutput
from eval.domain.question_result import QuestionResult


class Evaluator(ABC):
    """
    Scores a batch of PipelineOutputs and returns one QuestionResult per output.
    """

    @abstractmethod
    async def evaluate(self, outputs: list[PipelineOutput]) -> list[QuestionResult]:
        pass