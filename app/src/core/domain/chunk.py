from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4


@dataclass
class Chunk:
    document_id: UUID
    content: str
    id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)