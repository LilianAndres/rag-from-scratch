from eval.domain.pipeline_output import PipelineOutput
from eval.domain.question_result import QuestionResult
from eval.interfaces.evaluator import Evaluator
from eval.interfaces.metric import Metric


class BaseEvaluator(Evaluator):
    """
    Generic evaluator: runs every Metric against every PipelineOutput.
    Works with any combination of metrics: RAGAS, builtin, or custom.
    """

    def __init__(self, metrics: list[Metric]) -> None:
        if not metrics:
            raise ValueError("At least one metric is required.")
        self._metrics = metrics

    @property
    def metrics(self):
        return self._metrics

    @property
    def metric_names(self) -> list[str]:
        return [m.name for m in self._metrics]

    def add_metrics(self, metrics: list[Metric]) -> None:
        self._metrics.extend(metrics)

    async def evaluate(self, outputs: list[PipelineOutput]) -> list[QuestionResult]:
        results = []
        for output in outputs:
            scores: dict[str, float] = {}
            for metric in self._metrics:
                scores[metric.name] = await metric.score(output)

            results.append(QuestionResult(
                sample_id=output.sample_id,
                question=output.question,
                answer=output.answer,
                ground_truth=output.ground_truth,
                contexts=output.contexts,
                latency_ms=output.latency_ms,
                scores=scores,
            ))
        return results