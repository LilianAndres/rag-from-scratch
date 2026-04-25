import asyncio
from collections import defaultdict

from app.src.core.interfaces.backend import SearchBackend
from app.src.core.domain.chunk import Chunk
from app.src.core.search.search_query import SearchQuery
from app.src.core.search.search_result import SearchResult


class HybridBackend(SearchBackend):
    """
    Hybrid backend combining multiple backends using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self, backends: list[SearchBackend], rrf_k: int = 60) -> None:
        if len(backends) < 2:
            raise ValueError("HybridBackend requires at least two backends.")

        self._backends = backends
        self._rrf_k = rrf_k

    async def index(self, chunks: list[Chunk]) -> None:
        await asyncio.gather(*(b.index(chunks) for b in self._backends))

    async def search(self, query: SearchQuery) -> list[SearchResult]:
        all_results: list[list[SearchResult]] = list(await asyncio.gather(
            *(b.search(query) for b in self._backends)
        ))

        return self._rrf_merge(all_results, query.top_k)

    async def delete(self, document_id: str) -> None:
        await asyncio.gather(*(b.delete(document_id) for b in self._backends))

    def _rrf_merge(self, all_results: list[list[SearchResult]], top_k: int) -> list[SearchResult]:
        scores: dict[str, float] = defaultdict(float)
        result_map: dict[str, SearchResult] = {}

        for results in all_results:
            for rank, result in enumerate(results):
                chunk_id = result.chunk.id

                scores[chunk_id] += 1.0 / (self._rrf_k + rank + 1)

                # keep best scoring source result
                if chunk_id not in result_map or result.score > result_map[chunk_id].score:
                    result_map[chunk_id] = result

        ranked_ids = sorted( scores.keys(), key=lambda k: scores[k], reverse=True)

        return [
            SearchResult(
                chunk=result_map[cid].chunk,
                score=scores[cid],
                metadata=result_map[cid].metadata,
            )
            for cid in ranked_ids[:top_k]
        ]