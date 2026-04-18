from src.core.interfaces.retriever import BaseRetriever
from src.core.retrieval.result import RetrievedChunk
from config.models.retriever import HybridRetrieverConfig


class HybridRetriever(BaseRetriever):
    """
    Hybrid retriever: fuses dense (vector) and sparse (BM25) results
    using Reciprocal Rank Fusion (RRF).
    """

    RRF_K = 60 # gold standard from literature

    def __init__(self, vector_retriever: BaseRetriever, bm25_retriever: BaseRetriever, config: HybridRetrieverConfig):
        self._vector = vector_retriever
        self._bm25 = bm25_retriever
        self._config = config

    def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        k = top_k if top_k is not None else self._config.top_k
        fetch_k = self._config.fetch_k

        vector_results = self._vector.retrieve(query, top_k=fetch_k)
        bm25_results = self._bm25.retrieve(query, top_k=fetch_k)

        fused = self._reciprocal_rank_fusion(vector_results, bm25_results)
        return fused[:k]

    def _reciprocal_rank_fusion(self, *ranked_lists: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """
        Merge N ranked lists into one using RRF.
        Each chunk accumulates 1 / (RRF_K + rank) from every list it appears in.
        """
        rrf_scores: dict[str, float] = {}
        chunks_by_id: dict[str, RetrievedChunk] = {}

        for ranked_list in ranked_lists:
            for rank, chunk in enumerate(ranked_list, start=1):
                rrf_scores[chunk.chunk_id] = (rrf_scores.get(chunk.chunk_id, 0.0) + 1.0 / (self.RRF_K + rank))
                chunks_by_id[chunk.chunk_id] = chunk

        return [
            RetrievedChunk(
                chunk_id=chunk_id,
                content=chunks_by_id[chunk_id].content,
                score=score,
                metadata=chunks_by_id[chunk_id].metadata,
            )
            for chunk_id, score in sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        ]