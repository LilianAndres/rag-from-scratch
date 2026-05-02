from itertools import islice
from typing import Iterator
from uuid import UUID

from chromadb import AsyncHttpClient, AsyncClientAPI
from chromadb.api.models.AsyncCollection import AsyncCollection

from app.config.models.backend import ChromaConfig
from app.src.core.interfaces.backend import SearchBackend
from app.src.core.interfaces.embedder import BaseEmbedder
from app.src.core.domain.chunk import Chunk
from app.src.core.search.search_query import SearchQuery
from app.src.core.search.search_result import SearchResult


class ChromaBackend(SearchBackend):
    """
    Dense backend backed on ChromaDB (HTTP async client).
    """

    def __init__(self, config: ChromaConfig, embedder: BaseEmbedder):
        self._host: str = config.host
        self._port: int = config.port
        self._collection_name: str = config.collection_name
        self._distance_function: str = config.distance_function
        self._embedder = embedder
        self._client: AsyncClientAPI | None = None
        self._collection: AsyncCollection | None = None
        self._batch_size: int = config.batch_size

    async def _get_collection(self) -> AsyncCollection:
        if self._collection is None:
            self._client = await AsyncHttpClient(
                host=self._host,
                port=self._port,
            )
            self._collection = await self._client.get_or_create_collection(
                name=self._collection_name,
                metadata={"hnsw:space": self._distance_function},
            )
        return self._collection

    async def index(self, chunks: Iterator[Chunk]) -> None:
        collection = await self._get_collection()

        for batch in self._batched(chunks, self._batch_size):
            texts = [chunk.content for chunk in batch]
            embeddings = await self._embedder.embed_texts(texts)
            ids = [str(chunk.id) for chunk in batch]
            metadatas = [self._chunk_metadata(chunk, chunk_id) for chunk, chunk_id in zip(batch, ids)]

            await collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
            )

    @staticmethod
    def _batched(it: Iterator[Chunk], size: int) -> Iterator[list[Chunk]]:
        while batch := list(islice(it, size)):
            yield batch

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
            chunk = Chunk(
                id=UUID(chunk_id),
                document_id=UUID(meta.get("document_id")),
                content=doc,
                metadata=meta,
            )
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
            "chunk_id": str(chunk_id),
            "document_id": str(chunk.document_id),
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
        space = self._distance_function

        match space:
            case "cosine":
                return 1.0 - distance
            case "l2":
                return 1.0 / (1.0 + distance)
            case "ip":
                return distance
            case _:
                return 1.0 - distance