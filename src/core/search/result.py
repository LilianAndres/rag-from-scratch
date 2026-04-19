from dataclasses import dataclass, field
from src.core.domain.chunk import Chunk


@dataclass
class SearchResult:
    chunk: Chunk
    score: float | None = None
    metadata: dict = field(default_factory=dict)