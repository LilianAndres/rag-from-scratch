from pathlib import Path

from app.config.models.resolver import LocalResolverConfig
from app.src.core.interfaces.resolver import BaseSourceResolver


class LocalResolver(BaseSourceResolver):

    def __init__(self, config: LocalResolverConfig) -> None:
        self._base_path = Path(config.base_path)

    def resolve(self, source: str) -> Path:
        path = self._base_path / source
        if not path.exists():
            raise FileNotFoundError(f"Local file not found: {path}")
        return path