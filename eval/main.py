import asyncio
from datetime import datetime, timezone

from app.config.settings import AppSettings
from app.src.factories.app_factory import ApplicationFactory
from eval.reporters import build_reporters
from eval.utils.dateset_loader import load_dataset

from eval.domain import EvalRun, EvalSample
from eval.config.settings import EvalSettings
from eval.evaluators import build_ragas_evaluator, BaseEvaluator
from eval.metrics import LatencyMetric
from eval.runner import run_pipeline_batch


def _make_run_id(settings: EvalSettings) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    provider = settings.judge.provider
    judge_cfg = getattr(settings.judge, provider, None)
    model = getattr(judge_cfg, "model", "unknown").replace(":", "-").replace("/", "-")
    return f"{ts}_{provider}_{model}"


def _config_snapshot(settings: EvalSettings) -> dict:
    provider = settings.judge.provider
    judge_cfg = getattr(settings.judge, provider, None)
    return {
        "dataset": str(settings.dataset_path),
        "top_k": settings.top_k,
        "top_n": settings.top_n,
        "batch_size": settings.batch_size,
        "judge_provider": provider,
        "judge_model": getattr(judge_cfg, "model", "?"),
    }


def _build_evaluator(settings: EvalSettings) -> BaseEvaluator:
    evaluator = build_ragas_evaluator(settings)
    evaluator.add_metrics([
        LatencyMetric(threshold_ms=2000.0),
    ])
    return evaluator


async def run(settings: EvalSettings) -> None:
    run_id = _make_run_id(settings)
    timestamp = datetime.now(timezone.utc)
    run_dir = settings.results_dir / run_id

    print(f"\n{'═' * 60}")
    print(f"  {run_id}")
    print(f"{'═' * 60}")

    # Load the dataset
    samples: list[EvalSample] = load_dataset(settings.dataset_path)
    samples_by_id = {s.id: s for s in samples}
    print(f"  Loaded {len(samples)} samples")

    # Build the pipeline
    pipeline = ApplicationFactory(AppSettings()).create_rag_pipeline()
    print("  RAG pipeline ready")

    # Run pipeline in concurrent batches
    print(f"\n  Running pipeline  [batch_size={settings.batch_size}]")

    def on_progress(done: int, total: int) -> None:
        print(f"    {done}/{total}")

    outputs = await run_pipeline_batch(
        pipeline=pipeline,
        samples=samples,
        top_k=settings.top_k,
        top_n=settings.top_n,
        batch_size=settings.batch_size,
        on_progress=on_progress,
    )

    # Scoring
    print("\n  Scoring ...")
    evaluator = _build_evaluator(settings)
    question_results = await evaluator.evaluate(outputs, samples_by_id)

    # Assemble run
    eval_run = EvalRun(
        run_id=run_id,
        timestamp=timestamp,
        config_snapshot=_config_snapshot(settings),
        question_results=question_results,
    )

    # Report run
    print("\n  Writing reports ...")
    reporters = build_reporters(settings.reporters)
    for reporter in reporters:
        reporter.write(eval_run, run_dir)


def main() -> None:
    asyncio.run(run(EvalSettings()))

if __name__ == "__main__":
    main()