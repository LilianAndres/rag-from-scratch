from pathlib import Path

from pydantic_settings import (
    BaseSettings, SettingsConfigDict,
    PydanticBaseSettingsSource, YamlConfigSettingsSource,
)

from app.config.models import (
    ResolverConfig, LoaderConfig, ChunkerConfig, EmbedderConfig, BackendConfig,
    GeneratorConfig, RerankerConfig, LLMsConfig, QueryTransformerConfig, ProvidersConfig,
)

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ROOT = Path(__file__).parent.parent.parent

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=[str(ROOT / ".env")],
        env_file_encoding="utf-8",
    )

    env: str = "dev"
    port: int = 8000

    resolvers: ResolverConfig = ResolverConfig()
    loaders: LoaderConfig = LoaderConfig()
    chunker: ChunkerConfig = ChunkerConfig()
    embedder: EmbedderConfig = EmbedderConfig()
    reranker: RerankerConfig = RerankerConfig()
    providers: ProvidersConfig = ProvidersConfig()
    query_transformer: QueryTransformerConfig = QueryTransformerConfig()
    llms: LLMsConfig = LLMsConfig()

    backend: BackendConfig
    generator: GeneratorConfig

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