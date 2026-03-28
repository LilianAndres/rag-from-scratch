from config.app_settings import AppSettings
from src.pipelines.ingestion_pipeline import IngestionPipeline
from src.pipelines.rag_pipeline import RAGPipeline


class ApplicationFactory:

    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def make_ingestion_pipeline(self) -> IngestionPipeline:
        pass

    def make_rag_pipeline(self) -> RAGPipeline:
        pass

