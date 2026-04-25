from app.config.models.llm import LLMProfileConfig
from app.src.core.interfaces.llm import BaseLanguageModel


class LLMFactory:
    """
    Builds a single LLM client from a profile config.
    """

    def __init__(self, config: LLMProfileConfig):
        self._config = config

    def create_llm(self) -> BaseLanguageModel:
        match self._config.provider:
            case "openai":
                from app.src.llms.openai_llm import OpenAIClient
                return OpenAIClient(self._config.openai)
            case "ollama":
                from app.src.llms.ollama_llm import OllamaClient
                return OllamaClient(self._config.ollama)
            case _:
                raise ValueError(
                    f"Unknown LLM provider: {self._config.provider!r}"
                )