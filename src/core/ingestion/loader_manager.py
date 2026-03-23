from pathlib import Path

from src.loaders.loader import BaseLoader
from src.registry.loader_registry import loader_registry


class DefaultLoaderManager:
    """
    Handles loading files into Document objects using registered loaders.
    """

    def load(self, path: Path) -> list:
        loader_type = self._determine_loader_type(path)
        loader_cls = loader_registry.get(loader_type)
        if not loader_cls:
            raise ValueError(f"No loader registered for file type {loader_type}")
        loader: BaseLoader = loader_cls()
        return loader.load(path)

    def _determine_loader_type(self, path: Path) -> str:
        """
        Default strategy: use file extension without dot.
        """
        return path.suffix.lower()[1:]