from pathlib import Path

from src.core.domain import Document, Chunk
from src.core.ingestion.loader_manager import DefaultLoaderManager
from src.core.ingestion.source_manager import DefaultSourceManager
from src.core.interfaces.chunker import BaseChunker
from src.core.interfaces.backend import SearchBackend


class IngestionPipeline:

    def __init__(
        self,
        resolver: DefaultSourceManager,
        loader: DefaultLoaderManager,
        chunker: BaseChunker,
        backend: SearchBackend,
    ):
        self.resolver = resolver
        self.loader = loader
        self.chunker = chunker
        self.backend = backend

    async def ingest(self, sources: list[str]) -> None:
        for source in sources:
            path: Path = self.resolver.resolve(source)
            docs: list[Document] = self.loader.load(path)
            await self._ingest_documents(docs)

    async def _ingest_documents(self, documents: list[Document]) -> None:
        chunks: list[Chunk] = self.chunker.chunk_many(documents)

        if not chunks:
            return

        batch_size = 64
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            await self.backend.index(batch)