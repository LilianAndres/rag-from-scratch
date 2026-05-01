from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Iterator, Generator


class Streamable(ABC):

    @abstractmethod
    @contextmanager
    def open(self) -> Generator[Iterator[bytes], None, None]:
        """
        Open the resource and yield a file-like object.
        """
        pass