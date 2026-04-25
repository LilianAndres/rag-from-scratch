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

            case "infinity":
                from src.embedders.infinity_embedder import InfinityEmbedder
                return InfinityEmbedder(self._config.infinity)

            case _:
                raise ValueError(f"Unknown embedder provider: '{self._config.provider!r}'")