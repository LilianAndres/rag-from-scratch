import csv
from pathlib import Path
from eval.domain import EvalRun
from eval.interfaces import Reporter


class CsvReporter(Reporter):

    def write(self, run: EvalRun, output_dir: Path | None) -> None:
        if output_dir is None:
            raise ValueError("CsvReporter requires an output_dir.")
        if not run.question_results:
            return
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "results.csv"

        metric_keys = list(run.question_results[0].scores.keys())
        fieldnames = ["id", "question", "tags", "latency_ms", "mean_score"] + metric_keys

        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in run.question_results:
                writer.writerow({
                    "id": r.sample_id,
                    "question": r.question[:100],
                    "tags": "|".join(r.tags),
                    "latency_ms": round(r.latency_ms, 1),
                    "mean_score": round(r.mean_score, 4),
                    **{k: round(v, 4) for k, v in r.scores.items()},
                })
        print(f"  CSV   → {path}")