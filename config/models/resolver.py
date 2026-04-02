from pydantic import BaseModel


class LocalResolverConfig(BaseModel):
    base_path: str


class ResolverConfig(BaseModel):
    local: LocalResolverConfig | None = None