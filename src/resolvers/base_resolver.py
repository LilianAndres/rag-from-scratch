from abc import ABC, abstractmethod
from pathlib import Path


class BaseSourceResolver(ABC):
    @abstractmethod
    def resolve(self, source: str) -> Path:
        """
        Resolves a source into a local file path (typically a tmp/ directory).
        """