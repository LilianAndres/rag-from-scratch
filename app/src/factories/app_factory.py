from app.config.settings import AppSettings
from app.src.pipelines.ingestion_pipeline import IngestionPipeline
from app.src.pipelines.rag_pipeline import RAGPipeline
from app.src.factories.resolver_factory import ResolverFactory
from app.src.factories.parser_factory import ParserFactory
from app.src.factories.chunker_factory import ChunkerFactory
from app.src.factories.embedder_factory import EmbedderFactory
from app.src.factories.backend_factory import BackendFactory
from app.src.factories.generator_factory import GeneratorFactory
from app.src.factories.query_transformer_factory import QueryTransformerFactory
from app.src.factories.reranker_factory import RerankerFactory
from app.src.factories.llm_factory import LLMFactory


class ApplicationFactory:

    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        self._embedder = None

    def _get_embedder(self):
        if self._embedder is None:
            self._embedder = EmbedderFactory(self.settings.embedder, self.settings.providers).create_embedder()
        return self._embedder

    def _get_llm(self, profile: str):
        config = self.settings.llms.profiles.get(profile)
        if config is None:
            raise ValueError(
                f"Unknown LLM profile '{profile}'. "
                f"Available: {list(self.settings.llms.profiles.keys())}"
            )
        return LLMFactory(config, self.settings.providers).create_llm()

    def create_ingestion_pipeline(self) -> IngestionPipeline:
        resolver_registry = ResolverFactory().build_registry()
        parser_registry = ParserFactory(self.settings.parsers).build_registry()
        chunker = ChunkerFactory(self.settings.chunker).create_chunker()
        embedder = self._get_embedder()
        backend = BackendFactory(self.settings.backend).create_backend(embedder)

        return IngestionPipeline(
            resolver_registry=resolver_registry,
            parser_registry=parser_registry,
            chunker=chunker,
            backend=backend,
        )

    def create_rag_pipeline(self) -> RAGPipeline:
        embedder = self._get_embedder()
        backend = BackendFactory(self.settings.backend).create_backend(embedder)

        generator = GeneratorFactory(
            config=self.settings.generator,
            llm=self._get_llm(self.settings.generator.llm_profile),
        ).create_generator()

        query_transformer = QueryTransformerFactory(
            config=self.settings.query_transformer,
            llm=(
                self._get_llm(self.settings.query_transformer.llm_profile)
                if self.settings.query_transformer.enabled
                else None
            ),
        ).create()

        reranker = RerankerFactory(self.settings.reranker, self.settings.providers).create_reranker()

        return RAGPipeline(
            backend=backend,
            generator=generator,
            transformer=query_transformer,
            reranker=reranker,
        )