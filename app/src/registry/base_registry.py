from typing import TypeVar, Generic


T = TypeVar("T")

class BaseRegistry(Generic[T]):
    """
    Generic registry mapping string keys to classes or callables.
    """

    def __init__(self) -> None:
        self._registry: dict[str, T] = {}

    def register(self, name: str, instance: T) -> None:
        self._registry[name] = instance

    def get(self, name: str) -> T:
        if name not in self._registry:
            raise ValueError(f"No component registered under '{name}'")
        return self._registry[name]

    def list(self) -> list[str]:
        return list(self._registry.keys())