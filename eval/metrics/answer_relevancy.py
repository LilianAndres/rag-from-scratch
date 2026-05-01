from ragas.metrics.collections import AnswerRelevancy

from eval.domain.pipeline_output import PipelineOutput
from eval.interfaces.metric import Metric


class AnswerRelevancyMetric(Metric):

    def __init__(self, metric: AnswerRelevancy) -> None:
        self._metric = metric

    @property
    def name(self) -> str:
        return "answer_relevancy"

    async def score(self, output: PipelineOutput) -> float:
        result = await self._metric.ascore(
            user_input=output.question,
            response=output.answer,
        )
        return result.value