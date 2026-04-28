from eval.interfaces.metric import Metric


class MetricFactory:

    def __init__(self, llm, embeddings) -> None:
        self._llm = llm
        self._embeddings = embeddings

    def create(self, name: str, params: dict) -> Metric:
        match name:
            case "faithfulness":
                from ragas.metrics.collections import Faithfulness
                from eval.metrics.faithfulness import FaithfulnessMetric
                return FaithfulnessMetric(Faithfulness(llm=self._llm))

            case "answer_relevancy":
                from ragas.metrics.collections import AnswerRelevancy
                from eval.metrics.answer_relevancy import AnswerRelevancyMetric
                return AnswerRelevancyMetric(
                    AnswerRelevancy(llm=self._llm, embeddings=self._embeddings)
                )

            case "context_recall":
                from ragas.metrics.collections import ContextRecall
                from eval.metrics.context_recall import ContextRecallMetric
                return ContextRecallMetric(ContextRecall(llm=self._llm))

            case "factual_correctness":
                from ragas.metrics.collections import FactualCorrectness
                from eval.metrics.factual_correctness import FactualCorrectnessMetric
                return FactualCorrectnessMetric(FactualCorrectness(llm=self._llm))

            case "token_coverage":
                from eval.metrics.token_coverage_metric import TokenCoverageMetric
                return TokenCoverageMetric()

            case "latency":
                from eval.metrics.latency_metric import LatencyMetric
                return LatencyMetric(threshold_ms=params.get("threshold_ms", 2000.0))

            case _:
                raise ValueError(f"Unknown metric: {name!r}")