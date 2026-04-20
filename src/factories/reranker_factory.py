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
            case "cross-encoder":
                from src.rerankers.cross_encoder_reranker import CrossEncoderReranker

                if self._config.cross_encoder is None:
                    raise ValueError("Missing cross-encoder config")

                return CrossEncoderReranker(self._config.cross_encoder)

            case _:
                raise ValueError(
                    f"Unknown reranker provider: {self._config.provider!r}"
                )