from pathlib import Path
from pydantic_settings import (
    BaseSettings, SettingsConfigDict,
    PydanticBaseSettingsSource, YamlConfigSettingsSource,
)
from app.config.models.provider import ProvidersConfig
from eval.config.models import JudgeLLMConfig

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ROOT = Path(__file__).parent.parent.parent

class EvalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=[
            str(ROOT / ".env.secrets"),
            str(ROOT / ".env.providers"),
        ],
        env_file_encoding="utf-8",
    )

    dataset_path: Path = Path("eval/dataset/questions.yaml")
    results_dir: Path = Path("eval/results")
    batch_size: int = 5

    top_k: int = 5
    top_n: int | None = None

    judge: JudgeLLMConfig = JudgeLLMConfig()
    providers: ProvidersConfig = ProvidersConfig()

    reporters: list[str] = ["json", "csv", "console"]

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