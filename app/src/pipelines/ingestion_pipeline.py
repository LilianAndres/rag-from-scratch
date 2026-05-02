from app.src.core.domain.source import SourceDescriptor
from app.src.core.interfaces.chunker import BaseChunker
from app.src.core.interfaces.backend import SearchBackend
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
            resolver = self.resolver_registry.resolve(descriptor)
            for raw in resolver.discover(descriptor):
                parser = self.parser_registry.resolve(raw)
                chunks = self.chunker.chunk_many(parser.parse(raw))
                await self.backend.index(chunks)