from pydantic import BaseModel
from .sources import SourceRequest


class IngestRequest(BaseModel):
    sources: list[SourceRequest]


class IngestResponse(BaseModel):
    message: str