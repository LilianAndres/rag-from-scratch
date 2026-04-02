from sentence_transformers import SentenceTransformer

from src.core.interfaces.embedder import BaseEmbedder
from config.models.embedder import HuggingFaceEmbedderConfig


class HuggingFaceEmbedder(BaseEmbedder):
    """
    Local embedder backed by sentence-transformers.
    No API key, no cost, runs on CPU or GPU.
    """

    def __init__(self, config: HuggingFaceEmbedderConfig):
        self.batch_size = config.batch_size
        self._model = SentenceTransformer(config.model)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self._model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return vectors.tolist()