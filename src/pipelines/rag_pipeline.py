from src.core.interfaces.backend import SearchBackend
from src.core.interfaces.reranker import BaseReranker
from src.core.interfaces.generator import BaseGenerator
from src.core.search import SearchResult
from src.core.search.query import SearchQuery
from src.core.generation.result import GenerationResult


class RAGPipeline:

    def __init__(
        self,
        backend: SearchBackend,
        generator: BaseGenerator,
        reranker: BaseReranker | None = None,
    ):
        self.backend = backend
        self.reranker = reranker
        self.generator = generator

    async def run(self, query: SearchQuery) -> GenerationResult:
        results= await self.backend.search(query)

        if self.reranker:
            results = self.reranker.rerank(query.text, results)

        return self.generator.generate(query.text, results)