from abc import ABC, abstractmethod

from app.src.core.search.search_query import SearchQuery


class BaseQueryTransformer(ABC):

    @abstractmethod
    def transform(self, query: SearchQuery) -> list[SearchQuery]:
        """
        Transform a query into one or more retrieval queries.

        Parameters
        ----------
        query:
            The user's original search query.

        Returns
        -------
        list[SearchQuery]
            One or more queries to retrieve against.
        """