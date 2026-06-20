# Module 01 — Environment Setup & Project Overview

## What This Module Covers

Setting up the full infrastructure stack and understanding the project layout before writing any retrieval code.

## Why This Matters

Production retrieval systems depend on multiple services. Understanding what each service does and how to verify it's running is the first step before any code.

## Services

| Service | Port | Purpose |
|---------|------|---------|
| Qdrant | 6333 | Vector database for dense + sparse embeddings |
| Neo4j | 7474/7687 | Knowledge graph for entity relationships |
| FastAPI | 8000 | Retrieval API backend |
| Vite dev | 5173 | React search UI |

## Running

```bash
docker compose up -d
uv run python -m modules.01_intro.setup
```

Expected output:
```
✓ Qdrant reachable at http://localhost:6333
✓ Neo4j reachable at bolt://localhost:7687
✓ Corpus found, first doc: '...'
✓ Qdrant collection 'wiki10k' ready
Setup complete. Ready to start Module 02.
```

## What to Look For

- Both services reachable → infrastructure working
- Corpus download completes → `data/wiki10k/corpus.jsonl` exists with 10k lines
- Qdrant collection created → visible in dashboard at http://localhost:6333/dashboard
