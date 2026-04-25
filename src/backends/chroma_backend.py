import uuid
from chromadb import AsyncHttpClient, AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection

from config.models.backend import ChromaConfig
from src.core.interfaces.backend import SearchBackend
from src.core.interfaces.embedder import BaseEmbedder
from src.core.domain.chunk import Chunk
from src.core.search.search_query import SearchQuery
from src.core.search.search_result import SearchResult


class ChromaBackend(SearchBackend):
    """
    Dense backend backed on ChromaDB (HTTP async client).
    """

    def __init__(self, config: ChromaConfig, embedder: BaseEmbedder):
        self._config = config
        self._embedder = embedder
        self._client: AsyncClientAPI | None = None
        self._collection: AsyncCollection | None = None

    async def _get_collection(self) -> AsyncCollection:
        if self._collection is None:
            self._client = await AsyncHttpClient(
                host=self._config.host,
                port=self._config.port,
            )
            self._collection = await self._client.get_or_create_collection(
                name=self._config.collection_name,
                metadata={"hnsw:space": self._config.distance_function},
            )
        return self._collection

    async def index(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return

        collection = await self._get_collection()

        texts = [chunk.content for chunk in chunks]
        embeddings = await self._embedder.embed_texts(texts)

        ids = [chunk.id or str(uuid.uuid4()) for chunk in chunks]

        metadatas = [
            self._chunk_metadata(chunk, chunk_id)
            for chunk, chunk_id in zip(chunks, ids)
        ]

        await collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

    async def search(self, query: SearchQuery) -> list[SearchResult]:
        collection = await self._get_collection()

        query_embedding = await self._embedder.embed_query(query.text)
        where = query.filters or None

        response = await collection.query(
            query_embeddings=[query_embedding],
            n_results=query.top_k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        results: list[SearchResult] = []

        docs = response.get("documents", [[]])[0]
        metas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]
        ids = response.get("ids", [[]])[0]

        for chunk_id, doc, meta, distance in zip(ids, docs, metas, distances):
            score = self._distance_to_score(distance)
            chunk = Chunk(id=chunk_id, document_id=meta.get("document_id"), content=doc, metadata=meta)
            results.append(SearchResult(chunk=chunk, score=score, metadata=meta))

        return results

    async def delete(self, document_id: str) -> None:
        collection = await self._get_collection()
        await collection.delete(where={"document_id": document_id})

    @staticmethod
    def _chunk_metadata(chunk: Chunk, chunk_id: str) -> dict:
        """
        Flatten metadata for Chroma compatibility.
        Only primitive values allowed.
        """
        raw = {
            "chunk_id": chunk_id,
            "document_id": chunk.document_id,
            **(chunk.metadata or {}),
        }

        return {
            k: v
            for k, v in raw.items()
            if v is not None and isinstance(v, (str, int, float, bool))
        }

    def _distance_to_score(self, distance: float) -> float:
        """
        Convert Chroma distance to similarity score [0, 1]
        based on configured distance function.
        """
        space = getattr(self._config, "distance_function", "cosine")

        match space:
            case "cosine":
                return 1.0 - distance
            case "l2":
                return 1.0 / (1.0 + distance)
            case "ip":
                return distance
            case _:
                return 1.0 - distance