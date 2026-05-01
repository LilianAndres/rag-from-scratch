from ragas.llms import InstructorBaseRagasLLM
from eval.config.settings import EvalSettings
from eval.factories.client_factory import ClientFactory


class JudgeLLMFactory:

    def __init__(self, settings: EvalSettings) -> None:
        self._settings = settings

    def create(self) -> InstructorBaseRagasLLM:
        from ragas.llms import llm_factory
        cfg = self._settings.judge_llm
        client = ClientFactory(self._settings).create(cfg.provider)
        match cfg.provider:
            case "openai":
                model = cfg.openai.model
            case "ollama":
                model = cfg.ollama.model
            case _:
                raise ValueError(f"Unsupported LLM provider: {cfg.provider!r}")
        return llm_factory(model=model, provider="openai", client=client)