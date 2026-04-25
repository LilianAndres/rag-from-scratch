import httpx

from app.src.core.interfaces.embedder import BaseEmbedder
from app.config.models.embedder import InfinityEmbedderConfig


class InfinityEmbedder(BaseEmbedder):
    """
    Embedder backed by an Infinity inference server.
    Compatible with any HuggingFace embedding model served by Infinity.
    """

    def __init__(self, config: InfinityEmbedderConfig):
        self._config = config

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._config.base_url}/embeddings",
                json={"input": texts, "model": self._config.model},
                timeout=self._config.timeout,
            )
            response.raise_for_status()
            data = response.json()

            ordered = sorted(data["data"], key=lambda item: item["index"])
            return [item["embedding"] for item in ordered]