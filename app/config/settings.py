from pathlib import Path

from pydantic_settings import (
    BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource,
    YamlConfigSettingsSource, EnvSettingsSource,
)

from app.config.models import (
    ResolverConfig, LoaderConfig, ChunkerConfig, EmbedderConfig, BackendConfig,
    GeneratorConfig, RerankerConfig, LLMsConfig, QueryTransformerConfig, ProvidersConfig,
)

CONFIG_PATH = Path(__file__).parent / "config.yaml"
ROOT_ENV = Path(__file__).parent.parent / ".env"



class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=str(ROOT_ENV),
        env_file_encoding="utf-8",
    )

    resolvers: ResolverConfig = ResolverConfig()
    loaders: LoaderConfig = LoaderConfig()
    chunker: ChunkerConfig = ChunkerConfig()
    embedder: EmbedderConfig = EmbedderConfig()
    backend: BackendConfig = BackendConfig()
    generator: GeneratorConfig = GeneratorConfig()
    reranker: RerankerConfig = RerankerConfig()
    providers: ProvidersConfig = ProvidersConfig()
    query_transformer: QueryTransformerConfig = QueryTransformerConfig()
    llms: LLMsConfig = LLMsConfig()

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