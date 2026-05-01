from abc import ABC, abstractmethod

from app.src.core.generation.generation_result import GenerationResult
from app.src.core.search.search_result import SearchResult


class BaseGenerator(ABC):
    """
    Abstract base class for answer generators.

    A generator receives the user's query together with a set of retrieved
    (and optionally reranked) context chunks, and produces a final answer.
    """

    @abstractmethod
    def generate(self, query: str, context: list[SearchResult]) -> GenerationResult:
        """
        Generate an answer for *query* grounded in *context*.

        Parameters
        ----------
        query:
            The user's natural-language question.
        context:
            Ordered list of relevant chunks retrieved for *query*.  The
            generator is responsible for deciding how many tokens to include.

        Returns
        -------
        GenerationResult
            The generated answer together with the source chunks used.
        """