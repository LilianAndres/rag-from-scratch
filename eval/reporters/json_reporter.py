import json
from pathlib import Path
from eval.domain import EvalRun
from eval.interfaces import Reporter


class JsonReporter(Reporter):

    def write(self, run: EvalRun, output_dir: Path | None) -> None:
        if output_dir is None:
            raise ValueError("JsonReporter requires an output_dir.")
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / "results.json"

        payload = {
            "run_id": run.run_id,
            "timestamp": run.timestamp.isoformat(),
            "config": run.config_snapshot,
            "aggregate": {k: round(v, 4) for k, v in run.aggregate.items()},
            "by_tag": {
                tag: {k: round(v, 4) for k, v in scores.items()}
                for tag, scores in run.by_tag.items()
            },
            "questions": [
                {
                    "id": r.sample_id,
                    "question": r.question,
                    "answer": r.answer,
                    "ground_truth": r.ground_truth,
                    "latency_ms": round(r.latency_ms, 1),
                    "tags": r.tags,
                    "mean_score": round(r.mean_score, 4),
                    "scores": {k: round(v, 4) for k, v in r.scores.items()},
                }
                for r in run.question_results
            ],
        }

        with open(path, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"  JSON  → {path}")