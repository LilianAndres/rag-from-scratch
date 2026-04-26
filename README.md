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
- 🐳 **Docker infrastructure**
- 🧪 **Offline evaluation module**

---

## 📁 Project Structure

```
.
├── api/                        # FastAPI layer (HTTP interface)
│   ├── app.py                  # FastAPI app creation
│   ├── dependencies.py         # Dependency injection
│   ├── main.py                 # API entry point
│   ├── schemas.py              # API schemas
│   └── routers/
│       ├── ingestion.py        # POST /ingest
│       └── search.py           # POST /search
│
├── app/
│   ├── config/
│   │   ├── config.yaml         # ⚙️ Main configuration (app behaviour)
│   │   ├── settings.py         # Settings loader
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
│   ├── config/
│   │   ├── config.yaml         # ⚙️ Eval configuration
│   │   └── settings.py         # Eval settings loader
│   ├── dataset/                # Test questions (YAML)
│   ├── domain/                 # Eval domain models
│   ├── evaluators/             # RAGAS evaluator
│   ├── metrics/                # Latency, token coverage
│   ├── reporters/              # Console, JSON, CSV reporters
│   ├── runner.py               # Pipeline batch runner
│   └── main.py                 # Eval entry point
│
├── .env.example                # 👉 Copy to .env.secrets and fill in credentials
├── .env.local                  # Topology for local dev (committed, no secrets)
├── .env.providers              # Provider URLs shared by app and eval (committed)
├── docker-compose.dev.yaml     # Local dev infrastructure (Chroma, Ollama, Infinity)
├── Dockerfile                  # Production image
└── pyproject.toml
```

---

## ⚙️ Configuration

### Application settings

Controls how the RAG pipeline behaves: chunk size, models, reranking, prompt templates, etc. Environment-agnostic — no hostnames here.

```yaml
# app/config/config.yaml

chunker:
  provider: recursive
  recursive:
    chunk_size: 800
    chunk_overlap: 100

embedder:
  provider: infinity
  infinity:
    model: BAAI/bge-small-en-v1.5

reranker:
  enabled: true
  provider: infinity
  infinity:
    model: cross-encoder/ms-marco-MiniLM-L-6-v2
    top_n: 5

generator:
  llm_profile: fast
  prompt_template: rag.j2

query_transformer:
  enabled: false
```

> Refer to `app/config/models/` for the full set of options per component.

### Topology — env files

Service hostnames and ports live in env files, not in YAML, so the same config works across environments without modification.

| File | Purpose | Committed |
|---|---|---|
| `.env.secrets` | Credentials (API keys, passwords) | ❌ git-ignored |
| `.env.local` | App topology for local dev | ✅ |
| `.env.providers` | Provider URLs shared by app and eval | ✅ |
| `.env.example` | Template for `.env.secrets` | ✅ |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- Docker

### 1. Install dependencies

```bash
git clone https://github.com/LilianAndres/rag-from-scratch.git
cd rag-from-scratch
uv sync
```

### 2. Set up credentials

```bash
cp .env.example .env.secrets # fill in your API keys in .env.secrets
```

### 3. Start infrastructure

```bash
docker compose -f docker-compose.dev.yaml up
```

This starts **Chroma**, **Ollama**, and **Infinity** locally. The API runs on your machine, not in Docker.

> On first run, you might need to pull the Ollama image using `docker exec -it <project>-ollama-1 ollama pull llama3:8b`. This may take a few minutes.

### 4. Start the API

```bash
uv run serve
```

The API is available at `http://localhost:8001`. Documentation at `http://localhost:8001/docs`.

---

## 🧪 Evaluation

The evaluation module runs **offline** — it instantiates the RAG pipeline directly without going through the HTTP API. It requires documents to already be ingested into Chroma.

**Typical workflow:**

```bash
# 1. Ingest your documents (once, or when the corpus changes)
curl -X POST http://localhost:8000/ingest ...

# 2. Run evaluation (as many times as needed against the same corpus)
uv run eval
```

Chroma data is persisted in a named Docker volume, so you don't need to re-ingest between sessions or restarts.

Configure the evaluation in `eval/config/config.yaml` (judge model, dataset path, reporters, etc.).

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest` | Ingest documents into the vector store |
| `POST` | `/search` | Query the RAG pipeline |

Full interactive documentation: `http://localhost:8000/docs`

---

## 🧠 Architecture Principles

- Interface-driven design
- Dependency injection
- Factory pattern
- Config over code
- Modular pipelines

---

## 🛠️ Extending the system

1. Implement the interface (`core/interfaces/`)
2. Add the implementation in `src/`
3. Register it in the factory
4. Add a config model
5. Update `config.yaml`

No core changes required.

---

## 🧭 Going further

- Add more loaders (HTML, Markdown, APIs)
- Add more providers (Anthropic, Google, etc.)
- Add observability (logs, tracing)
- Add guardrails layer (input, output)
- Add CI/CD workflows (evaluation, Docker image)

---

## 🤝 Contributing

Contributions are welcome!

- Follow existing architecture
- Keep components modular
- Add config models
- Run evaluation before submitting

---

## 📄 License

This project is under MIT license. Please feel free to use it.