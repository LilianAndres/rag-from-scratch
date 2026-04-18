from config.models.embedder import EmbedderConfig
from src.core.interfaces.embedder import BaseEmbedder


class EmbedderFactory:
    def __init__(self, config: EmbedderConfig) -> None:
        self._config = config

    def create_embedder(self) -> BaseEmbedder:
        match self._config.provider:
            case "openai":
                from src.embedders.openai_embedder import OpenAIEmbedder
                return OpenAIEmbedder(self._config.openai)

            case "huggingface":
                from src.embedders.huggingface_embedder import HuggingFaceEmbedder
                return HuggingFaceEmbedder(self._config.huggingface)

            case _:
                raise ValueError(f"Unknown embedder provider: '{self._config.provider!r}'")