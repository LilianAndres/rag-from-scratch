from pathlib import Path

from src.registry.resolver_registry import resolver_registry
from src.resolvers import BaseSourceResolver


@resolver_registry.register("file")
class LocalResolver(BaseSourceResolver):
    def resolve(self, source: str) -> Path:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Local file not found: {source}")
        return path