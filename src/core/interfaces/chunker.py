from abc import ABC, abstractmethod

from src.core import Chunk
from src.core.domain import Document


class BaseChunker(ABC):
    """
    Abstract base class for text chunkers.

    A chunker splits large Document objects into smaller chunks that
    fit within the context window of an embedding model.
    """

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        """
        Split *document* into a list of smaller Document chunks.

        Parameters
        ----------
        document:
            The source document to split.

        Returns
        -------
        list[Document]
            Ordered list of chunk documents derived from *document*.
        """

    def chunk_many(self, documents: list[Document]) -> list[Chunk]:
        """
        Chunk multiple documents, flattening results into a single list.
        """
        chunks: list[Chunk] = []
        for doc in documents:
            chunks.extend(self.chunk(doc))
        return chunks