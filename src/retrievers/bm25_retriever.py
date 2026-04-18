from rank_bm25 import BM25Okapi

from src.core.interfaces.retriever import BaseRetriever
from src.core.interfaces.vectorstore import BaseVectorStore
from src.core.retrieval.result import RetrievedChunk
from config.models.retriever import BM25RetrieverConfig


class BM25Retriever(BaseRetriever):
    """
    Sparse retriever backed by BM25Okapi (rank_bm25).

    The index is built at construction time from all chunks currently
    stored in the vector store. This means it reflects the corpus at
    startup.
    """

    def __init__(self, vectorstore: BaseVectorStore, config: BM25RetrieverConfig):
        self._config = config
        self._chunks, self._bm25 = self._build_index(vectorstore)

    def retrieve(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        k = top_k if top_k is not None else self._config.top_k
        tokens = self._tokenize(query)
        scores = self._bm25.get_scores(tokens)

        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

        return [
            RetrievedChunk(
                chunk_id=self._chunks[i]["id"],
                content=self._chunks[i]["content"],
                score=float(scores[i]),
                metadata=self._chunks[i]["metadata"],
            )
            for i in top_indices
            if scores[i] > 0  # BM25 score of 0 means no term overlap at all
        ]

    @staticmethod
    def _build_index(vectorstore: BaseVectorStore) -> tuple[list[dict], BM25Okapi]:
        """
        Pull every chunk from Chroma and build a BM25 index over their content.
        """
        # Access the underlying Chroma collection directly
        collection = vectorstore._collection
        result = collection.get(include=["documents", "metadatas"])

        chunks = [
            {
                "id": chunk_id,
                "content": content,
                "metadata": dict(metadata),
            }
            for chunk_id, content, metadata in zip(
                result["ids"], result["documents"], result["metadatas"]
            )
        ]

        tokenized_corpus = [BM25Retriever._tokenize(chunk["content"]) for chunk in chunks]
        return chunks, BM25Okapi(tokenized_corpus)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Lowercase whitespace tokenization — consistent between index and query."""
        return text.lower().split()