from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from app.config.models.backend import ELKConfig
from app.src.core.interfaces.backend import SearchBackend
from app.src.core.domain.chunk import Chunk
from app.src.core.search.search_query import SearchQuery
from app.src.core.search.search_result import SearchResult


_MAPPING = {
    "mappings": {
        "properties": {
            "content": {"type": "text"},
            "document_id": {"type": "keyword"},
            "chunk_id": {"type": "keyword"},
        }
    }
}


class ELKBackend(SearchBackend):
    """
    Sparse lexical backend backed by Elasticsearch (BM25 only).
    """

    def __init__(self, config: ELKConfig) -> None:
        self._client = AsyncElasticsearch(
            hosts=config.hosts,
            basic_auth=(
                (config.username, config.password.get_secret_value())
                if config.username and config.password
                else None
            ),
        )
        self._config = config

    async def _ensure_index(self) -> None:
        exists = await self._client.indices.exists(index=self._config.index_name)
        if not exists:
            await self._client.indices.create(index=self._config.index_name, body=_MAPPING)

    async def index(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return

        await self._ensure_index()

        docs = [
            {
                "_index": self._config.index_name,
                "_id": chunk.id,
                "_source": self._chunk_to_source(chunk),
            }
            for chunk in chunks
        ]

        await async_bulk(self._client, docs)

    async def search(self, query: SearchQuery) -> list[SearchResult]:
        body = {
            "size": query.top_k,
            "query": self._build_query(query),
        }

        response = await self._client.search(
            index=self._config.index_name,
            body=body,
        )

        hits = response.get("hits", {}).get("hits", [])
        return [self._to_result(hit) for hit in hits]

    async def delete(self, document_id: str) -> None:
        await self._client.delete_by_query(
            index=self._config.index_name,
            body={
                "query": {
                    "term": {"document_id": document_id}
                }
            },
        )

    def _build_query(self, query: SearchQuery) -> dict:
        """
        Build a BM25 query with optional filters.
        """
        base_query = {
            "match": {
                "content": query.text
            }
        }

        if not query.filters:
            return base_query

        return {
            "bool": {
                "must": base_query,
                "filter": [
                    {"term": {k: v}} for k, v in query.filters.items()
                ],
            }
        }

    @staticmethod
    def _chunk_to_source(chunk: Chunk) -> dict:
        """
        Flatten metadata for Elasticsearch.
        """
        raw = {
            "content": chunk.content,
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            **(chunk.metadata or {}),
        }

        return {
            k: v
            for k, v in raw.items()
            if v is not None and isinstance(v, (str, int, float, bool))
        }

    @staticmethod
    def _to_result(hit: dict) -> SearchResult:
        src = hit["_source"]

        chunk = Chunk(
            id=src.get("chunk_id"),
            content=src["content"],
            metadata={k: v for k, v in src.items() if k not in "content"},
            document_id=src.get("document_id"),
        )

        return SearchResult(chunk=chunk, score=hit["_score"], metadata=src)