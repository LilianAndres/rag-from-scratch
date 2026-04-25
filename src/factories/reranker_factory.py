from config.models.reranker import RerankerConfig
from src.core.interfaces.reranker import BaseReranker


class RerankerFactory:
    def __init__(self, config: RerankerConfig) -> None:
        self._config = config

    def create_reranker(self) -> BaseReranker | None:
        """
        Returns None when reranking is disabled.
        """
        if not self._config.enabled:
            return None

        match self._config.provider:
            case "infinity":
                from src.rerankers.infinity_reranker import InfinityReranker
                if self._config.infinity is None:
                    raise ValueError("Missing infinity reranker config")
                return InfinityReranker(self._config.infinity)

            case _:
                raise ValueError(
                    f"Unknown reranker provider: {self._config.provider!r}"
                )