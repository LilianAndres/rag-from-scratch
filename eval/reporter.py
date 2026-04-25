import json
from pathlib import Path

from ragas import EvaluationResult


def print_results(results: EvaluationResult) -> None:
    print("\n" + "=" * 50)
    print("RAGAS Evaluation Results")
    print("=" * 50)
    df = results.to_pandas()
    for metric in df.columns:
        if metric not in ("question", "answer", "contexts", "ground_truth"):
            mean = df[metric].mean()
            print(f"  {metric:<25} {mean:.4f}")
    print("=" * 50)


def save_results(results: EvaluationResult, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = results.to_pandas()
    summary = {
        col: float(df[col].mean())
        for col in df.columns
        if col not in ("question", "answer", "contexts", "ground_truth")
    }
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to {output_path}")