import logging

from app.src.core import SearchQuery
from app.src.core.interfaces import BaseLanguageModel
from app.src.core.interfaces.query_transformer import BaseQueryTransformer
from app.src.prompts.prompt_loader import PromptLoader
from app.config.models.query_transformer import MultiQueryConfig

logger = logging.getLogger(__name__)


class MultiQueryTransformer(BaseQueryTransformer):
    """
    Expands a single query into N rephrased variants using an LLM.
    """

    def __init__(self, config: MultiQueryConfig, llm: BaseLanguageModel, prompt_loader: PromptLoader):
        self._llm = llm
        self._prompt_loader = prompt_loader
        self._n_variants = config.n_variants
        self._prompt_template = config.prompt_template

    def transform(self, query: SearchQuery) -> list[SearchQuery]:
        prompt = self._prompt_loader.render(self._prompt_template, query=query, n=self._n_variants)
        try:
            raw = self._llm.complete(prompt)
            variants = self._parse_variants(raw)
        except Exception as e:
            logger.warning("Multi-query expansion failed, falling back to original: %s", e)
            return [query]

        queries = [query] + [SearchQuery(text=v) for v in variants if v != query.text]
        return queries[: self._n_variants + 1]

    @staticmethod
    def _parse_variants(raw: str) -> list[str]:
        lines = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            for prefix in ("1.", "2.", "3.", "4.", "5.", "-", "*", "•"):
                if line.startswith(prefix):
                    line = line[len(prefix):].strip()
                    break
            if line:
                lines.append(line)
        return lines