import yaml
from pathlib import Path

from eval.domain.eval_sample import EvalSample


def load_dataset(path: Path) -> list[EvalSample]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    return [
        EvalSample(
            id=item.get("id", f"q{i+1:03d}"),
            question=item["question"],
            ground_truth=item["ground_truth"],
        )
        for i, item in enumerate(data["questions"])
    ]