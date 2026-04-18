from src.core.interfaces.retriever import BaseRetriever
from src.core.interfaces.embedder import BaseEmbedder
from src.core.interfaces.vectorstore import BaseVectorStore
from src.core.retrieval.result import RetrievedChunk
from config.models.retriever import VectorRetrieverConfig


class VectorRetriever(BaseRetriever):
    """
    Dense retriever: embeds the query and searches the vector store.
    """

    def __init__(self, embedder: BaseEmbedder, vectorstore: BaseVectorStore, config: VectorRetrieverConfig):
        self._embedder = embedder
        self._vectorstore = vectorstore
        self.top_k = config.top_k
        self.score_threshold = config.score_threshold

    def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        k = top_k if top_k is not None else self.top_k
        query_vector = self._embedder.embed_query(query)
        results = self._vectorstore.similarity_search(query_vector, k=k)
        return self._apply_score_threshold(results)

    def _apply_score_threshold(self, results: list[RetrievedChunk]) -> list[RetrievedChunk]:
        threshold = self.score_threshold
        if threshold is None:
            return results
        return [r for r in results if r.score >= threshold]