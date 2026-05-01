from abc import ABC, abstractmethod
from typing import Iterator

from app.src.core.domain.document import RawDocument
from app.src.core.domain.source import SourceDescriptor


class BaseSourceResolver(ABC):

    @abstractmethod
    def discover(self, descriptor: SourceDescriptor) -> Iterator[RawDocument]:
        """
        Discover all files at the source location described
        by the descriptor and yield RawDocuments.
        """
        pass