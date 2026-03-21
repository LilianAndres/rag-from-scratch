from dataclasses import dataclass, field
from typing import Any

from src.core import RetrievedChunk


@dataclass
class GenerationResult:
    answer: str
    sources: list[RetrievedChunk] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)