from typing import List

from src.core.domain import Document, Chunk
from src.core.embeddings.embedding import Embedding
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
        chunker: BaseChunker,
        embedder: BaseEmbedder,
        vectorstore: BaseVectorStore,
        model_name: str,
    ):
        self.chunker = chunker
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.model_name = model_name

    def ingest(self, documents: List[Document]) -> List[Chunk]:
        """
        Ingest a batch of documents: chunk, embed, and index.
        Returns the list of chunks.
        """
        all_chunks: List[Chunk] = self.chunker.chunk_many(documents)

        if not all_chunks:
            return []

        embeddings: List[Embedding] = self.embedder.embed_chunks(all_chunks, model_name=self.model_name)

        self.vectorstore.add_chunks(all_chunks, embeddings)

        return all_chunks