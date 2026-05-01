from pydantic import BaseModel


class OpenAIEmbedderConfig(BaseModel):
    model: str = "text-embedding-3-small"
    dimensions: int | None = None
    batch_size: int = 512


class InfinityEmbedderConfig(BaseModel):
    model: str = "BAAI/bge-small-en-v1.5"
    timeout: float = 30.0


class EmbedderConfig(BaseModel):
    provider: str = "infinity"
    openai: OpenAIEmbedderConfig | None = None
    infinity: InfinityEmbedderConfig = InfinityEmbedderConfig()