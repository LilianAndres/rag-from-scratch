from config.models.backend import BackendConfig

from src.core.interfaces.backend import SearchBackend
from src.core.interfaces.embedder import BaseEmbedder


class BackendFactory:
    def __init__(self, config: BackendConfig) -> None:
        self._config = config

    def create_backend(self, embedder: BaseEmbedder) -> SearchBackend:
        match self._config.type:

            case "chroma":
                from src.backends.dense.chroma_backend import ChromaBackend

                if self._config.chroma is None:
                    raise ValueError("Missing chroma config")

                return ChromaBackend(config=self._config.chroma, embedder=embedder)

            case "elk":
                from src.backends.sparse.elk_backend import ELKBackend

                if self._config.elk is None:
                    raise ValueError("Missing ELK config")

                return ELKBackend(config=self._config.elk)

            case "hybrid":
                from src.backends.hybrid_backend import HybridBackend

                if self._config.hybrid is None:
                    raise ValueError("Missing hybrid config")

                sub_backends = [
                    BackendFactory(sub_config).create_backend(embedder)
                    for sub_config in self._config.hybrid.backends
                ]

                return HybridBackend(
                    backends=sub_backends,
                    rrf_k=self._config.hybrid.rrf_k
                )

            case _:
                raise ValueError(f"Unknown backend type: {self._config.type!r}")