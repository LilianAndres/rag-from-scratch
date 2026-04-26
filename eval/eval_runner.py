from dataclasses import dataclass

from app.src.core.search.search_query import SearchQuery
from app.src.pipelines.rag_pipeline import RAGPipeline


@dataclass
class PipelineOutput:
    question: str
    answer: str
    contexts: list[str]
    ground_truth: str


async def run_pipeline(
    pipeline: RAGPipeline,
    question: str,
    ground_truth: str,
    top_k: int = 5,
    top_n: int | None = None,
) -> PipelineOutput:
    query = SearchQuery(text=question, top_k=top_k)
    result = await pipeline.run(query, top_n=top_n)

    contexts = [source.chunk.content for source in result.sources]

    return PipelineOutput(
        question=question,
        answer=result.answer,
        contexts=contexts,
        ground_truth=ground_truth,
    )