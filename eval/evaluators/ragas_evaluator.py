from eval.domain import PipelineOutput
from eval.config.settings import EvalSettings
from eval.evaluators.base_evaluator import BaseEvaluator
from eval.interfaces import Metric


class FaithfulnessMetric(Metric):
    def __init__(self, ragas_metric) -> None:
        self._metric = ragas_metric

    @property
    def name(self) -> str:
        return self._metric.name

    async def score(self, output: PipelineOutput) -> float:
        if not output.contexts:
            return 0.0

        result = await self._metric.ascore(
            user_input=output.question,
            response=output.answer,
            retrieved_contexts=output.contexts,
        )

        return result.value


class AnswerRelevancyMetric(Metric):
    def __init__(self, ragas_metric) -> None:
        self._metric = ragas_metric

    @property
    def name(self) -> str:
        return self._metric.name

    async def score(self, output: PipelineOutput) -> float:
        result = await self._metric.ascore(
            user_input=output.question,
            response=output.answer,
        )
        return result.value


class ContextRecallMetric(Metric):
    def __init__(self, ragas_metric) -> None:
        self._metric = ragas_metric

    @property
    def name(self) -> str:
        return self._metric.name

    async def score(self, output: PipelineOutput) -> float:
        if not output.contexts:
            return 0.0

        result = await self._metric.ascore(
            user_input=output.question,
            retrieved_contexts=output.contexts,
            reference=output.ground_truth,
        )

        return result.value


class FactualCorrectnessMetric(Metric):
    def __init__(self, ragas_metric) -> None:
        self._metric = ragas_metric

    @property
    def name(self) -> str:
        return self._metric.name

    async def score(self, output: PipelineOutput) -> float:
        result = await self._metric.ascore(
            response=output.answer,
            reference=output.ground_truth,
        )
        return result.value


def _build_judge_llm(settings: EvalSettings):
    from ragas.llms import llm_factory

    match settings.judge.provider:
        case "openai":
            if settings.providers.openai is None:
                raise ValueError(
                    "OpenAI credentials not configured. "
                    "Set PROVIDERS__OPENAI__API_KEY in your environment."
                )
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key=settings.providers.openai.api_key.get_secret_value(),
                base_url=settings.providers.openai.base_url,
            )
            return llm_factory(
                model=settings.judge.openai.model,
                provider="openai",
                client=client,
            )
        case "ollama":
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key="ollama",
                base_url=f"{settings.providers.ollama.base_url}/v1",
            )
            return llm_factory(
                model=settings.judge.ollama.model,
                provider="openai",
                client=client,
            )
        case _:
            raise ValueError(f"Unknown judge provider: {settings.judge.provider!r}")


def _build_judge_embeddings(settings: EvalSettings):
    from ragas.embeddings.base import embedding_factory

    match settings.judge.provider:
        case "openai":
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key=settings.providers.openai.api_key.get_secret_value(),
                base_url=settings.providers.openai.base_url,
            )
            return embedding_factory(
                model=settings.judge.openai.embedding_model,
                provider="openai",
                client=client,
            )
        case "ollama":
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key="ollama",
                base_url=f"{settings.providers.ollama.base_url}/v1",
            )
            return embedding_factory(
                model=settings.judge.ollama.embedding_model,
                provider="openai",
                client=client,
            )
        case _:
            raise ValueError(f"Unknown judge provider: {settings.judge.provider!r}")


def build_ragas_evaluator(settings: EvalSettings) -> BaseEvaluator:
    from ragas.metrics.collections import (
        Faithfulness,
        AnswerRelevancy,
        ContextRecall,
        FactualCorrectness,
    )

    llm = _build_judge_llm(settings)
    embeddings = _build_judge_embeddings(settings)

    metrics: list[Metric] = [
        FaithfulnessMetric(Faithfulness(llm=llm)),
        AnswerRelevancyMetric(AnswerRelevancy(llm=llm, embeddings=embeddings)),
        ContextRecallMetric(ContextRecall(llm=llm)),
        FactualCorrectnessMetric(FactualCorrectness(llm=llm)),
    ]
    return BaseEvaluator(metrics)