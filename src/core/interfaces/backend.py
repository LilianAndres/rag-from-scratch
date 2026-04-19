from abc import ABC, abstractmethod
from src.core.search.query import SearchQuery
from src.core.search.result import SearchResult
from src.core.domain.chunk import Chunk


class SearchBackend(ABC):

    @abstractmethod
    async def index(self, chunks: list[Chunk]) -> None:
        """
        Index chunks into database.

        Parameters
        ----------
        chunks:
            A list of Chunk objects.
        """

    @abstractmethod
    async def search(self, query: SearchQuery) -> list[SearchResult]:
        """
        Search for relevant documents based on the *query*.

        Parameters
        ----------
        query:
            The user input query to search for.

        Returns
        -------
        list[SearchResult]
            Ordered list of results from *query*.
        """

    @abstractmethod
    async def delete(self, document_id: str) -> None:
        """
        Delete document from database.

        Parameters
        ----------
        document_id:
            The document to delete.
        """