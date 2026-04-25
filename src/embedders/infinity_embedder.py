import httpx

from src.core.interfaces.embedder import BaseEmbedder
from config.models.embedder import InfinityEmbedderConfig


class InfinityEmbedder(BaseEmbedder):
    """
    Embedder backed by an Infinity inference server.
    Compatible with any HuggingFace embedding model served by Infinity.
    """

    def __init__(self, config: InfinityEmbedderConfig):
        self._config = config

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        response = httpx.post(
            f"{self._config.base_url}/embeddings",
            json={"input": texts, "model": self._config.model},
            timeout=self._config.timeout,
        )
        response.raise_for_status()
        data = response.json()

        ordered = sorted(data["data"], key=lambda item: item["index"])
        return [item["embedding"] for item in ordered]