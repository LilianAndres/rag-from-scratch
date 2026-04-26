from pydantic import BaseModel


class LocalResolverConfig(BaseModel):
    base_path: str = "/tmp"


class ResolverConfig(BaseModel):
    local: LocalResolverConfig = LocalResolverConfig()