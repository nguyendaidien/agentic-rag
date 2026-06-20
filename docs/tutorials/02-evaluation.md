# Module 02 — Evaluation Harness

## What This Module Covers

Building an evaluation harness before optimizing anything. This is intentional — you can't improve what you can't measure.

## Why This Matters

Most RAG systems fail because teams optimize based on vibes, not metrics. This module establishes a reproducible benchmark so every subsequent module can be objectively compared.

## Key Metrics

| Metric | Measures | Typical range |
|--------|----------|--------------|
| Recall@10 | % of relevant docs in top 10 | 0.4–0.9 |
| MRR | Where does the first relevant doc appear? | 0.3–0.8 |
| NDCG@10 | Ranking quality with graded relevance | 0.4–0.9 |
| Latency p95 | Worst-case query time (95th pct) | 10ms–500ms |
| LLM-as-judge | Qualitative relevance scoring | 0–1 rubric |

## Running

```bash
# Requires OPENAI_API_KEY or ANTHROPIC_API_KEY in .env
uv run python -m modules.02_evaluation.generate_golden_set
# Output: data/golden_set.jsonl (500 Q&A pairs)
```

## What to Look For

- 500 lines in `data/golden_set.jsonl`
- Each line: `{"question": "...", "answer": "...", "relevant_doc_ids": ["N"]}`
- Cost: ~500 API calls × ~300 tokens = ~150k tokens (~$0.02 with gpt-4o-mini)
- This golden set is reused in all subsequent modules for apples-to-apples comparison
