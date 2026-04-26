from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings, SettingsConfigDict,
    PydanticBaseSettingsSource, YamlConfigSettingsSource, EnvSettingsSource,
)
from app.config.models.provider import ProvidersConfig

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ROOT_ENV = Path(__file__).parent.parent / ".env"


class OpenAIJudgeConfig(BaseModel):
    model: str = "gpt-4o-mini"
    temperature: float = 0.0


class OllamaJudgeConfig(BaseModel):
    model: str = "llama3:8b"
    temperature: float = 0.0


class JudgeLLMConfig(BaseModel):
    provider: str = "ollama"
    openai: OpenAIJudgeConfig | None = None
    ollama: OllamaJudgeConfig = OllamaJudgeConfig()


class EvalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=str(ROOT_ENV),
        env_file_encoding="utf-8",
    )

    dataset_path: Path = Path("eval/dataset/questions.yaml")
    output_path: Path = Path("eval/results/latest.json")

    top_k: int = 5
    top_n: int | None = None

    judge: JudgeLLMConfig = JudgeLLMConfig()
    providers: ProvidersConfig = ProvidersConfig()  # shared with app module

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        **kwargs,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            EnvSettingsSource(settings_cls),
            YamlConfigSettingsSource(settings_cls, yaml_file=CONFIG_PATH),
        )