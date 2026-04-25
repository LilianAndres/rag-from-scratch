from openai import AsyncOpenAI

from app.config.models.embedder import OpenAIEmbedderConfig
from app.src.core.interfaces.embedder import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):

    def __init__(self, config: OpenAIEmbedderConfig):
        self.model = config.model
        self.dimensions = config.dimensions
        self.batch_size = config.batch_size
        self._client = AsyncOpenAI(api_key=config.api_key.get_secret_value())

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            vectors.extend(await self._embed_batch(texts[start: start + self.batch_size]))
        return vectors

    async def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        kwargs: dict = dict(input=texts, model=self.model)
        if self.dimensions is not None:
            kwargs["dimensions"] = self.dimensions
        response = await self._client.embeddings.create(**kwargs)
        return [item.embedding for item in sorted(response.data, key=lambda i: i.index)]