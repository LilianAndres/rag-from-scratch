import chromadb
from chromadb import Collection

from src.core.interfaces.vectorstore import BaseVectorStore
from src.core.domain import Chunk
from src.core.embeddings.embedding import Embedding
from src.core.retrieval.result import RetrievedChunk
from config.models.vectorstore import ChromaVectorStoreConfig


class ChromaVectorStore(BaseVectorStore):
    """
    Vector store backed by ChromaDB in embedded (local) mode.
    Persists automatically to disk at the configured path.
    """

    def __init__(self, config: ChromaVectorStoreConfig):
        self._client = chromadb.PersistentClient(path=config.persist_directory)
        self._collection: Collection = self._client.get_or_create_collection(
            name=config.collection_name,
            metadata={"hnsw:space": config.distance_function},
        )

    def add_chunks(self, chunks: list[Chunk], embeddings: list[Embedding]) -> list[str]:
        if not chunks:
            return []

        self._collection.upsert(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.content for chunk in chunks],
            embeddings=[embedding.vector for embedding in embeddings],
            metadatas=[self._chunk_metadata(chunk) for chunk in chunks],
        )
        return [chunk.id for chunk in chunks]

    def similarity_search(self, query_vector: list[float], k: int = 5) -> list[RetrievedChunk]:
        results = self._collection.query(
            n_results=k,
            query_embeddings=[query_vector],
            include=["documents", "metadatas", "distances"],
        )

        retrieved: list[RetrievedChunk] = []

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for chunk_id, content, metadata, distance in zip(ids, documents, metadatas, distances):
            retrieved.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    content=content,
                    score=self._distance_to_score(distance, metadata),
                    metadata=metadata,
                )
            )
        return retrieved

    def delete(self, chunk_ids: list[str]) -> None:
        self._collection.delete(ids=chunk_ids)

    @staticmethod
    def _chunk_metadata(chunk: Chunk) -> dict:
        """
        Flatten chunk metadata to a Chroma-compatible dict.
        Chroma only accepts str, int, float, bool values — no nested objects.
        """
        raw = {
            "document_id": chunk.document_id,
            **chunk.metadata,
        }
        return {k: v for k, v in raw.items() if v is not None}

    @staticmethod
    def _distance_to_score(distance: float, metadata: dict) -> float:
        """
        Chroma returns a distance, not a similarity score.
        Convert to a [0, 1] similarity score based on the distance function.
        """
        space = metadata.get("hnsw:space", "cosine")
        match space:
            case "cosine":
                return 1.0 - distance / 2.0
            case "l2":
                return 1.0 / (1.0 + distance)
            case "ip":
                return distance
            case _:
                return 1.0 - distance