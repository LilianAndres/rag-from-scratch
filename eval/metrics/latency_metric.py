from eval.domain import PipelineOutput
from eval.interfaces import Metric


class LatencyMetric(Metric):
    """
    Soft score: 1.0 at or below threshold, decays linearly to 0.0 at 2× threshold.
    Useful as a CI gate — a regression in retrieval speed shows up here immediately.
    """

    def __init__(self, threshold_ms: float = 2000.0) -> None:
        self._threshold = threshold_ms

    @property
    def name(self) -> str:
        return "latency_score"

    async def score(self, output: PipelineOutput) -> float:
        return max(0.0, 1.0 - output.latency_ms / (self._threshold * 2))