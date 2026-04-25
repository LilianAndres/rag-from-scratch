from src.core.interfaces import BaseLanguageModel
from src.core.interfaces.generator import BaseGenerator
from src.core.prompts.prompt_loader import PromptLoader
from src.core import GenerationResult, SearchResult
from config.models.generator import GeneratorConfig


class RAGGenerator(BaseGenerator):
    """
    Single, provider-agnostic generator.
    """

    def __init__(self, config: GeneratorConfig, llm: BaseLanguageModel, prompt_loader: PromptLoader):
        self._config = config
        self._llm = llm
        self._prompt_loader = prompt_loader

    def generate(self, query: str, context: list[SearchResult]) -> GenerationResult:
        prompt = self._prompt_loader.render(self._config.prompt_template, query=query, context=context)
        answer = self._llm.complete(prompt)
        return GenerationResult(
            answer=answer,
            sources=context,
            metadata={"prompt_template": self._config.prompt_template},
        )