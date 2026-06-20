# Module 03 — Lexical Search: From TF-IDF to BM25

## What This Module Covers

Understanding inverted index mechanics through TF-IDF from scratch, then switching to BM25 for production use.

## Why This Matters

Before embeddings existed, information retrieval was solved with inverted indexes. BM25 (Best Match 25) is still competitive — it's fast, interpretable, and the best choice for keyword-heavy queries.

Understanding BM25 forces you to think about relevance at a token level: frequency, document length normalization, and diminishing returns on repeated terms.

## The Problem with TF-IDF

Raw TF has a saturation problem: a document mentioning "Paris" 50 times scores higher than one mentioning it 10 times, even if the latter is more relevant.

BM25 fixes this: `k1` controls saturation (default 1.5), `b` controls length normalization (default 0.75).

## Key Tradeoffs

| | BM25 | Semantic |
|--|------|----------|
| Latency | < 50ms | 20–100ms |
| RAM | ~200MB | ~500MB+ |
| GPU | Not needed | Helpful |
| Handles synonyms | ✗ | ✓ |
| Handles typos | ✗ | Partial |
| Best for | Exact terms, code, IDs | Natural language |

## Running

```bash
# Build index (needs corpus)
uv run python -m modules.03_lexical.indexer

# Run tests
uv run pytest modules/03_lexical/tests/ -v

# Benchmark
uv run python -c "
import sys; sys.path.insert(0, 'modules/03_lexical')
from indexer import load
from evals.benchmark import run_benchmark, save_report
from evals.synthetic_data import load_golden_set
r = load()
report = run_benchmark(lambda q, k: r.retrieve(q, k), load_golden_set(), k=10)
save_report(report, '03_bm25')
print(report)
"
```

## What to Look For

- `recall@10` → 0.40–0.60 on the golden set
- `latency_p95_ms` → under 50ms at 10k docs
- BM25 wins on exact-match queries ("API error 404"), loses on paraphrase queries
