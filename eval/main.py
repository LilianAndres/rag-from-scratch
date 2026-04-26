import asyncio

from app.config.settings import AppSettings
from app.src.factories.app_factory import ApplicationFactory
from eval.settings import EvalSettings
from eval.ragas_evaluator import RagasEvaluator
from eval.dateset_loader import EvalSample, load_dataset
from eval.eval_reporter import print_results, save_results
from eval.eval_runner import run_pipeline


async def run(settings: EvalSettings) -> None:
    samples: list[EvalSample] = load_dataset(settings.dataset_path)
    print(f"Loaded {len(samples)} evaluation samples.")
    print(f"Judge: {settings.judge.provider} / ", end="")

    app_settings = AppSettings()
    factory = ApplicationFactory(app_settings)
    pipeline = factory.create_rag_pipeline()
    print("RAG pipeline ready.")

    print(f"Running {len(samples)} questions through the pipeline...")
    outputs = []
    for i, sample in enumerate(samples, 1):
        print(f"  [{i}/{len(samples)}] {sample.question[:60]}...")
        output = await run_pipeline(
            pipeline=pipeline,
            question=sample.question,
            ground_truth=sample.ground_truth,
            top_k=settings.top_k,
            top_n=settings.top_n,
        )
        outputs.append(output)

    print("\nRunning RAGAS evaluation...")
    evaluator = RagasEvaluator(settings)
    results = await evaluator.evaluate(outputs)

    print_results(results)
    save_results(results, settings.output_path)


def main() -> None:
    settings = EvalSettings()
    asyncio.run(run(settings))


if __name__ == "__main__":
    main()