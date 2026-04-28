from typing import Any
from eval.config.settings import EvalSettings


class LLMFactory:

    def __init__(self, settings: EvalSettings) -> None:
        self._settings = settings

    def create(self) -> Any:
        from ragas.llms import llm_factory
        from openai import AsyncOpenAI
        cfg = self._settings.judge
        match cfg.provider:
            case "openai":
                client = AsyncOpenAI(
                    api_key=self._settings.providers.openai.api_key.get_secret_value(),
                    base_url=self._settings.providers.openai.base_url,
                )
                return llm_factory(model=cfg.openai.model, provider="openai", client=client)
            case "ollama":
                client = AsyncOpenAI(
                    api_key="ollama",
                    base_url=f"{self._settings.providers.ollama.base_url}/v1",
                )
                return llm_factory(model=cfg.ollama.model, provider="openai", client=client)
            case _:
                raise ValueError(f"Unknown judge provider: {cfg.provider!r}")