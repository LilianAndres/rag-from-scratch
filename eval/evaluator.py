from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.llms import LangchainLLMWrapper

from eval.settings import EvalSettings, JudgeLLMConfig
from eval.runner import PipelineOutput


def _build_llm_wrapper(config: JudgeLLMConfig) -> LangchainLLMWrapper:
    match config.provider:
        case "openai":
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model=config.openai.model,
                temperature=config.openai.temperature,
                api_key=config.openai.api_key
            )
        case "ollama":
            from langchain_ollama import ChatOllama
            llm = ChatOllama(
                model=config.ollama.model,
                base_url=config.ollama.base_url,
                temperature=config.ollama.temperature,
            )
        case _:
            raise ValueError(f"Unknown judge LLM provider: {config.provider!r}")
    return LangchainLLMWrapper(llm)


class RagasEvaluator:

    def __init__(self, settings: EvalSettings):
        self._llm = _build_llm_wrapper(settings.judge)
        self._metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ]

    def evaluate(self, outputs: list[PipelineOutput]) -> dict:
        dataset = Dataset.from_dict({
            "question":     [o.question     for o in outputs],
            "answer":       [o.answer       for o in outputs],
            "contexts":     [o.contexts     for o in outputs],
            "ground_truth": [o.ground_truth for o in outputs],
        })
        return evaluate(
            dataset=dataset,
            metrics=self._metrics,
            llm=self._llm,
        )