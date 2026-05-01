from typing import Any
from eval.config.settings import EvalSettings


class ClientFactory:

    def __init__(self, settings: EvalSettings) -> None:
        self._settings = settings

    def create(self, provider: str) -> Any:
        from openai import AsyncOpenAI
        match provider:
            case "openai":
                return AsyncOpenAI(
                    api_key=self._settings.providers.openai.api_key.get_secret_value(),
                    base_url=self._settings.providers.openai.base_url,
                )
            case "infinity":
                return AsyncOpenAI(
                    api_key="infinity",
                    base_url=f"{self._settings.providers.infinity.base_url}/v1",
                )
            case _:
                raise ValueError(f"Unknown provider: {provider!r}")