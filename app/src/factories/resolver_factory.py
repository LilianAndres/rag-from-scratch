from app.config.models import ResolverConfig
from app.src.registry import BaseRegistry
from app.src.resolvers import LocalResolver


class ResolverFactory:
    def __init__(self, config: ResolverConfig) -> None:
        self._config = config

    def build_registry(self) -> BaseRegistry:
        registry = BaseRegistry()
        registry.register("file",  LocalResolver(config=self._config.local))
        return registry