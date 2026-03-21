from dataclasses import dataclass, field
from typing import Any


@dataclass
class RetrievedChunk:
    chunk_id: str
    doc_id: str
    content: str
    score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievalResult:
    query: str
    chunks: list[RetrievedChunk]