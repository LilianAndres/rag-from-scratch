from pathlib import Path

from app.src.loaders.loader import BaseLoader
from app.src.registry import BaseRegistry


class DefaultLoaderManager:
    """
    Handles loading files into Document objects using registered loaders.
    """

    def __init__(self, registry: BaseRegistry[BaseLoader]):
        self.registry = registry

    def load(self, path: Path) -> list:
        loader_type = self._determine_loader_type(path)
        loader_instance = self.registry.get(loader_type)
        if not loader_instance:
            raise ValueError(f"No loader registered for file type {loader_type}")
        return loader_instance.load(path)

    def _determine_loader_type(self, path: Path) -> str:
        """
        Default strategy: use file extension without dot.
        """
        return path.suffix.lower()[1:]