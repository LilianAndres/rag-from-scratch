from config.models import LoaderConfig
from src.registry import BaseRegistry
from src.loaders.pdf_loader import PDFLoader


class LoaderFactory:
    def __init__(self, config: LoaderConfig) -> None:
        self._config = config

    def build_registry(self) -> BaseRegistry:
        registry = BaseRegistry()
        registry.register("pdf",  PDFLoader(config=self._config.pdf))
        return registry