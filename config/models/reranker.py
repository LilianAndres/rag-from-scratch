from pydantic import BaseModel


class InfinityRerankerConfig(BaseModel):
    base_url: str = "http://localhost:7997"
    model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_n: int | None = None
    timeout: float = 30.0

class RerankerConfig(BaseModel):
    enabled: bool = False
    provider: str = "infinity"
    infinity: InfinityRerankerConfig = InfinityRerankerConfig()