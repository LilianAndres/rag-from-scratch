from app.config.models.generator import GeneratorConfig
from app.src.core.interfaces.generator import BaseGenerator
from app.src.core.interfaces.llm import BaseLanguageModel
from app.src.generators.rag_generator import RAGGenerator
from app.src.prompts.prompt_loader import PromptLoader


class GeneratorFactory:
    def __init__(self, config: GeneratorConfig, llm: BaseLanguageModel):
        self._config = config
        self._llm = llm

    def create_generator(self) -> BaseGenerator:
        prompt_loader = PromptLoader(self._config.prompts_dir)
        return RAGGenerator(config=self._config, llm=self._llm, prompt_loader=prompt_loader)