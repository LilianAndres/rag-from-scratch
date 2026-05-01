from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from app.src.core.interfaces.streamable import Streamable


@dataclass
class RawDocument:
    source_uri: str
    source_type: str
    mime_type: str | None
    content: Streamable
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Document:
    content: str
    id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        preview = self.content[:80].replace("\n", " ")
        return f"Document(id={self.id!r}, preview={preview!r})"