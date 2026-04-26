from dataclasses import dataclass


@dataclass
class PipelineOutput:
    sample_id: str
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str
    latency_ms: float