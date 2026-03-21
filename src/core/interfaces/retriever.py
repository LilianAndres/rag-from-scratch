from abc import ABC, abstractmethod

from src.core import RetrievedChunk


class BaseRetriever(ABC):
    """
    Abstract base class for retrievers.

    A retriever accepts a natural-language query and returns the most relevant
    document chunks from one or more underlying sources (vector store, keyword
    index, knowledge graph, etc.).
    """

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """
        Fetch the top-*k* most relevant chunks for *query*.

        Parameters
        ----------
        query:
            The user's natural-language question or search string.
        top_k:
            Maximum number of chunks to return.

        Returns
        -------
        list[RetrievedChunk]
            Relevant chunks, ordered by descending relevance.
        """

    def retrieve_many(self, queries: list[str], top_k: int = 5) -> list[list[RetrievedChunk]]:
        """
        Retrieve results for multiple queries.
        """
        return [self.retrieve(q, top_k=top_k) for q in queries]