from config.models.retriever import RetrieverConfig
from src.core.interfaces.retriever import BaseRetriever
from src.core.interfaces.embedder import BaseEmbedder
from src.core.interfaces.vectorstore import BaseVectorStore


def create_retriever(config: RetrieverConfig, embedder: BaseEmbedder, vectorstore: BaseVectorStore) -> BaseRetriever:
    match config.provider:
        case "vector":
            from src.retrievers.vector_retriever import VectorRetriever
            return VectorRetriever(embedder=embedder, vectorstore=vectorstore, config=config.vector)

        case "bm25":
            from src.retrievers.bm25_retriever import BM25Retriever
            return BM25Retriever(vectorstore=vectorstore, config=config.bm25)

        case "hybrid":
            from src.retrievers.vector_retriever import VectorRetriever
            from src.retrievers.bm25_retriever import BM25Retriever
            from src.retrievers.hybrid_retriever import HybridRetriever

            vector = VectorRetriever(embedder=embedder, vectorstore=vectorstore, config=config.vector)
            bm25 = BM25Retriever(vectorstore=vectorstore, config=config.bm25)
            return HybridRetriever(vector_retriever=vector, bm25_retriever=bm25, config=config.hybrid)

        case _:
            raise ValueError(f"Unknown retriever provider: {config.provider!r}")