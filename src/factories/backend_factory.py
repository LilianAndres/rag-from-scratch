from config.models.backend import BackendConfig, HybridConfig

from src.core.interfaces.backend import SearchBackend
from src.core.interfaces.embedder import BaseEmbedder


def create_backend(config: BackendConfig, embedder: BaseEmbedder) -> SearchBackend:
    match config.type:

        case "chroma":
            from src.backends.dense.chroma_backend import ChromaBackend

            if config.chroma is None:
                raise ValueError("Missing chroma config")

            return ChromaBackend(config=config.chroma, embedder=embedder)

        case "elk":
            from src.backends.sparse.elk_backend import ELKBackend

            if config.elk is None:
                raise ValueError("Missing ELK config")

            return ELKBackend(config=config.elk)

        case "hybrid":
            from src.backends.hybrid_backend import HybridBackend

            if config.hybrid is None:
                raise ValueError("Missing hybrid config")

            sub_backends = [create_backend(sub_config, embedder) for sub_config in config.backends]

            return HybridBackend(backends=sub_backends, rrf_k=config.rrf_k)

        case _:
            raise ValueError(f"Unknown backend type: {config.type!r}")