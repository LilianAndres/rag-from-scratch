from config.models.generator import GeneratorConfig
from src.core.interfaces.generator import BaseGenerator
from src.core.prompts.prompt_loader import PromptLoader


class GeneratorFactory:
    def __init__(self, config: GeneratorConfig) -> None:
        self._config = config
        self._prompt_loader = PromptLoader(prompts_dir=config.prompts_dir)

    def create_generator(self) -> BaseGenerator:
        match self._config.provider:
            case "openai":
                from src.generators.openai_generator import OpenAIGenerator

                if self._config.openai is None:
                    raise ValueError("Missing OpenAI config")

                return OpenAIGenerator(
                    config=self._config.openai,
                    prompt_loader=self._prompt_loader
                )

            case "ollama":
                from src.generators.ollama_generator import OllamaGenerator

                if self._config.ollama is None:
                    raise ValueError("Missing Ollama config")

                return OllamaGenerator(
                    config=self._config.ollama,
                    prompt_loader=self._prompt_loader
                )

            case _:
                raise ValueError(f"Unknown generator provider: {self._config.provider!r}")