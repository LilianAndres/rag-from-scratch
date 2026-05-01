from contextlib import contextmanager
from typing import Generator, Iterator

from app.src.core.interfaces.streamable import Streamable


class S3Streamable(Streamable):

    def __init__(self, bucket: str, key: str, client, chunk_size: int = 8 * 1024 * 1024):
        self._bucket = bucket
        self._key = key
        self._client = client
        self._chunk_size = chunk_size

    @contextmanager
    def open(self) -> Generator[Iterator[bytes], None, None]:
        response = self._client.get_object(Bucket=self._bucket, Key=self._key)
        body = response["Body"]
        try:
            yield body
        finally:
            body.close()