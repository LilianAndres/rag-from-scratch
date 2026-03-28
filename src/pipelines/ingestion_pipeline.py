from pathlib import Path

from src.core.domain import Document, Chunk
from src.core.embeddings.embedding import Embedding
from src.core.ingestion.loader_manager import DefaultLoaderManager
from src.core.ingestion.source_manager import DefaultSourceManager
from src.core.interfaces.chunker import BaseChunker
from src.core.interfaces.embedder import BaseEmbedder
from src.core.interfaces.vectorstore import BaseVectorStore


class IngestionPipeline:
    """
    Pipeline that ingests raw documents, chunks them,
    computes embeddings, and stores them in a vector store.
    """

    def __init__(
        self,
        resolver: DefaultSourceManager,
        loader: DefaultLoaderManager,
        chunker: BaseChunker,
        embedder: BaseEmbedder,
        vectorstore: BaseVectorStore,
        model_name: str,
    ):
        self.resolver = resolver
        self.loader = loader
        self.chunker = chunker
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.model_name = model_name

    def ingest(self, sources: list[str]) -> None:
        """
        Resolve sources, load documents, then ingest them.
        """
        for source in sources:
            path: Path = self.resolver.resolve(source)
            docs: list[Document] = self.loader.load(path) # load one source at a time
            self._ingest_documents(docs) # document streaming
        return None

    def _ingest_documents(self, documents: list[Document]) -> None:
        """
        Ingest a batch of documents: chunk, embed, and index.
        Returns the list of chunks.
        """
        chunks: list[Chunk] = self.chunker.chunk_many(documents)

        if not chunks:
            return None

        batch_size = 64 # chunk batching (memory-safe)
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            embeddings: list[Embedding] = self.embedder.embed_chunks(batch, self.model_name)
            self.vectorstore.add_chunks(batch, embeddings)

        return None