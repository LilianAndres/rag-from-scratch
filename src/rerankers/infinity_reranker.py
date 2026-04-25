import httpx

from src.core.interfaces.reranker import BaseReranker
from src.core.search import SearchResult
from config.models.reranker import InfinityRerankerConfig


class InfinityReranker(BaseReranker):
    """
    Reranker backed by an Infinity inference server.
    Compatible with any cross-encoder model served by Infinity.
    """

    def __init__(self, config: InfinityRerankerConfig):
        self._config = config

    def rerank(self, query: str, chunks: list[SearchResult], top_n: int | None = None) -> list[SearchResult]:
        if not chunks:
            return []

        response = httpx.post(
            f"{self._config.base_url}/rerank",
            json={
                "query": query,
                "documents": [r.chunk.content for r in chunks],
                "model": self._config.model,
            },
            timeout=self._config.timeout,
        )
        response.raise_for_status()
        data = response.json()

        reranked = sorted(
            [
                SearchResult(
                    chunk=chunks[item["index"]].chunk,
                    score=item["relevance_score"],
                    metadata=chunks[item["index"]].metadata,
                )
                for item in data["results"]
            ],
            key=lambda r: r.score,
            reverse=True,
        )

        n = top_n if top_n is not None else self._config.top_n
        return reranked[:n] if n is not None else reranked