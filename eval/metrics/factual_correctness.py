from ragas.metrics.collections import FactualCorrectness
from eval.domain import PipelineOutput
from eval.interfaces.metric import Metric


class FactualCorrectnessMetric(Metric):

    def __init__(self, metric: FactualCorrectness) -> None:
        self._metric = metric

    @property
    def name(self) -> str:
        return "factual_correctness"

    async def score(self, output: PipelineOutput) -> float:
        result = await self._metric.ascore(
            response=output.answer,
            reference=output.ground_truth,
        )
        return result.value