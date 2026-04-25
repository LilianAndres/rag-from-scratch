from config.app_settings import AppSettings
from src.pipelines.ingestion_pipeline import IngestionPipeline
from src.pipelines.rag_pipeline import RAGPipeline
from src.core.ingestion.source_manager import DefaultSourceManager
from src.core.ingestion.loader_manager import DefaultLoaderManager
from src.factories.resolver_factory import ResolverFactory
from src.factories.loader_factory import LoaderFactory
from src.factories.chunker_factory import ChunkerFactory
from src.factories.embedder_factory import EmbedderFactory
from src.factories.backend_factory import BackendFactory
from src.factories.generator_factory import GeneratorFactory
from src.factories.query_transformer_factory import QueryTransformerFactory
from src.factories.reranker_factory import RerankerFactory
from src.factories.llm_factory import LLMFactory


class ApplicationFactory:

    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        self._embedder = None

    def _get_embedder(self):
        if self._embedder is None:
            self._embedder = EmbedderFactory(self.settings.embedder).create_embedder()
        return self._embedder

    def _get_llm(self, profile: str):
        config = self.settings.llms.profiles.get(profile)
        if config is None:
            raise ValueError(
                f"Unknown LLM profile '{profile}'. "
                f"Available: {list(self.settings.llms.profiles.keys())}"
            )
        return LLMFactory(config).create_llm()

    def create_ingestion_pipeline(self) -> IngestionPipeline:
        resolver_registry = ResolverFactory(self.settings.resolver).build_registry()
        loader_registry = LoaderFactory(self.settings.loader).build_registry()
        chunker = ChunkerFactory(self.settings.chunker).create_chunker()
        embedder = self._get_embedder()
        backend = BackendFactory(self.settings.backend).create_backend(embedder)

        return IngestionPipeline(
            resolver=DefaultSourceManager(resolver_registry),
            loader=DefaultLoaderManager(loader_registry),
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

        reranker = RerankerFactory(self.settings.reranker).create_reranker()

        return RAGPipeline(
            backend=backend,
            generator=generator,
            transformer=query_transformer,
            reranker=reranker,
        )