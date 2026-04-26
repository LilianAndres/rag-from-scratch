from abc import ABC, abstractmethod
from pathlib import Path


class BaseSourceResolver(ABC):
    """
    Resolves a source identifier into a local file path.

    A source can be anything — a local path, a remote URL, an S3 URI —
    depending on the concrete implementation. The resolver's responsibility
    is to make that source available as a local file, downloading or copying
    it if necessary.
    """

    @abstractmethod
    def resolve(self, source: str) -> Path:
        """
        Resolve a source identifier into a local file path.

        Args:
            source: A string identifying the source to resolve.
                    The format is implementation-defined (e.g. a file path,
                    a URL, or a cloud storage URI).

        Returns:
            A Path pointing to the resolved local file.

        Raises:
            FileNotFoundError: If the source cannot be located.
            ValueError: If the source format is not supported by this resolver.
        """