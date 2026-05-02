from abc import ABC, abstractmethod
from typing import Iterator

from app.src.core.domain.document import Document
from app.src.core.domain.chunk import Chunk


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

    def chunk_many(self, documents: Iterator[Document]) -> Iterator[Chunk]:
        for doc in documents:
            yield from self.chunk(doc)