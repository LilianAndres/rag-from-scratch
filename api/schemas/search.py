from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    top_n: int | None = None


class SourceResponse(BaseModel):
    chunk_id: str
    content: str
    score: float | None
    metadata: dict


class SearchResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]