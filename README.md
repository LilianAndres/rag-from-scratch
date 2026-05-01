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

- **Interfaces** for behavior definition
- **Factories** for instantiating components and injecting dependencies
- **Config-driven system** to control everything in one place

---

## 🔥 Features

- 🔌 **Pluggable vector backends**
- 🤖 **Multiple LLM providers**
- 🧠 **Embeddings**
- 🔍 **Query transformation**
- 📊 **Reranking**
- 🔍 **Source resolution**
- 📄 **Document (streamable) parsing**
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
│   ├── schemas/                # API schemas
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
│       ├── backends/           # Vector stores
│       ├── chunkers/           # Text splitting
│       ├── embedders/          # Embedding providers
│       ├── llms/               # LLM providers
│       ├── parsers/            # Document parsers
│       ├── query_transformers/ # Query rewriting
│       ├── rerankers/          # Reranking logic
│       ├── generators/         # Answer generation
│       ├── pipelines/          # Ingestion & RAG pipelines
│       ├── factories/          # Component factories
│       ├── registries/         # Component registries
│       ├── core/               # Domain + interfaces
│       │   ├── domain/
│       │   ├── interfaces/
│       │   ├── embeddings/
│       │   ├── generation/
│       │   └── search/
│       ├── prompts/            # Jinja2 templates
│       │   ├── rag.j2
│       │   └── multi_query.j2
│       └── resolvers/          # Source resolution
│
├── eval/                       # 🧪 Offline evaluation module
│   ├── config/
│   │   ├── config.yaml         # ⚙️ Eval configuration
│   │   └── settings.py         # Eval settings loader
│   ├── domain/                 # Eval domain models
│   ├── interfaces/             # Evaluation interfaces
│   ├── factories/              # RAGAS component factories
│   ├── evaluators/             # Generic evaluator
│   ├── metrics/                # Latency, token coverage
│   ├── reporters/              # Console, JSON, CSV reporters
│   ├── runner.py               # Pipeline batch runner
│   └── main.py                 # Eval entry point
│
├── .env.example                # 👉 Copy to .env.secrets and fill in credentials
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
cp .env.example .env
```

Then fill the `.env` file with your own credentials.

### 3. Start infrastructure

```bash
docker compose -f docker-compose.dev.yaml up
```

This starts the services listed in `docker-compose.dev.yaml`. The API runs on your machine, not in Docker.

> On first run, you might need to pull the Ollama image using `docker exec -it <project>-ollama-1 ollama pull llama3:8b`. This may take a few minutes.

### 4. Start the API

```bash
uv run serve
```

The API is available at `http://localhost:8001`. Documentation at `http://localhost:8001/docs`.

---

## 🧪 Evaluation

The evaluation module runs **offline** — it instantiates the RAG pipeline directly without going through the HTTP API. It requires documents to already be ingested into the configured data stores.

The evaluation module is currently built on top of RAGAS for metric computation. However, the architecture is designed to be provider-agnostic: the underlying interfaces allow easy replacement of RAGAS or integration of alternative evaluation backends in the future without major refactoring.
In addition, the system supports extensibility through custom metrics (e.g. LatencyMetric) alongside built-in RAGAS metrics, enabling the evaluation pipeline to be tailored to specific use cases or production requirements.

1. Configure the evaluation in `eval/config/config.yaml` (judge model, dataset path, reporters, etc.).
2. Prepare carefully your own custom question set.
3. Run `uv run eval` in a terminal.

Note that the question set is expected to have the following format.

```yaml
questions:
  - id: q001
    question: "What is the Transformer model?"
    ground_truth: "The Transformer is a model architecture that relies entirely on attention mechanisms, dispensing with recurrence and convolutions."

  - id: q002
    question: "What attention mechanism does the Transformer use?"
    ground_truth: "The Transformer uses scaled dot-product attention and multi-head attention mechanisms."
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest` | Ingest documents into the vector store |
| `POST` | `/search` | Query the RAG pipeline |

Full interactive documentation: `http://localhost:8001/docs`

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