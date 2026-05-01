from ragas.embeddings import BaseRagasEmbeddings

from eval.config.settings import EvalSettings
from eval.factories.client_factory import ClientFactory


class JudgeEmbeddingsFactory:

    def __init__(self, settings: EvalSettings) -> None:
        self._settings = settings

    def create(self) -> BaseRagasEmbeddings:
        from ragas.embeddings.base import embedding_factory
        cfg = self._settings.judge_embeddings
        client = ClientFactory(self._settings).create(cfg.provider)
        match cfg.provider:
            case "openai":
                model = cfg.openai.model
            case "infinity":
                model = cfg.infinity.model
            case _:
                raise ValueError(f"Unsupported embeddings provider: {cfg.provider!r}")
        return embedding_factory(model=model, provider="openai", client=client)