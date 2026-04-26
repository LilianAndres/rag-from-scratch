import httpx

from app.config.models.provider import OllamaProviderConfig
from app.src.core.interfaces.llm import BaseLanguageModel
from app.config.models.llm import OllamaProfileConfig


class OllamaClient(BaseLanguageModel):
    """
    LLM client backed by an Ollama instance.
    """

    def __init__(self, config: OllamaProfileConfig, provider: OllamaProviderConfig):
        self._model = config.model
        self._temperature = config.temperature
        self._max_tokens = config.max_tokens
        self._timeout = config.timeout
        self._base_url = provider.base_url

    def complete(self, prompt: str) -> str:
        response = httpx.post(
            f"{self._base_url}/api/chat",
            json={
                "model": self._model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {
                    "temperature": self._temperature,
                    "num_predict": self._max_tokens,
                },
            },
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]