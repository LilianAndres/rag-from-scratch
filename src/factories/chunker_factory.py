from config.models.chunker import ChunkerConfig
from src.core.interfaces.chunker import BaseChunker


class ChunkerFactory:
    def __init__(self, config: ChunkerConfig) -> None:
        self._config = config

    def create_chunker(self) -> BaseChunker:
        match self._config.provider:
            case "recursive":
                from src.chunkers.recursive_chunker import RecursiveChunker
                return RecursiveChunker(self._config.recursive)
            case _:
                raise ValueError(
                    f"Unknown chunker provider: {self._config.provider!r}"
                )