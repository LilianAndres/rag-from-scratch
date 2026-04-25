import httpx

from src.core.interfaces.llm import BaseLanguageModel
from config.models.llm import OllamaProfileConfig


class OllamaClient(BaseLanguageModel):
    """
    LLM client backed by an Ollama instance.
    """

    def __init__(self, config: OllamaProfileConfig):
        self._config = config

    def complete(self, prompt: str) -> str:
        response = httpx.post(
            f"{self._config.base_url}/api/chat",
            json={
                "model": self._config.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {
                    "temperature": self._config.temperature,
                    "num_predict": self._config.max_tokens,
                },
            },
            timeout=self._config.timeout,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]