from app.config.models.embedder import EmbedderConfig
from app.config.models.provider import ProvidersConfig
from app.src.core.interfaces.embedder import BaseEmbedder


class EmbedderFactory:
    def __init__(self, config: EmbedderConfig, providers: ProvidersConfig) -> None:
        self._config = config
        self._providers = providers

    def create_embedder(self) -> BaseEmbedder:
        match self._config.provider:
            case "openai":
                if self._providers.openai is None:
                    raise ValueError("OpenAI credentials not configured.")
                from app.src.embedders.openai_embedder import OpenAIEmbedder
                return OpenAIEmbedder(self._config.openai, self._providers.openai)

            case "infinity":
                from app.src.embedders.infinity_embedder import InfinityEmbedder
                return InfinityEmbedder(self._config.infinity, self._providers.infinity)

            case _:
                raise ValueError(f"Unknown embedder provider: {self._config.provider!r}")