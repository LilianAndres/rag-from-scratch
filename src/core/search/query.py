from dataclasses import dataclass, field


@dataclass
class SearchQuery:
    text: str
    top_k: int = 5
    filters: dict = field(default_factory=dict)