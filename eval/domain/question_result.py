from dataclasses import dataclass


@dataclass
class QuestionResult:
    sample_id: str
    question: str
    answer: str
    ground_truth: str
    contexts: list[str]
    latency_ms: float
    scores: dict[str, float]

    @property
    def mean_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)