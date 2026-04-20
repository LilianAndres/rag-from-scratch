import httpx

from src.core.interfaces.generator import BaseGenerator
from src.core.prompts.prompt_loader import PromptLoader
from src.core import GenerationResult, SearchResult
from config.models.generator import OllamaGeneratorConfig


class OllamaGenerator(BaseGenerator):
    """
    Generator backed by a local Ollama instance.
    Requires Ollama running at config.base_url.
    """

    def __init__(self, config: OllamaGeneratorConfig, prompt_loader: PromptLoader):
        self._config = config
        self._prompt_loader = prompt_loader

    def generate(self, query: str, context: list[SearchResult]) -> GenerationResult:
        prompt = self._prompt_loader.render(self._config.prompt_template, query=query, context=context)

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
        data = response.json()

        answer = data["message"]["content"]
        usage = data.get("usage", {})

        return GenerationResult(
            answer=answer,
            sources=context,
            metadata={
                "model": self._config.model,
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "finish_reason": data.get("done_reason"),
            },
        )