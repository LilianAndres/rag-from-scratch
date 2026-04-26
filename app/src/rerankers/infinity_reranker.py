import httpx

from app.config.models.provider import InfinityProviderConfig
from app.src.core.interfaces.reranker import BaseReranker
from app.src.core.search import SearchResult
from app.config.models.reranker import InfinityRerankerConfig


class InfinityReranker(BaseReranker):
    """
    Reranker backed by an Infinity inference server.
    Compatible with any cross-encoder model served by Infinity.
    """

    def __init__(self, config: InfinityRerankerConfig, provider: InfinityProviderConfig):
        self._model = config.model
        self._top_n = config.top_n
        self._timeout = config.timeout
        self._base_url = provider.base_url
        self._api_key = provider.api_key  # None until server is secured

    async def rerank(self, query: str, chunks: list[SearchResult], top_n: int | None = None) -> list[SearchResult]:
        if not chunks:
            return []

        headers = {}
        if self._api_key is not None:
            headers["Authorization"] = f"Bearer {self._api_key.get_secret_value()}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/rerank",
                headers=headers,
                json={
                    "query": query,
                    "documents": [r.chunk.content for r in chunks],
                    "model": self._model,
                },
                timeout=self._timeout,
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

            n = top_n if top_n is not None else self._top_n
            return reranked[:n] if n is not None else reranked