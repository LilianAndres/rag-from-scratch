from dataclasses import dataclass, field
from typing import Any
from datetime import datetime


@dataclass
class Embedding:
    chunk_id: str
    vector: list[float]
    model_name: str
    metadata: dict[str, Any] = field(default_factory=dict)