# Module 04 — Semantic Search with Vector Embeddings

## What This Module Covers

Using dense vector embeddings to find documents by meaning rather than exact keywords.

## Why This Matters

Semantic search solves the vocabulary mismatch problem. "capital city" finds documents about "metropolis" and "seat of government" that BM25 would miss entirely.

## How It Works

1. Embed each document with `all-MiniLM-L6-v2` → 384-dim vector
2. Store vectors in Qdrant with HNSW index
3. At query time: embed query → find k nearest vectors via ANN search

## Key Tradeoffs

| | ANN (HNSW) | Exact Search |
|--|------------|-------------|
| Latency | Fast (< 10ms) | Slow (O(n)) |
| Recall | ~95–99% | 100% |
| RAM | ~500MB for 10k docs | Same |
| Best for | Production | Evaluation baseline |

## Embedding Model Choice

| Model | Dim | Speed | Quality |
|-------|-----|-------|---------|
| all-MiniLM-L6-v2 | 384 | Very fast | Good |
| all-mpnet-base-v2 | 768 | Moderate | Better |
| text-embedding-3-small | 1536 | API call | Best |

## Running

```bash
# Requires Qdrant running
uv run python -m modules.04_semantic.indexer
# Takes ~5 min for 10k docs on CPU

uv run pytest modules/04_semantic/tests/ -v
```

## What to Look For

- `recall@10` → 0.55–0.75 (better than BM25 on natural language queries)
- Semantic wins on synonyms, loses on exact product codes and error messages
- Compare Qdrant HNSW vs exact search: recall gap should be < 2%
