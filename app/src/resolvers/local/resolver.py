import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Iterator

from app.src.core.domain.document import RawDocument
from app.src.core.interfaces.source import BaseSourceResolver
from app.src.resolvers.local.descriptor import LocalSourceDescriptor
from app.src.resolvers.local.streamable import LocalFileStreamable


class LocalSourceResolver(BaseSourceResolver):

    def discover(self, descriptor: LocalSourceDescriptor) -> Iterator[RawDocument]:
        root = Path(descriptor.path)

        if root.is_file():
            yield self._make_raw_document(root)
            return

        pattern = descriptor.glob_pattern if descriptor.recursive else "*"
        for path in root.glob(pattern):
            if path.is_file():
                yield self._make_raw_document(path)

    def _make_raw_document(self, path: Path) -> RawDocument:
        mime_type, _ = mimetypes.guess_type(str(path))
        return RawDocument(
            source_uri=f"local://{path.resolve()}",
            source_type="local",
            mime_type=mime_type,
            content=LocalFileStreamable(str(path.resolve())),
            metadata={
                "filename": path.name,
                "ingested_at": datetime.utcnow().isoformat(),
            },
        )