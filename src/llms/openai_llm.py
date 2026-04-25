from openai import OpenAI

from src.core.interfaces import BaseLanguageModel
from config.models.llm import OpenAIProfileConfig


class OpenAIClient(BaseLanguageModel):
    """
    LLM client backed by the OpenAI Chat Completions API.
    """

    def __init__(self, config: OpenAIProfileConfig):
        self._config = config
        self._client = OpenAI(api_key=config.api_key.get_secret_value())

    def complete(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._config.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self._config.temperature,
            max_tokens=self._config.max_tokens,
        )
        return response.choices[0].message.content or ""