import hashlib

from app.config.models.chunker import RecursiveChunkerConfig
from app.src.core.domain import Document, Chunk
from app.src.core.interfaces.chunker import BaseChunker


class RecursiveChunker(BaseChunker):
    """
    Splits documents recursively on natural text boundaries.
    Supports a token overlap window to preserve cross-chunk context.
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, config: RecursiveChunkerConfig):
        self._config = config

    def chunk(self, document: Document) -> list[Chunk]:
        raw_splits = self._split_text(document.content, self._config.separators or self.DEFAULT_SEPARATORS)
        merged_splits = self._merge_splits(raw_splits)
        return [
            Chunk(
                id=self._make_chunk_id(document.id, i),
                content=text,
                document_id=document.id,
                metadata={
                    **document.metadata,
                    "chunk_index": i,
                    "chunk_total": len(merged_splits),
                },
            )
            for i, text in enumerate(merged_splits)
        ]

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        """
        Recursively split *text* using the first separator that actually
        divides it, then recurse on any piece that is still too large.
        """
        # Find the best separator that exists in the text
        separator = separators[-1] # fallback: split char-by-char
        remaining = separators
        for sep in separators:
            if sep == "" or sep in text:
                separator = sep
                remaining = separators[separators.index(sep) + 1:]
                break

        splits = text.split(separator) if separator else list(text)

        final: list[str] = []
        good: list[str] = [] # splits that fit on their own

        for split in splits:
            if len(split) < self._config.chunk_size:
                good.append(split)
            else:
                # Too large: flush good splits first, then recurse
                if good:
                    final.extend(good)
                    good = []
                final.extend(self._split_text(split, remaining))

        if good:
            final.extend(good)

        return [s for s in final if s.strip()]

    def _merge_splits(self, splits: list[str]) -> list[str]:
        """
        Greedily merge small splits into chunks up to *chunk_size*,
        with an *overlap* window carried forward.
        """
        chunks: list[str] = []
        current: list[str] = []
        current_len = 0

        for split in splits:
            split_len = len(split)

            if current_len + split_len > self._config.chunk_size and current:
                chunks.append(" ".join(current))
                # Carry overlap: keep trailing splits that fit the window
                while current and current_len > self._config.chunk_overlap:
                    current_len -= len(current[0])
                    current.pop(0)

            current.append(split)
            current_len += split_len

        if current:
            chunks.append(" ".join(current))

        return chunks

    @staticmethod
    def _make_chunk_id(doc_id: str, index: int) -> str:
        """
        Stable chunk ID derived from its parent doc ID and position.
        Format: chunk-<hash>-c<index>, e.g. chunk-3a5f9c1b2e4d7a8f-c0
        """
        digest = hashlib.sha1(f"{doc_id}:{index}".encode()).hexdigest()[:16]
        return f"chunk-{digest}-c{index}"