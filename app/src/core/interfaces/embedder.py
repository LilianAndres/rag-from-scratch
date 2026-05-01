from abc import ABC, abstractmethod

from app.src.core.domain.chunk import Chunk
from app.src.core.embeddings.embedding import Embedding


class BaseEmbedder(ABC):
    """
    Abstract base class for embedding models.

    An embedder converts text or chunks into dense vector representations
    used for semantic similarity search.
    """

    @abstractmethod
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a batch of raw text strings.

        Parameters
        ----------
        texts : List[str]
            The texts to embed.

        Returns
        -------
        List[List[float]]
            A list of embedding vectors, one per input text, in the same order.
        """

    async def embed_chunks(self, chunks: list[Chunk], model_name: str) -> list[Embedding]:
        """
        Embed a list of chunks, producing Embedding objects.

        Parameters
        ----------
        chunks : List[Chunk]
            The chunks to embed.
        model_name : str
            The name of the embedding model used.

        Returns
        -------
        List[Embedding]
            One embedding per chunk.
        """
        vectors = await self.embed_texts([chunk.content for chunk in chunks])
        embeddings = [
            Embedding(chunk_id=chunk.id, vector=vec, model_name=model_name)
            for chunk, vec in zip(chunks, vectors)
        ]
        return embeddings

    async def embed_query(self, query: str) -> list[float]:
        """
        Embed a single query string.

        Parameters
        ----------
        query : str
            The text of the query.

        Returns
        -------
        List[float]
            The embedding vector for the query.
        """
        results = await self.embed_texts([query])
        return results[0]