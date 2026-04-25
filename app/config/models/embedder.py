from pydantic import BaseModel, SecretStr


class OpenAIEmbedderConfig(BaseModel):
    model: str = "text-embedding-3-small"
    dimensions: int | None = None
    batch_size: int = 512
    api_key: SecretStr


class InfinityEmbedderConfig(BaseModel):
    base_url: str = "http://localhost:7997"
    model: str = "BAAI/bge-small-en-v1.5"
    timeout: float = 30.0


class EmbedderConfig(BaseModel):
    provider: str = "infinity"
    openai: OpenAIEmbedderConfig | None = None
    infinity: InfinityEmbedderConfig = InfinityEmbedderConfig()