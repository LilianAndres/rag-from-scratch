# rag-from-scratch

A modular, production-ready **Retrieval-Augmented Generation (RAG)** system built from the ground up in Python. Every component - from document ingestion to answer generation - is cleanly abstracted behind interfaces, making it easy to swap backends, models, and retrieval strategies without touching core logic.

---

## Overview

RAG grounds LLM responses in your own documents by retrieving relevant context at query time. This project implements the full pipeline from scratch:

```
Documents → Load → Chunk → Embed → Store
                                      ↓
              Query → Transform → Retrieve → Rerank → Generate → Answer
```

The architecture is built around **interfaces and factories**: each stage of the pipeline is defined by a clean Python interface and instantiated via a corresponding factory, configured entirely through `config.yaml`.

---

## Features

- **Pluggable vector backends** - Chroma, Elasticsearch (ELK), or Hybrid (both combined)
- **Multiple LLM providers** - OpenAI or Ollama
- **Multiple embedding providers** - OpenAI or Infinity
- **Query transformation** - passthrough or multi-query expansion for improved recall
- **Reranking** - optional cross-encoder reranking via Infinity
- **Document loaders** - PDF support out of the box
- **REST API** - FastAPI-powered ingestion and search endpoints
- **Fully configurable** - swap any component via `config.yaml`, no code changes needed
- **Dockerized** - run the entire stack with a single `docker-compose` command

---

## Project Structure

```
.
├── api/                        # FastAPI application layer
│   ├── app.py                  # App entrypoint & middleware
│   ├── dependencies.py         # Dependency injection
│   ├── schemas.py              # Request / response schemas
│   └── routers/
│       ├── ingestion.py        # POST /ingest — load & index documents
│       └── search.py           # POST /search — query the RAG pipeline
│
├── app/
│   ├── config/
│   │   ├── config.yaml         # ⚙️  Main configuration file
│   │   ├── settings.py         # Pydantic settings loader
│   │   └── models/             # Config model definitions per component
│   │
│   └── src/
│       ├── backends/           # Vector store implementations
│       │   ├── chroma_backend.py
│       │   ├── elk_backend.py
│       │   └── hybrid_backend.py
│       ├── chunkers/           # Text splitting strategies
│       │   └── recursive_chunker.py
│       ├── embedders/          # Embedding providers
│       │   ├── openai_embedder.py
│       │   └── infinity_embedder.py
│       ├── llms/               # LLM providers
│       │   ├── openai_llm.py
│       │   └── ollama_llm.py
│       ├── loaders/            # Document loaders
│       │   ├── loader.py
│       │   └── pdf_loader.py
│       ├── query_transformers/ # Query pre-processing
│       │   ├── passthrough_transformer.py
│       │   └── multi_query_transformer.py
│       ├── rerankers/          # Result reranking
│       │   └── infinity_reranker.py
│       ├── generators/         # Answer generation (RAG)
│       │   └── rag_generator.py
│       ├── pipelines/          # Full pipeline orchestration
│       │   ├── ingestion_pipeline.py
│       │   └── rag_pipeline.py
│       ├── factories/          # Component instantiation from config
│       ├── core/               # Domain models & interfaces
│       │   ├── domain/         # Chunk, Document
│       │   ├── interfaces/     # Abstract base classes for all components
│       │   ├── embeddings/
│       │   ├── generation/
│       │   ├── ingestion/
│       │   ├── search/
│       │   └── prompts/        # Jinja2 prompt templates
│       ├── prompts/
│       │   ├── rag.j2          # Main RAG prompt
│       │   └── multi_query.j2  # Multi-query expansion prompt
│       └── resolvers/          # File path resolution
│
├── main.py                     # CLI entrypoint
├── Dockerfile
├── docker-compose.yaml
└── pyproject.toml
```

---

## Pipelines

### Ingestion Pipeline

Transforms raw documents into indexed, searchable chunks:

1. **Load** - reads source files via a `LoaderManager` (PDF, plain text, …)
2. **Chunk** - splits documents into overlapping text chunks
3. **Embed** — encodes chunks into dense vectors
4. **Store** - upserts chunks + vectors into the configured backend

### RAG Pipeline

Answers a user query using retrieved context:

1. **Transform** - optionally rewrites or expands the query (multi-query)
2. **Retrieve** - fetches top-k relevant chunks from the backend
3. **Rerank** - optionally re-scores retrieved chunks with a cross-encoder
4. **Generate** - calls the LLM with a context-augmented prompt

---

## Configuration

All components are configured in `app/config/config.yaml`. Switch backends, models, and strategies by editing this single file.

```yaml
# Example structure (adapt to your config.yaml)

backend: chroma          # chroma | elk | hybrid

embedder:
  provider: openai       # openai | infinity
  model: text-embedding-3-small

llm:
  provider: openai       # openai | ollama
  model: gpt-4o-mini

chunker:
  strategy: recursive
  chunk_size: 512
  chunk_overlap: 64

query_transformer:
  strategy: passthrough  # passthrough | multi_query

reranker:
  enabled: false
  provider: infinity
```

> Refer to `app/config/models/` for the full set of options per component.

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (for the containerized setup)
- An OpenAI API key and/or a running Ollama instance (depending on your config)

### Running with Docker

The recommended way to run the full stack (API + vector stores):

```bash
# Clone the repository
git clone https://github.com/LilianAndres/rag-from-scratch.git
cd rag-from-scratch

# Configure your environment
cp .env.example .env          # then fill in your API keys
nano app/config/config.yaml   # choose your backend, LLM, embedder…

# Start everything
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Running Locally

```bash
# Install dependencies
pip install -e .

# Start the API
python main.py
```

> Make sure any external services (Chroma, Elasticsearch, Ollama) are reachable at the URLs defined in your config.

---

## API Reference

### Ingest documents

```http
POST /ingest
Content-Type: application/json

{
  "source": "path/to/your/documents"
}
```

Loads, chunks, embeds, and stores the documents into the configured backend.

### Search

```http
POST /search
Content-Type: application/json

{
  "query": "What is the refund policy?"
}
```

Runs the full RAG pipeline and returns a generated answer with source chunks.

Interactive API docs are available at `http://localhost:8000/docs` once the server is running.

---

## Component Matrix

| Stage             | Options                              |
|-------------------|--------------------------------------|
| Document Loader   | PDF, plain text                      |
| Chunker           | Recursive character splitter         |
| Embedder          | OpenAI, Infinity (self-hosted)       |
| Vector Backend    | Chroma, Elasticsearch, Hybrid        |
| Query Transformer | Passthrough, Multi-Query             |
| Reranker          | Infinity (optional)                  |
| LLM               | OpenAI, Ollama                       |

---

## Extending the System

Every component follows the same pattern — implement the interface, register in the factory, add config:

1. **Create** your class in the appropriate `src/` subdirectory, implementing the interface from `core/interfaces/`
2. **Register** it in the corresponding factory under `src/factories/`
3. **Add** its config model under `app/config/models/`
4. **Select** it in `config.yaml`

No other files need to change.

---

## License

This project is open-source. See [`LICENSE`](./LICENSE) for details.