import asyncio
from datetime import datetime, timezone

from app.config.settings import AppSettings
from app.src.factories.app_factory import ApplicationFactory

from eval.config.settings import EvalSettings
from eval.domain.eval_run import EvalRun
from eval.domain.eval_sample import EvalSample
from eval.factories.evaluator_factory import EvaluatorFactory
from eval.reporters import build_reporters
from eval.runner import run_pipeline
from eval.utils.dateset_loader import load_dataset


def _make_run_id(settings: EvalSettings) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

    provider = settings.judge_llm.provider
    provider_cfg = getattr(settings.judge_llm, provider, None)

    model = getattr(provider_cfg, "model", "unknown")
    model = model.replace(":", "-").replace("/", "-")

    return f"{ts}_{provider}_{model}"


def _config_snapshot(settings: EvalSettings) -> dict:
    provider = settings.judge_llm.provider
    provider_cfg = getattr(settings.judge_llm, provider, None)

    return {
        "dataset": str(settings.dataset_path),
        "top_k": settings.top_k,
        "top_n": settings.top_n,
        "judge_provider": provider,
        "judge_model": getattr(provider_cfg, "model", "?"),
    }


async def run(settings: EvalSettings) -> None:
    run_id = _make_run_id(settings)
    timestamp = datetime.now(timezone.utc)
    run_dir = settings.results_dir / run_id

    print(f"\n{'═' * 60}")
    print(f"  {run_id}")
    print(f"{'═' * 60}")

    samples: list[EvalSample] = load_dataset(settings.dataset_path)
    print(f"  Loaded {len(samples)} samples")

    app_settings = AppSettings()
    pipeline = ApplicationFactory(app_settings).create_rag_pipeline()
    print("  RAG pipeline ready\n")

    def on_progress(done: int, total: int) -> None:
        print(f"  Running pipeline  [{done}/{total}]")

    outputs = await run_pipeline(
        pipeline=pipeline,
        samples=samples,
        top_k=settings.top_k,
        top_n=settings.top_n,
        on_progress=on_progress,
    )

    print("\n  Scoring ...")
    evaluator = EvaluatorFactory(settings).create()
    question_results = await evaluator.evaluate(outputs)

    eval_run = EvalRun(
        run_id=run_id,
        timestamp=timestamp,
        config_snapshot=_config_snapshot(settings),
        question_results=question_results,
    )

    print("\n  Writing reports ...")
    reporters = build_reporters(settings.reporters)
    for reporter in reporters:
        reporter.write(eval_run, run_dir)


def main() -> None:
    asyncio.run(run(EvalSettings()))


if __name__ == "__main__":
    main()