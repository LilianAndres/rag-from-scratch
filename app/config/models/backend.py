from typing import Literal
from pydantic import BaseModel, Field, SecretStr


class ChromaConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000
    collection_name: str = "documents"
    distance_function: str = "cosine"
    batch_size: int = 128

class ELKConfig(BaseModel):
    hosts: list[str] = Field(default_factory=lambda: ["http://localhost:9200"])
    username: str | None = None
    password: SecretStr | None = None
    index_name: str = "documents"
    batch_size: int = 128

class HybridConfig(BaseModel):
    backends: list["BackendConfig"] = Field(default_factory=list)
    rrf_k: int = 60

class BackendConfig(BaseModel):
    type: Literal["chroma", "elk", "hybrid"]

    chroma: ChromaConfig | None = None
    elk: ELKConfig | None = None
    hybrid: HybridConfig | None = None


HybridConfig.model_rebuild()