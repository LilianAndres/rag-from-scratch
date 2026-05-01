from ragas.metrics.collections import ContextRecall

from eval.domain.pipeline_output import PipelineOutput
from eval.interfaces.metric import Metric


class ContextRecallMetric(Metric):

    def __init__(self, metric: ContextRecall) -> None:
        self._metric = metric

    @property
    def name(self) -> str:
        return "context_recall"

    async def score(self, output: PipelineOutput) -> float:
        if not output.contexts:
            return 0.0
        result = await self._metric.ascore(
            user_input=output.question,
            retrieved_contexts=output.contexts,
            reference=output.ground_truth,
        )
        return result.value