from dataclasses import dataclass, field
from typing import Any

from app.src.core.search.search_result import SearchResult


@dataclass
class GenerationResult:
    answer: str
    sources: list[SearchResult] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)