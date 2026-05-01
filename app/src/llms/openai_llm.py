from openai import OpenAI

from app.config.models.provider import OpenAIProviderConfig
from app.config.models.llm import OpenAIProfileConfig
from app.src.core.interfaces.llm import BaseLanguageModel


class OpenAIClient(BaseLanguageModel):
    """
    LLM client backed by the OpenAI Chat Completions API.
    """

    def __init__(self, config: OpenAIProfileConfig, provider: OpenAIProviderConfig):
        self._model = config.model
        self._temperature = config.temperature
        self._max_tokens = config.max_tokens
        self._client = OpenAI(
            api_key=provider.api_key.get_secret_value(),
            base_url=provider.base_url,
        )

    def complete(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self._temperature,
            max_tokens=self._max_tokens,
        )
        return response.choices[0].message.content or ""