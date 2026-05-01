from typing import Iterator

from app.src.core.domain.document import Document, RawDocument
from app.src.core.interfaces.parser import BaseParser


class PlainTextParser(BaseParser):

    def can_handle(self, raw: RawDocument) -> bool:
        return (raw.mime_type or "").startswith("text/")

    def parse(self, raw: RawDocument) -> Iterator[Document]:
        with raw.content.open() as f:
            for line_num, line in enumerate(f):
                text = line.decode("utf-8", errors="replace").strip()
                if text:
                    yield Document(
                        content=text,
                        metadata={
                            **vars(raw.metadata),
                            "line": line_num + 1,
                        },
                    )