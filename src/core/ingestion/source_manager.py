from pathlib import Path
from src.registry.resolver_registry import resolver_registry
from src.resolvers import BaseSourceResolver


class DefaultSourceManager:
    """
    Handles resolving any source string using the registered resolvers.
    """

    def resolve(self, source: str) -> Path:
        """
        Pick the right resolver for the source and return a local path.
        """
        resolver_type = self._determine_resolver_type(source)
        resolver_cls = resolver_registry.get(resolver_type)
        if not resolver_cls:
            raise ValueError(f"No resolver registered for type {resolver_type}")
        resolver: BaseSourceResolver = resolver_cls()
        return resolver.resolve(source)

    def _determine_resolver_type(self, source: str) -> str:
        """
        Example strategy: URI scheme, file prefix, or any custom logic.
        """
        if source.startswith("s3://"):
            return "s3"
        return "file"