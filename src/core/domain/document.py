from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """Represents a unit of text with associated metadata."""

    content: str
    id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        preview = self.content[:80].replace("\n", " ")
        return f"Document(id={self.doc_id!r}, preview={preview!r})"