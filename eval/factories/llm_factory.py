from ragas.llms import InstructorBaseRagasLLM

from eval.config.settings import EvalSettings


class JudgeLLMFactory:

    def __init__(self, settings: EvalSettings) -> None:
        self._settings = settings

    def create(self) -> InstructorBaseRagasLLM:
        from openai import AsyncOpenAI
        from ragas.llms import llm_factory
        cfg = self._settings.judge_llm
        match cfg.provider:
            case "openai":
                client = AsyncOpenAI(
                    api_key=self._settings.providers.openai.api_key.get_secret_value(),
                    base_url=self._settings.providers.openai.base_url,
                )
                model = cfg.openai.model
            case "ollama":
                client = AsyncOpenAI(
                    api_key="ollama",
                    base_url=self._settings.providers.ollama.base_url,
                )
                model = cfg.ollama.model
            case _:
                raise ValueError(f"Unsupported LLM provider: {cfg.provider!r}")

        # RAGAS only uses provider to detect Google/Gemini adapters.
        # For OpenAI-compatible clients (including Ollama), "openai" is the correct value.
        return llm_factory(model=model, provider="openai", client=client)
