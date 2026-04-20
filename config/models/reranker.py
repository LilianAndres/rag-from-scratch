from pydantic import BaseModel


class CrossEncoderRerankerConfig(BaseModel):
    model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_n: int | None = None  # None = return all, reordered

class RerankerConfig(BaseModel):
    enabled: bool = False
    provider: str = "cross-encoder"
    cross_encoder: CrossEncoderRerankerConfig = CrossEncoderRerankerConfig()