from dataclasses import dataclass
from datetime import datetime

from eval.domain.question_result import QuestionResult


@dataclass
class EvalRun:
    """Complete results for one evaluation run."""
    run_id: str
    timestamp: datetime
    config_snapshot: dict
    question_results: list[QuestionResult]

    @property
    def scores_by_metric(self) -> dict[str, float]:
        """Mean of each metric across all questions."""
        if not self.question_results:
            return {}
        keys = self.question_results[0].scores.keys()
        n = len(self.question_results)
        return {
            k: sum(r.scores.get(k, 0.0) for r in self.question_results) / n
            for k in keys
        }