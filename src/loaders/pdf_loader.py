import hashlib
from pathlib import Path

import pymupdf

from src.core.domain.document import Document
from src.core.interfaces.loader import BaseLoader


class PDFLoader(BaseLoader):
    """
    Loads PDF files into Document objects using PyMuPDF.

    Each page is extracted as a separate Document, carrying the page text
    as its content and a metadata dict with source path, page number, and
    basic PDF-level metadata (title, author, etc.).

    Parameters
    ----------
    page_separator : str
        String inserted between text blocks within a single page.
        Defaults to ``"\\n"``.
    """

    def __init__(self, *, page_separator: str = "\n") -> None:
        self.page_separator = page_separator

    def load(self, source: str | Path) -> list[Document]:
        path = self._validate(source)

        with pymupdf.open(path) as doc:
            pdf_meta = self._extract_metadata(doc, path)
            documents = [self._page_to_document(page, pdf_meta) for page in doc]

        non_empty = [d for d in documents if d.content.strip()]
        return non_empty

    @staticmethod
    def _validate(source: str | Path) -> Path:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a .pdf file, got: {path.suffix!r}")
        return path

    @staticmethod
    def _make_id(source: str, page_number: int) -> str:
        """
        Build a stable, collision-resistant document ID.

        Using SHA-1 (truncated to 16 hex chars) keeps IDs short while
        being virtually collision-free across any realistic corpus.
        Format: ``pdf-<hash>-p<page>``, e.g. ``pdf-3a5f9c1b2e4d7a8f-p0``.
        """
        digest = hashlib.sha1(source.encode()).hexdigest()[:16]
        return f"pdf-{digest}-p{page_number}"

    @staticmethod
    def _extract_metadata(doc: pymupdf.Document, path: Path) -> dict:
        """
        Extract metadata from a PDF file and return as a dict.
        """
        raw = doc.metadata or {}
        return {
            "source": str(path),
            "total_pages": doc.page_count,
            "title": raw.get("title") or None,
            "author": raw.get("author") or None,
            "subject": raw.get("subject") or None,
            "creator": raw.get("creator") or None,
            "producer": raw.get("producer") or None,
            "creation_date": raw.get("creationDate") or None,
            "modification_date": raw.get("modDate") or None,
        }

    def _page_to_document(self, page: pymupdf.Page, pdf_meta: dict) -> Document:
        """
        Convert a PDF file page to a Document object.
        """
        text = self._extract_text(page)
        metadata = {
            **pdf_meta,
            "page": page.number,          # 0-based
            "page_label": page.number + 1, # human-friendly 1-based
        }
        doc_id = self._make_id(pdf_meta["source"], page.number)
        return Document(id=doc_id, content=text, metadata=metadata)

    def _extract_text(self, page: pymupdf.Page) -> str:
        """
        Return the textual content of *page* with order preserved.
        Image blocks are ignored.
        """
        blocks = page.get_text("blocks", sort=True)
        parts: list[str] = []

        for block in blocks:
            # block layout: (x0, y0, x1, y1, text_or_None, block_no, block_type)
            # block_type: 0 = text, 1 = image
            block_type: int = block[6]
            if block_type == 0:
                text: str = block[4].strip()
                if text:
                    parts.append(text)

        return self.page_separator.join(parts)