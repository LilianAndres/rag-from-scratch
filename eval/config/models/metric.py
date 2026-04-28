from typing import Any
from pydantic import BaseModel


class MetricConfig(BaseModel):
    name: str
    params: dict[str, Any] = {}