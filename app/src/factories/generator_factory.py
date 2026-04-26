from app.config.models.generator import GeneratorConfig
from app.src.core.interfaces import BaseLanguageModel
from app.src.core.interfaces.generator import BaseGenerator
from app.src.prompts.prompt_loader import PromptLoader
from app.src.generators import RAGGenerator


class GeneratorFactory:
    def __init__(self, config: GeneratorConfig, llm: BaseLanguageModel):
        self._config = config
        self._llm = llm

    def create_generator(self) -> BaseGenerator:
        prompt_loader = PromptLoader(self._config.prompts_dir)
        return RAGGenerator(config=self._config, llm=self._llm, prompt_loader=prompt_loader)