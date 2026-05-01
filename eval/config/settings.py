from pathlib import Path
from pydantic_settings import (
    BaseSettings, SettingsConfigDict,
    PydanticBaseSettingsSource, YamlConfigSettingsSource,
)

from app.config.models.embedder import EmbedderConfig
from app.config.models.llm import LLMProfileConfig
from app.config.models.provider import ProvidersConfig
from eval.config.models import MetricConfig

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ROOT = Path(__file__).parent.parent.parent

class EvalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=[str(ROOT / ".env")],
        env_file_encoding="utf-8",
        extra="ignore",
    )

    dataset_path: Path
    results_dir: Path
    batch_size: int = 5

    top_k: int = 5
    top_n: int | None = None

    providers: ProvidersConfig = ProvidersConfig() # shared configuration with app/

    judge_llm: LLMProfileConfig = LLMProfileConfig()
    judge_embeddings: EmbedderConfig = EmbedderConfig()

    metrics: list[MetricConfig] = []

    reporters: list[str] = ["console"]

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            **kwargs,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,  # highest priority (programmatic override)
            env_settings,  # real environment variables
            dotenv_settings,  # .env / .env.test
            YamlConfigSettingsSource(settings_cls, yaml_file=CONFIG_PATH),  # base config
        )