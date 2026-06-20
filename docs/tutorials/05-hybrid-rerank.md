# Module 05 — Hybrid Retrieval + Reranking

## What This Module Covers

Combining BM25 and semantic retrieval with RRF fusion, then applying a cross-encoder reranker to improve final ranking.

## Why This Matters

BM25 and semantic search have complementary failure modes. Hybrid search gets the best of both. Reranking then re-scores the top candidates with a more expensive but more accurate model.

## Reciprocal Rank Fusion (RRF)

RRF merges ranked lists without needing calibrated scores:
```
score(doc) = Σ 1 / (k + rank_in_list_i)
```
where k=60 is a smoothing constant. A document ranked #1 in both lists gets score ≈ 2/61 ≈ 0.033.

## Cross-Encoder Reranking

The retriever gets top-40 candidates (20 from BM25 + 20 from semantic via RRF). The cross-encoder scores each `(query, doc)` pair jointly — much more accurate but O(n) expensive. We rerank to top-10.

## Key Tradeoffs

| Stage | Candidates | Latency | Model |
|-------|-----------|---------|-------|
| BM25 retrieval | Top 40 | ~10ms | Inverted index |
| Semantic retrieval | Top 40 | ~30ms | all-MiniLM |
| RRF fusion | Top 40 | ~1ms | Math |
| Cross-encoder rerank | Top 10 | ~70ms | ms-marco cross-encoder |
| **Total** | **10** | **~110ms** | |

## Running

```bash
uv run pytest modules/05_hybrid_rerank/tests/ -v

# Compare BM25 vs hybrid in benchmark:
# Run both and compare data/benchmarks/03_bm25.json vs 05_hybrid.json
```

## What to Look For

- Hybrid `recall@10` → 0.65–0.85 (5–15% above best single retriever)
- Reranker improves MRR significantly (first result more likely to be relevant)
- Latency: reranker adds ~70ms — is it worth it for your use case?
