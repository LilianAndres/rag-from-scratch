from config.models.vectorstore import VectorStoreConfig
from src.core.interfaces.vectorstore import BaseVectorStore


def create_vectorstore(config: VectorStoreConfig) -> BaseVectorStore:
    match config.provider:
        case "chroma":
            from src.vectorstores.chroma_vectorstore import ChromaVectorStore
            return ChromaVectorStore(config.chroma)
        case _:
            raise ValueError(f"Unknown vectorstore provider: {config.provider!r}")