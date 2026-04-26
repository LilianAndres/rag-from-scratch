import httpx

from app.config.models.provider import InfinityProviderConfig
from app.src.core.interfaces.embedder import BaseEmbedder
from app.config.models.embedder import InfinityEmbedderConfig


class InfinityEmbedder(BaseEmbedder):
    """
    Embedder backed by an Infinity inference server.
    Compatible with any HuggingFace embedding model served by Infinity.
    """

    def __init__(self, config: InfinityEmbedderConfig, provider: InfinityProviderConfig):
        self._model = config.model
        self._timeout = config.timeout
        self._base_url = provider.base_url
        self._api_key = provider.api_key  # None until server is secured

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        headers = {}
        if self._api_key is not None:
            headers["Authorization"] = f"Bearer {self._api_key.get_secret_value()}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/embeddings",
                headers=headers,
                json={"input": texts, "model": self._model},
                timeout=self._timeout,
            )
            response.raise_for_status()
            data = response.json()

            ordered = sorted(data["data"], key=lambda item: item["index"])
            return [item["embedding"] for item in ordered]