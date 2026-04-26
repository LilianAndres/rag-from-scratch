from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class EvalSample:
    question: str
    ground_truth: str


def load_dataset(path: Path) -> list[EvalSample]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    return [
        EvalSample(
            question=item["question"],
            ground_truth=item["ground_truth"],
        )
        for item in data["questions"]
    ]