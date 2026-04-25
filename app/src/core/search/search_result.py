from dataclasses import dataclass, field
from app.src.core.domain.chunk import Chunk


@dataclass
class SearchResult:
    chunk: Chunk
    score: float | None = None
    metadata: dict = field(default_factory=dict)