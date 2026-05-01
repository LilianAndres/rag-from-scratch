from ragas.metrics.collections import Faithfulness

from eval.domain.pipeline_output import PipelineOutput
from eval.interfaces.metric import Metric

class FaithfulnessMetric(Metric):

    def __init__(self, metric: Faithfulness) -> None:
        self._metric = metric

    @property
    def name(self) -> str:
        return "faithfulness"

    async def score(self, output: PipelineOutput) -> float:
        if not output.contexts:
            return 0.0
        result = await self._metric.ascore(
            user_input=output.question,
            response=output.answer,
            retrieved_contexts=output.contexts,
        )
        return result.value