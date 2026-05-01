from itertools import islice
from typing import Iterator

from app.src.core.domain.chunk import Chunk
from app.src.core.domain.document import Document
from app.src.core.domain.source import SourceDescriptor
from app.src.core.interfaces.chunker import BaseChunker
from app.src.core.interfaces.backend import SearchBackend
from app.src.core.interfaces.parser import BaseParser
from app.src.core.interfaces.source import BaseSourceResolver
from app.src.registries.parser_registry import ParserRegistry
from app.src.registries.resolver_registry import ResolverRegistry


class IngestionPipeline:

    def __init__(
        self,
        resolver_registry: ResolverRegistry,
        parser_registry: ParserRegistry,
        chunker: BaseChunker,
        backend: SearchBackend,
    ):
        self.resolver_registry = resolver_registry
        self.parser_registry = parser_registry
        self.chunker = chunker
        self.backend = backend

    async def ingest(self, descriptors: list[SourceDescriptor]) -> None:
        for descriptor in descriptors:
            resolver: BaseSourceResolver = self.resolver_registry.resolve(descriptor)
            for raw in resolver.discover(descriptor):
                parser: BaseParser = self.parser_registry.resolve(raw)
                await self._ingest_documents(parser.parse(raw))

    async def _ingest_documents(self, documents: Iterator[Document]) -> None:
        while batch := list(islice(documents, 64)):
            chunks: list[Chunk] = self.chunker.chunk_many(batch)
            if chunks:
                await self.backend.index(chunks)