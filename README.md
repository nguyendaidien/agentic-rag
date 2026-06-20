# Production-Grade Agentic RAG

Learning project for [ContextBox AI Engineer Module 2](https://academy.contextbox.tech/courses/ai-engineer-module-2/). Covers the full retrieval stack from TF-IDF to agentic search with a live Web UI.

## Prerequisites

- Python 3.11+
- Docker Desktop
- One of: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (for eval + query understanding)
- Node.js 18+ (for Web UI)

## Install & Run

### 1. Clone and install

```bash
git clone https://github.com/you/agentic-rag
cd agentic-rag
pip install uv
uv sync
```

### 2. Start infrastructure

```bash
docker compose up -d
# Qdrant dashboard: http://localhost:6333/dashboard
# Neo4j browser:    http://localhost:7474  (user: neo4j, pass: password)
```

### 3. Configure API keys

```bash
cp .env.example .env
# Edit .env and fill in OPENAI_API_KEY or ANTHROPIC_API_KEY
```

### 4. Setup (environment check + corpus download)

```bash
uv run python -m modules.01_intro.setup
```

### 5a. Web UI

```bash
# Terminal 1: API
uv run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd app/frontend && npm install && npm run dev
# Open: http://localhost:5173
```

### 5b. Or run individual notebooks

```bash
uv run jupyter notebook modules/03_lexical/notebook.ipynb
```

## Module Index

| Module | Topic | Key Output |
|--------|-------|-----------|
| [01 — Intro](docs/tutorials/01-intro.md) | Environment Setup | Working infra, corpus ready |
| [02 — Evaluation](docs/tutorials/02-evaluation.md) | Evaluation Harness | 500-query golden set |
| [03 — Lexical](docs/tutorials/03-lexical.md) | BM25 Search | BM25Retriever, benchmark |
| [04 — Semantic](docs/tutorials/04-semantic.md) | Semantic Search | SemanticRetriever, Qdrant index |
| [05 — Hybrid](docs/tutorials/05-hybrid-rerank.md) | Hybrid + Rerank | HybridRetriever, comparative benchmark |
| [06 — Query Understanding](docs/tutorials/06-query-understanding.md) | Agentic Query Parsing | QueryIntent, RetrieverRouter |
| [07 — Graph](docs/tutorials/07-graph-filesystem.md) | Knowledge Graph | GraphRetriever (Neo4j), FilesystemSkill |
| [08 — Multimodal](docs/tutorials/08-multimodal.md) | Document Parsing | DocumentParser, MultimodalRetriever |

## Running benchmarks

```bash
# Generate golden set (requires API key)
uv run python -m modules.02_evaluation.generate_golden_set

# Build BM25 index
uv run python -m modules.03_lexical.indexer

# Build semantic index (requires Qdrant running)
uv run python -m modules.04_semantic.indexer

# Run benchmark
uv run python -c "
from modules.03_lexical.indexer import load
from evals.benchmark import run_benchmark, save_report
from evals.synthetic_data import load_golden_set
r = load()
report = run_benchmark(lambda q, k: r.retrieve(q, k), load_golden_set(), k=10)
save_report(report, '03_bm25')
print(report)
"
```

## Tech Stack

Python 3.11 · uv · Qdrant · DeepEval · Neo4j · sentence-transformers · rank-bm25 · FastAPI · React+Vite · Docker Compose · pdfplumber · pytesseract · spaCy
