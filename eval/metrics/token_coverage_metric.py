from eval.domain.pipeline_output import PipelineOutput
from eval.interfaces.metric import Metric


class TokenCoverageMetric(Metric):
    """
    Fraction of ground-truth tokens that appear anywhere in the retrieved contexts.
    A proxy for retrieval recall that requires no LLM call.
    Low score → your retriever is not surfacing the relevant passages at all.
    """

    @property
    def name(self) -> str:
        return "context_token_coverage"

    async def score(self, output: PipelineOutput) -> float:
        gt_tokens = set(output.ground_truth.lower().split())
        ctx_tokens = set(" ".join(output.contexts).lower().split())
        if not gt_tokens:
            return 0.0
        return len(gt_tokens & ctx_tokens) / len(gt_tokens)