from pydantic import BaseModel
from typing import Literal


class ChromaVectorStoreConfig(BaseModel):
    persist_directory: str = ".chroma"
    collection_name: str = "rag_collection"
    distance_function: Literal["cosine", "l2", "ip"] = "cosine"


class VectorStoreConfig(BaseModel):
    provider: str = "chroma"
    chroma: ChromaVectorStoreConfig = ChromaVectorStoreConfig()