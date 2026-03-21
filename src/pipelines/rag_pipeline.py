from src.core.retrieval.result import RetrievedChunk
from src.core.interfaces.retriever import BaseRetriever
from src.core.interfaces.reranker import BaseReranker
from src.core.interfaces.generator import BaseGenerator
from src.core.retrieval.query import Query
from src.core.generation.result import GenerationResult


class RAGPipeline:
    """
    Pipeline that performs Retrieval-Augmented Generation (RAG).
    """

    def __init__(
        self,
        retriever: BaseRetriever,
        generator: BaseGenerator,
        reranker: BaseReranker | None = None,
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.generator = generator

    def run(self, query: Query, top_k: int = 5) -> GenerationResult:
        retrieved_chunks: list[RetrievedChunk] = self.retriever.retrieve(query.text, top_k=top_k)

        if self.reranker:
            retrieved_chunks = self.reranker.rerank(query.text, retrieved_chunks)

        answer = self.generator.generate(query.text, retrieved_chunks)

        return answer