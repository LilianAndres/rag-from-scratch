from openai import AsyncOpenAI

from app.config.models.embedder import OpenAIEmbedderConfig
from app.config.models.provider import OpenAIProviderConfig
from app.src.core.interfaces.embedder import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):

    def __init__(self, config: OpenAIEmbedderConfig, provider: OpenAIProviderConfig):
        self._model = config.model
        self._dimensions = config.dimensions
        self._batch_size = config.batch_size
        self._client = AsyncOpenAI(
            api_key=provider.api_key.get_secret_value(),
            base_url=provider.base_url,
        )

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self._batch_size):
            vectors.extend(await self._embed_batch(texts[start: start + self._batch_size]))
        return vectors

    async def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        kwargs: dict = dict(input=texts, model=self._model)
        if self._dimensions is not None:
            kwargs["dimensions"] = self._dimensions
        response = await self._client.embeddings.create(**kwargs)
        return [item.embedding for item in sorted(response.data, key=lambda i: i.index)]