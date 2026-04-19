import asyncio
from collections import defaultdict
from src.core.interfaces.backend import SearchBackend
from src.core.interfaces.reranker import BaseReranker
from src.core.domain.chunk import Chunk
from src.core.search.query import SearchQuery
from src.core.search.result import SearchResult


class HybridBackend(SearchBackend):
    """
    Composes any number of SearchBackend instances.
    Merges results via Reciprocal Rank Fusion; no alpha tuning needed.
    Optionally reranks the merged list.
    """

    def __init__(
        self,
        backends: list[SearchBackend],
        reranker: BaseReranker | None = None,
        rrf_k: int = 60,
    ) -> None:
        if len(backends) < 2:
            raise ValueError("HybridBackend requires at least two backends.")
        self._backends = backends
        self._reranker = reranker
        self._rrf_k = rrf_k

    async def index(self, chunks: list[Chunk]) -> None:
        await asyncio.gather(*[b.index(chunks) for b in self._backends])

    async def search(self, query: SearchQuery) -> list[SearchResult]:
        all_results: list[list[SearchResult]] = await asyncio.gather(
            *[b.search(query) for b in self._backends]
        )
        merged = self._rrf_merge(all_results, query.top_k)

        if self._reranker:
            return await self._reranker.rerank(merged, query)
        return merged

    async def delete(self, document_id: str) -> None:
        await asyncio.gather(*[b.delete(document_id) for b in self._backends])

    def _rrf_merge(
        self,
        all_results: list[list[SearchResult]],
        top_k: int,
    ) -> list[SearchResult]:
        scores: dict[str, float] = defaultdict(float)
        result_map: dict[str, SearchResult] = {}

        for results in all_results:
            for rank, result in enumerate(results):
                key = result.chunk.id
                scores[key] += 1.0 / (self._rrf_k + rank + 1)
                result_map[key] = result

        ranked = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
        return [
            SearchResult(
                chunk=result_map[k].chunk,
                score=scores[k],
                metadata=result_map[k].metadata,
            )
            for k in ranked[:top_k]
        ]