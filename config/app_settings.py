from pydantic_settings import (
    BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource,
    YamlConfigSettingsSource, EnvSettingsSource,
)

from config.models import (
    ResolverConfig, LoaderConfig, ChunkerConfig, EmbedderConfig, BackendConfig,
    GeneratorConfig, RerankerConfig, LLMsConfig, QueryTransformerConfig,
)


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
            YamlConfigSettingsSource(settings_cls, yaml_file="config.yaml"),
        )