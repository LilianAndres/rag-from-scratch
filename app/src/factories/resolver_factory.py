from app.src.registries.resolver_registry import ResolverRegistry
from app.src.resolvers.local.descriptor import LocalSourceDescriptor
from app.src.resolvers.local.resolver import LocalSourceResolver


class ResolverFactory:

    def build_registry(self) -> ResolverRegistry:
        registry = ResolverRegistry()
        registry.register(LocalSourceDescriptor, LocalSourceResolver())
        return registry