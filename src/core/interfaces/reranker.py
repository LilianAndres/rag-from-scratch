from abc import ABC, abstractmethod

from src.core import SearchResult


class BaseReranker(ABC):
    """
    Abstract base class for rerankers.

    A reranker takes a query and an initial candidate list produced by a
    SearchBackend and returns a re-scored, re-ordered list that is better
    calibrated to the query's intent.
    """

    @abstractmethod
    def rerank(self, query: str, chunks: list[SearchResult], top_n: int | None = None) -> list[SearchResult]:
        """
        Re-score and re-order *chunks* with respect to *query*.

        Parameters
        ----------
        query:
            The user's natural-language question.
        chunks:
            Candidate chunks from a retriever (order does not matter).
        top_n:
            If provided, return only the *top_n* highest-scoring chunks.
            When None all input chunks are returned (re-ordered).

        Returns
        -------
        list[SearchResult]
            Chunks sorted by descending reranker score. chunk.score
            should be updated to reflect the new score.
        """