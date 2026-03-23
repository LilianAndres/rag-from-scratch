from typing import Callable, Dict, TypeVar, Type

from src.meta.singleton_meta import SingletonMeta


T = TypeVar("T")

class BaseRegistry(metaclass=SingletonMeta):
    """
    Generic registry mapping string keys to classes or callables.
    """

    def __init__(self):
        self._registry: Dict[str, Callable] = {}

    def register(self, name: str):
        def decorator(cls: Type[T]) -> Type[T]:
            self._registry[name] = cls
            return cls
        return decorator

    def get(self, name: str) -> Callable:
        if name not in self._registry:
            raise ValueError(f"{name} is not registered")
        return self._registry[name]

    def list(self) -> list[str]:
        return list(self._registry.keys())