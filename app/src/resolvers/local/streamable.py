from contextlib import contextmanager
from typing import Iterator, Generator

from app.src.core.interfaces.streamable import Streamable


class LocalFileStreamable(Streamable):

    def __init__(self, path: str, chunk_size: int = 65536):
        self._path = path
        self._chunk_size = chunk_size

    @contextmanager
    def open(self) -> Generator[Iterator[bytes], None, None]:
        f = builtins_open(self._path, "rb")
        try:
            yield f
        finally:
            f.close()


# alias to avoid shadowing built-in open
import builtins
builtins_open = builtins.open