from app.config.models.llm import LLMProfileConfig
from app.config.models.provider import ProvidersConfig
from app.src.core.interfaces.llm import BaseLanguageModel


class LLMFactory:
    """
    Builds a single LLM client from a profile config.
    """

    def __init__(self, config: LLMProfileConfig, providers: ProvidersConfig):
        self._config = config
        self._providers = providers

    def create_llm(self) -> BaseLanguageModel:
        match self._config.provider:
            case "openai":
                if self._providers.openai is None:
                    raise ValueError("OpenAI credentials not configured.")
                from app.src.llms.openai_llm import OpenAIClient
                return OpenAIClient(self._config.openai, self._providers.openai)

            case "ollama":
                from app.src.llms.ollama_llm import OllamaClient
                return OllamaClient(self._config.ollama, self._providers.ollama)

            case _:
                raise ValueError(f"Unknown LLM provider: {self._config.provider!r}")