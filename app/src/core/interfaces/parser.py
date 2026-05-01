from abc import ABC, abstractmethod
from typing import Iterator

from app.src.core.domain.document import RawDocument, Document


class BaseParser(ABC):

    @abstractmethod
    def can_handle(self, raw: RawDocument) -> bool:
        pass

    @abstractmethod
    def parse(self, raw: RawDocument) -> Iterator[Document]:
        pass