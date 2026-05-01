from typing import Iterator

import pymupdf

from app.config.models.parser import PDFParserConfig
from app.src.core.domain.document import Document, RawDocument
from app.src.core.interfaces.parser import BaseParser


class PDFParser(BaseParser):

    def __init__(self, config: PDFParserConfig) -> None:
        self.page_separator: str = config.page_separator

    def can_handle(self, raw: RawDocument) -> bool:
        return raw.mime_type == "application/pdf"

    def parse(self, raw: RawDocument) -> Iterator[Document]:
        with raw.content.open() as f:
            data = f.read()

        with pymupdf.open(stream=data, filetype="pdf") as doc:
            pdf_meta = self._extract_metadata(doc, raw.source_uri)
            documents = [self._page_to_document(page, pdf_meta) for page in doc]

        return iter(d for d in documents if d.content.strip())

    @staticmethod
    def _extract_metadata(doc: pymupdf.Document, source_uri: str) -> dict:
        raw = doc.metadata or {}
        return {
            "source": source_uri,
            "total_pages": doc.page_count,
            "title": raw.get("title") or None,
            "author": raw.get("author") or None,
            "subject": raw.get("subject") or None,
            "creator": raw.get("creator") or None,
            "producer": raw.get("producer") or None,
            "created_at": raw.get("creationDate") or None,
            "updated_at": raw.get("modDate") or None,
        }

    def _page_to_document(self, page: pymupdf.Page, pdf_meta: dict) -> Document:
        text = self._extract_text(page)
        metadata = {
            **pdf_meta,
            "page": page.number,
            "page_label": page.number + 1,
        }
        return Document(content=text, metadata=metadata)

    def _extract_text(self, page: pymupdf.Page) -> str:
        blocks = page.get_text("blocks", sort=True)
        parts: list[str] = []
        for block in blocks:
            if block[6] == 0:
                text: str = block[4].strip()
                if text:
                    parts.append(text)
        return self.page_separator.join(parts)