from dataclasses import dataclass, field


@dataclass
class EvalSample:
    id: str
    question: str
    ground_truth: str