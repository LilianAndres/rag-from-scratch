from functools import lru_cache
from app.config.app_settings import AppSettings
from app.src.factories.app_factory import ApplicationFactory
from app.src.pipelines.ingestion_pipeline import IngestionPipeline
from app.src.pipelines.rag_pipeline import RAGPipeline


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()


@lru_cache(maxsize=1)
def get_factory() -> ApplicationFactory:
    return ApplicationFactory(get_settings())


def get_ingestion_pipeline() -> IngestionPipeline:
    return get_factory().create_ingestion_pipeline()


def get_rag_pipeline() -> RAGPipeline:
    return get_factory().create_rag_pipeline()