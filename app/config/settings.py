from pathlib import Path

from pydantic_settings import (
    BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource,
    YamlConfigSettingsSource, EnvSettingsSource,
)

from app.config.models import (
    ResolverConfig, LoaderConfig, ChunkerConfig, EmbedderConfig, BackendConfig,
    GeneratorConfig, RerankerConfig, LLMsConfig, QueryTransformerConfig,
)

CONFIG_PATH = Path(__file__).parent / "config.yaml"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8")

    resolvers: ResolverConfig
    loaders: LoaderConfig
    chunker: ChunkerConfig
    embedder: EmbedderConfig
    backend: BackendConfig
    generator: GeneratorConfig
    reranker: RerankerConfig
    llms: LLMsConfig
    query_transformer: QueryTransformerConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        **kwargs,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            EnvSettingsSource(settings_cls), # highest priority
            YamlConfigSettingsSource(settings_cls, yaml_file=CONFIG_PATH),
        )