from abc import ABC, abstractmethod
from typing import List

from src.core.retrieval.result import RetrievedChunk
from src.core.domain import Document, Chunk
from src.core.embeddings.embedding import Embedding


class BaseVectorStore(ABC):
    """
    Abstract base class for vector stores.

    A vector store persists chunk embeddings and exposes nearest-neighbor
    search so that a retriever can find the most semantically similar chunks
    for a given query vector.
    """

    @abstractmethod
    def add_chunks(self, chunks: List[Chunk], embeddings: List[Embedding]) -> List[str]:
        """
        Convenience method: store chunks and their embeddings together.

        Parameters
        ----------
        chunks : List[Chunk]
            Chunks to store.
        embeddings : List[Embedding]
            Corresponding embeddings, must be in the same order.

        Returns
        -------
        List[str]
            Chunk IDs confirmed by the store.
        """
        pass

    @abstractmethod
    def similarity_search(self, query_vector: List[float], k: int = 5) -> List[RetrievedChunk]:
        """
        Return the k most similar chunks to the given query vector.

        Parameters
        ----------
        query_vector : List[float]
            Dense embedding of the user query.
        k : int
            Maximum number of results to return.

        Returns
        -------
        List[RetrievedChunk]
            Results sorted by descending similarity score.
        """
        pass

    @abstractmethod
    def delete(self, chunk_ids: List[str]) -> None:
        """
        Remove embeddings (and optionally chunks) from the store by their IDs.

        Parameters
        ----------
        chunk_ids : List[str]
            IDs of the chunks to remove.
        """
        pass

    @abstractmethod
    def get_all_chunks(self) -> list[tuple[str, str, dict]]:
        """
        Return all stored chunks as (id, content, metadata) tuples.
        Used by in-memory retrievers (e.g. BM25) to build their index.
        """