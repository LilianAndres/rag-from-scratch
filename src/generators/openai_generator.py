from openai import OpenAI

from src.core.interfaces.generator import BaseGenerator
from src.core.prompts.prompt_loader import PromptLoader
from src.core import GenerationResult, SearchResult
from config.models.generator import OpenAIGeneratorConfig


class OpenAIGenerator(BaseGenerator):
    """
    Generator backed by the OpenAI Chat Completions API.
    """

    def __init__(self, config: OpenAIGeneratorConfig, prompt_loader: PromptLoader):
        self._config = config
        self._prompt_loader = prompt_loader
        self._client = OpenAI(api_key=config.api_key.get_secret_value())

    def generate(self, query: str, context: list[SearchResult]) -> GenerationResult:
        prompt = self._prompt_loader.render(self._config.prompt_template, query=query, context=context)

        response = self._client.chat.completions.create(
            model=self._config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self._config.temperature,
            max_tokens=self._config.max_tokens,
        )

        answer = response.choices[0].message.content or ""
        usage = response.usage

        return GenerationResult(
            answer=answer,
            sources=context,
            metadata={
                "model": self._config.model,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason,
            },
        )