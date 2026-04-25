from pydantic import BaseModel


class RecursiveChunkerConfig(BaseModel):
    chunk_size: int = 400
    chunk_overlap: int = 50
    separators: list[str] | None = None


class ChunkerConfig(BaseModel):
    provider: str = "recursive"
    recursive: RecursiveChunkerConfig = RecursiveChunkerConfig()