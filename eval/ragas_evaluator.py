from ragas.llms import llm_factory
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, ResponseRelevancy

from eval.eval_runner import PipelineOutput
from eval.settings import EvalSettings


def _build_llm(settings: EvalSettings):
    match settings.judge.provider:
        case "openai":
            if settings.providers.openai is None:
                raise ValueError(
                    "OpenAI credentials not configured. "
                    "Set PROVIDERS__OPENAI__API_KEY in your environment."
                )
            from openai import OpenAI
            client = OpenAI(
                api_key=settings.providers.openai.api_key.get_secret_value(),
                base_url=settings.providers.openai.base_url,
            )
            return llm_factory(
                model=settings.judge.openai.model,
                provider="openai",
                client=client,
            )
        case "ollama":
            from ollama import Client
            client = Client(host=settings.providers.ollama.base_url)
            return llm_factory(
                model=settings.judge.ollama.model,
                provider="ollama",
                client=client,
            )
        case _:
            raise ValueError(f"Unknown judge provider: {settings.judge.provider!r}")


class RagasEvaluator:

    def __init__(self, settings: EvalSettings):
        self._llm = _build_llm(settings)
        self._metrics = [
            Faithfulness(llm=self._llm),
            ResponseRelevancy(llm=self._llm),
            LLMContextRecall(llm=self._llm),
            FactualCorrectness(llm=self._llm),
        ]

    async def evaluate(self, outputs: list[PipelineOutput]) -> list[dict]:
        results = []
        for output in outputs:
            row = {}
            for metric in self._metrics:
                result = await metric.ascore(
                    response=output.answer,
                    retrieved_contexts=output.contexts,
                    reference=output.ground_truth,
                    user_input=output.question,
                )
                row[metric.name] = result.score
            results.append({"question": output.question, **row})
        return results