import json
from pathlib import Path


def print_results(results: list[dict]) -> None:
    print("\n" + "=" * 50)
    print("RAGAS Evaluation Results")
    print("=" * 50)
    metric_keys = [k for k in results[0] if k != "question"]
    for key in metric_keys:
        mean = sum(r[key] for r in results) / len(results)
        print(f"  {key:<25} {mean:.4f}")
    print("=" * 50)


def save_results(results: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metric_keys = [k for k in results[0] if k != "question"]
    summary = {
        key: sum(r[key] for r in results) / len(results)
        for key in metric_keys
    }
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to {output_path}")