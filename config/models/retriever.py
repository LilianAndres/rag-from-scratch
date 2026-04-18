from pydantic import BaseModel


class VectorRetrieverConfig(BaseModel):
    top_k: int = 5
    score_threshold: float | None = None


class BM25RetrieverConfig(BaseModel):
    top_k: int = 5


class HybridRetrieverConfig(BaseModel):
    top_k: int = 5
    fetch_k: int = 20  # how many results to fetch from each retriever before fusion


class RetrieverConfig(BaseModel):
    provider: str = "hybrid"
    vector: VectorRetrieverConfig = VectorRetrieverConfig()
    bm25: BM25RetrieverConfig = BM25RetrieverConfig()
    hybrid: HybridRetrieverConfig = HybridRetrieverConfig()