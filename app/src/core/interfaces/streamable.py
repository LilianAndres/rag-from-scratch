from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, IO


class Streamable(ABC):

    @abstractmethod
    @contextmanager
    def open(self) -> Generator[IO[bytes], None, None]:
        """
        Open the resource and yield a file-like object.
        """
        pass