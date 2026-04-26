from pathlib import Path
from eval.domain import EvalRun
from eval.interfaces import Reporter

_W = 72


class ConsoleReporter(Reporter):

    def write(self, run: EvalRun, output_dir: Path | None = None) -> None:
        agg = run.aggregate
        results = run.question_results
        metric_keys = list(agg.keys())

        print(f"\n{'═' * _W}")
        print(f"  Run  : {run.run_id}")
        print(f"  Date : {run.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"  N    : {len(results)} questions")
        print(f"{'═' * _W}")

        # aggregate
        print("\n  AGGREGATE")
        print(f"  {'─' * 44}")
        for metric, score in agg.items():
            bar = _sparkbar(score)
            print(f"  {metric:<28}  {score:.4f}  {bar}")
        avg_lat = sum(r.latency_ms for r in results) / len(results)
        print(f"\n  {'avg latency':<28}  {avg_lat:.0f} ms")

        # by tag
        if run.by_tag:
            print(f"\n  BY TAG")
            print(f"  {'─' * 44}")
            for tag, scores in run.by_tag.items():
                tag_mean = sum(scores.values()) / len(scores)
                print(f"  [{tag}]  mean={tag_mean:.4f}")
                for k, v in scores.items():
                    print(f"    {k:<26}  {v:.4f}")

        # per question
        print(f"\n  PER QUESTION")
        header = f"  {'id':<8}  {'mean':>6}  " + "  ".join(f"{k[:16]:>16}" for k in metric_keys)
        print(header)
        print(f"  {'─' * (len(header) - 2)}")
        for r in results:
            row = f"  {r.sample_id:<8}  {r.mean_score:>6.4f}  "
            row += "  ".join(f"{r.scores.get(k, 0.0):>16.4f}" for k in metric_keys)
            flag = "  ⚠" if r.mean_score < 0.5 else ""
            print(row + flag)

        print(f"\n{'═' * _W}\n")


def _sparkbar(score: float, width: int = 16) -> str:
    filled = round(score * width)
    return f"[{'█' * filled}{'░' * (width - filled)}]"