from typing import Type

from app.src.core.domain.source import SourceDescriptor
from app.src.core.interfaces.source import BaseSourceResolver


class ResolverRegistry:

    def __init__(self):
        self._registry: dict[Type[SourceDescriptor], BaseSourceResolver] = {}

    def register(self, descriptor_type: Type[SourceDescriptor], resolver: BaseSourceResolver) -> None:
        self._registry[descriptor_type] = resolver

    def resolve(self, descriptor: SourceDescriptor) -> BaseSourceResolver:
        resolver = self._registry.get(type(descriptor))
        if resolver is None:
            raise ValueError(f"No resolver registered for {type(descriptor).__name__}")
        return resolver