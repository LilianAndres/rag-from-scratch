from abc import ABC, abstractmethod
from pathlib import Path

from src.core.domain.document import Document


class BaseLoader(ABC):
    """
    Abstract base class for document loaders.

    A loader is responsible for reading raw source material and converting it
    into a list of Document objects that the rest of the pipeline can process.
    """

    @abstractmethod
    def load(self, source: str | Path) -> list[Document]:
        """
        Load documents from *source*.

        Parameters
        ----------
        source:
            A file path, directory path, or any other identifier that
            the concrete loader knows how to handle.

        Returns
        -------
        list[Document]
            One or more documents extracted from *source*.
        """

    def load_many(self, sources: list[str | Path]) -> list[Document]:
        """
        Load documents from multiple sources.
        """
        docs: list[Document] = []
        for source in sources:
            docs.extend(self.load(source))
        return docs