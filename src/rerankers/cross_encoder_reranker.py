from sentence_transformers import CrossEncoder

from src.core.interfaces.reranker import BaseReranker
from src.core import SearchResult
from config.models.reranker import CrossEncoderRerankerConfig


class CrossEncoderReranker(BaseReranker):
    """
    Local reranker backed by a sentence-transformers CrossEncoder.
    """

    def __init__(self, config: CrossEncoderRerankerConfig):
        self._config = config
        self._model = CrossEncoder(config.model)

    def rerank(self, query: str, chunks: list[SearchResult], top_n: int | None = None) -> list[SearchResult]:
        if not chunks:
            return []

        pairs = [(query, result.chunk.content) for result in chunks]
        scores: list[float] = self._model.predict(pairs).tolist()

        reranked = sorted(
            [
                SearchResult(chunk=result.chunk, score=score, metadata=result.metadata)
                for result, score in zip(chunks, scores)
            ],
            key=lambda r: r.score,
            reverse=True,
        )

        n = top_n if top_n is not None else self._config.top_n
        return reranked[:n] if n is not None else reranked