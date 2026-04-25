from app.src.core.interfaces import BaseQueryTransformer
from app.src.core.interfaces.backend import SearchBackend
from app.src.core.interfaces.reranker import BaseReranker
from app.src.core.interfaces.generator import BaseGenerator
from app.src.core.search.search_query import SearchQuery
from app.src.core.generation.generation_result import GenerationResult


class RAGPipeline:

    def __init__(
        self,
        backend: SearchBackend,
        generator: BaseGenerator,
        transformer: BaseQueryTransformer | None = None,
        reranker: BaseReranker | None = None,
    ):
        self.backend = backend
        self.generator = generator
        self.transformer = transformer
        self.reranker = reranker

    async def run(self, query: SearchQuery, top_n: int | None = None) -> GenerationResult:
        queries = [query]
        if self.transformer is not None:
            queries = self.transformer.transform(query)

        results = []
        for q in queries:
            result = await self.backend.search(q)
            results.extend(result)

        if self.reranker is not None:
            results = await self.reranker.rerank(query.text, results, top_n)

        return self.generator.generate(query.text, results)