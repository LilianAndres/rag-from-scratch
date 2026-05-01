from ragas.embeddings import BaseRagasEmbeddings
from eval.config.settings import EvalSettings


class JudgeEmbeddingsFactory:

    def __init__(self, settings: EvalSettings) -> None:
        self._settings = settings

    def create(self) -> BaseRagasEmbeddings:
        from openai import AsyncOpenAI
        from ragas.embeddings.base import embedding_factory
        cfg = self._settings.judge_embeddings
        match cfg.provider:
            case "openai":
                client = AsyncOpenAI(
                    api_key=self._settings.providers.openai.api_key.get_secret_value(),
                    base_url=self._settings.providers.openai.base_url,
                )
                model = cfg.openai.model
            case "ollama":
                client = AsyncOpenAI(
                    api_key="ollama",
                    base_url=f"{self._settings.providers.ollama.base_url}",
                )
                model = cfg.ollama.model
            case "infinity":
                client = AsyncOpenAI(
                    api_key="infinity",
                    base_url=f"{self._settings.providers.infinity.base_url}",
                )
                model = cfg.infinity.model
            case _:
                raise ValueError(f"Unsupported embeddings provider: {cfg.provider!r}")

        # RAGAS embedding_factory only knows openai, google, litellm, huggingface.
        # Ollama is accessed via an OpenAI-compatible AsyncOpenAI client pointing at /v1.
        return embedding_factory(model=model, provider="openai", client=client)