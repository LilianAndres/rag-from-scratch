import asyncio
import time
from typing import Callable

from app.src.core.search.search_query import SearchQuery
from app.src.pipelines.rag_pipeline import RAGPipeline
from eval.domain.eval_sample import EvalSample
from eval.domain.pipeline_output import PipelineOutput


async def _run_single(
    pipeline: RAGPipeline,
    sample: EvalSample,
    top_k: int,
    top_n: int | None,
) -> PipelineOutput:
    query = SearchQuery(text=sample.question, top_k=top_k)
    t0 = time.monotonic()
    result = await pipeline.run(query, top_n=top_n)
    latency_ms = (time.monotonic() - t0) * 1000

    return PipelineOutput(
        sample_id=sample.id,
        question=sample.question,
        answer=result.answer,
        contexts=[source.chunk.content for source in result.sources],
        ground_truth=sample.ground_truth,
        latency_ms=latency_ms,
    )


async def run_pipeline(
    pipeline: RAGPipeline,
    samples: list[EvalSample],
    top_k: int,
    top_n: int | None,
    on_progress: Callable[[int, int], None] | None = None,
) -> list[PipelineOutput]:
    outputs: list[PipelineOutput] = []
    total = len(samples)

    for i, sample in enumerate(samples):
        result = await _run_single(pipeline, sample, top_k, top_n)
        outputs.append(result)
        if on_progress:
            on_progress(i + 1, total)

    return outputs