from app.config.models.provider import ProvidersConfig
from app.config.models.reranker import RerankerConfig
from app.src.core.interfaces.reranker import BaseReranker


class RerankerFactory:
    def __init__(self, config: RerankerConfig, providers: ProvidersConfig) -> None:
        self._config = config
        self._providers = providers

    def create_reranker(self) -> BaseReranker | None:
        """
        Returns None when reranking is disabled.
        """
        if not self._config.enabled:
            return None

        match self._config.provider:
            case "infinity":
                from app.src.rerankers.infinity_reranker import InfinityReranker
                return InfinityReranker(self._config.infinity, self._providers.infinity)

            case _:
                raise ValueError(f"Unknown reranker provider: {self._config.provider!r}")