from openai import OpenAI

from config.models.embedder import OpenAIEmbedderConfig
from src.core.interfaces.embedder import BaseEmbedder


class OpenAIEmbedder(BaseEmbedder):
    """
    Embedder backed by the OpenAI Embeddings API.

    Supports ``text-embedding-3-small`` and ``text-embedding-3-large``.
    Sub-batches internally so callers never have to think about API limits.
    """

    def __init__(self, config: OpenAIEmbedderConfig):
        self.model = config.model
        self.dimensions = config.dimensions
        self.batch_size = config.batch_size
        self._client = OpenAI(api_key=config.api_key.get_secret_value())

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            vectors.extend(self._embed_batch(texts[start : start + self.batch_size]))
        return vectors

    def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        kwargs: dict = dict(input=texts, model=self.model)
        if self.dimensions is not None:
            kwargs["dimensions"] = self.dimensions
        response = self._client.embeddings.create(**kwargs)
        return [item.embedding for item in sorted(response.data, key=lambda i: i.index)]