from abc import ABC, abstractmethod
from typing import Iterator

from app.src.core.search.search_query import SearchQuery
from app.src.core.search.search_result import SearchResult
from app.src.core.domain.chunk import Chunk


class SearchBackend(ABC):

    @abstractmethod
    async def index(self, chunks: Iterator[Chunk]) -> None:
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