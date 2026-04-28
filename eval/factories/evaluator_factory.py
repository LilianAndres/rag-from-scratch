from eval.config.settings import EvalSettings
from eval.evaluators.base_evaluator import BaseEvaluator
from eval.factories import LLMFactory, EmbeddingsFactory
from eval.factories.metric_factory import MetricFactory


class EvaluatorFactory:

    def __init__(self, settings: EvalSettings) -> None:
        self._settings = settings

    def create(self) -> BaseEvaluator:
        llm = LLMFactory(self._settings).create()
        embeddings = EmbeddingsFactory(self._settings).create()

        factory = MetricFactory(llm=llm, embeddings=embeddings)
        metrics = [
            factory.create(mc.name, mc.params)
            for mc in self._settings.metrics
        ]
        return BaseEvaluator(metrics)