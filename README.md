# 🚀 rag-from-scratch

A modular, production-ready **Retrieval-Augmented Generation (RAG)** system built from the ground up in Python.

Every component — from ingestion to generation — is abstracted behind clean interfaces, making it easy to swap models, backends, and strategies **without touching core logic**.

---

## ✨ Overview

RAG enhances LLM responses by grounding them in your own data.

This project implements the full pipeline:

```
Documents → Load → Chunk → Embed → Store
                                      ↓
              Query → Transform → Retrieve → Rerank → Generate → Answer
```

The architecture is built around:

- **Interfaces** → define behavior  
- **Factories** → instantiate components  
- **Config-driven system** → everything controlled in one place

---

## 🔥 Features

- 🔌 **Pluggable vector backends** 
- 🤖 **Multiple LLM providers**
- 🧠 **Embeddings**
- 🔍 **Query transformation**
- 📊 **Reranking**
- 📄 **Document loaders**
- 🌐 **FastAPI REST API**  
- ⚙️ **Fully configurable**
- 🐳 **Production-ready**  
- 🧪 **Offline evaluation module**  

---

## 📁 Project Structure

```
.
├── api/                        # FastAPI layer (HTTP interface)
│   ├── app.py                  # FastAPI app creation
│   ├── dependencies.py         # Dependency injection
│   ├── schemas.py              # API schemas
│   └── routers/
│       ├── ingestion.py        # POST /ingest
│       └── search.py           # POST /search
│
├── app/
│   ├── config/
│   │   ├── config.yaml         # ⚙️ Main configuration
│   │   ├── settings.py         # Env + settings loader
│   │   └── models/             # Typed config models
│   │
│   └── src/
│       ├── backends/           # Vector stores (Chroma, ELK, Hybrid)
│       ├── chunkers/           # Text splitting
│       ├── embedders/          # Embedding providers
│       ├── llms/               # LLM providers
│       ├── loaders/            # Document loaders (PDF, etc.)
│       ├── query_transformers/ # Query rewriting
│       ├── rerankers/          # Reranking logic
│       ├── generators/         # Answer generation
│       ├── pipelines/          # Ingestion & RAG pipelines
│       ├── factories/          # Component factories
│       ├── core/               # Domain + interfaces
│       │   ├── domain/
│       │   ├── interfaces/
│       │   ├── embeddings/
│       │   ├── generation/
│       │   └── search/
│       ├── prompts/            # Jinja2 templates
│       │   ├── rag.j2
│       │   └── multi_query.j2
│       └── resolvers/          # File resolution
│
├── eval/                       # 🧪 Offline evaluation module
│   ├── dataset/                # Test questions
│   ├── eval_runner.py
│   ├── ragas_evaluator.py
│   ├── eval_reporter.py
│   └── main.py                 # Entry point
│
├── main.py                     # App entrypoint (runs API)
├── Dockerfile
├── docker-compose.dev.yml      # Local dev infrastructure (optional)
└── pyproject.toml
```

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

### ⚙️ Configuration

All components are configured in:

```
app/config/config.yaml
```

Example:

```yaml
providers:
  ollama:
    base_url: "http://localhost:11434"
  infinity:
    base_url: "http://localhost:7997"

llms:
  profiles:
    fast:
      provider: ollama
      ollama:
        model: llama3:8b
        temperature: 0.0
        max_tokens: 512
        timeout: 360.0

resolvers:
  local:
    base_path: /tmp

loaders:
  pdf:
    page_separator: "\n"

chunker:
  provider: recursive
  recursive:
    chunk_size: 800
    chunk_overlap: 100
    separators: null

embedder:
  provider: infinity
  infinity:
    model: BAAI/bge-small-en-v1.5
    timeout: 60.0

backend:
  type: chroma
  chroma:
    host: localhost
    port: 8001
    collection_name: documents
    distance_function: cosine

reranker:
  enabled: true
  provider: infinity
  infinity:
    model: cross-encoder/ms-marco-MiniLM-L-6-v2
    top_n: 5
    timeout: 60.0

generator:
  llm_profile: fast
  prompts_dir: app/src/prompts/templates
  prompt_template: rag.j2

query_transformer:
  enabled: false
  provider: multi-query
  llm_profile: fast
  prompts_dir: app/src/prompts/templates
  multi_query:
    n_variants: 3
    prompt_template: multi_query.j2
```

> Refer to `app/config/models/` for the full set of options per component Feel free to add your own.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional but recommended)
- OpenAI API key (if using OpenAI)

---

## 🐳 Running with Docker (recommended)

```bash
git clone https://github.com/LilianAndres/rag-from-scratch.git
cd rag-from-scratch

cp .env.example .env
nano app/config/config.yaml

docker compose -f docker-compose.dev.yaml up --build
```

The API should be available at `http://localhost:8000`.

---

## 💻 Running Locally

```bash
uv sync
uv run python main.py
```

> Make sure any external services are reachable at the URLs defined in your config.

---

## 🧪 Evaluation Module (offline)

```bash
uv run python eval/main.py
```

Used for benchmarking, testing configurations, and regression checks.

---

## 🔌 API Reference

The documentation is available at `http://localhost:8000/docs`.

---

## 🧠 Architecture Principles

- Interface-driven design  
- Dependency injection  
- Factory pattern  
- Config over code  
- Modular pipelines  

---

## 🛠️ Extending the system

1. Implement interface (`core/interfaces/`)  
2. Add implementation in `src/`  
3. Register in factory  
4. Add config model  
5. Update `config.yaml`  

No core changes required.

---

## 🤝 Contributing

Contributions are welcome!

- Follow existing architecture  
- Keep components modular  
- Add config models  
- Run evaluation before submitting  

---

## 🧭 Going further

- Add more loaders (HTML, Markdown, APIs)
- Add more providers (Anthropic, Google, etc.)
- Add observability (logs, tracing)
- Add guardrails layer (input, output)
- Add CI/CD workflows (evaluation, docker image)

---

## 📄 License

This project is under MIT license. Please feel free to use it.