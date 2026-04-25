from config.models.query_transformer import QueryTransformerConfig
from src.core.interfaces import BaseLanguageModel
from src.core.interfaces.query_transformer import BaseQueryTransformer
from src.core.prompts.prompt_loader import PromptLoader


class QueryTransformerFactory:
    def __init__(self, config: QueryTransformerConfig, llm: BaseLanguageModel | None):
        self._config = config
        self._llm = llm

    def create(self) -> BaseQueryTransformer:
        if not self._config.enabled:
            from src.query_transformers.passthrough_transformer import PassthroughTransformer
            return PassthroughTransformer()

        match self._config.provider:
            case "multi-query":
                from src.query_transformers.multi_query_transformer import MultiQueryTransformer
                prompt_loader = PromptLoader(self._config.prompts_dir)
                return MultiQueryTransformer(
                    config=self._config.multi_query,
                    llm=self._llm,
                    prompt_loader=prompt_loader,
                )
            case _:
                raise ValueError(
                    f"Unknown query transformer provider: {self._config.provider!r}"
                )