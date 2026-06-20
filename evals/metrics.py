import math


def recall_at_k(relevant: set[str], retrieved: list[str], k: int) -> float:
    if not relevant:
        return 0.0
    top_k = set(retrieved[:k])
    return len(relevant & top_k) / len(relevant)


def mrr(relevant: set[str], retrieved: list[str]) -> float:
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(relevant: set[str], retrieved: list[str], k: int) -> float:
    def dcg(hits: list[int]) -> float:
        return sum(h / math.log2(i + 2) for i, h in enumerate(hits))

    hits = [1 if doc_id in relevant else 0 for doc_id in retrieved[:k]]
    ideal = sorted(hits, reverse=True)
    actual_dcg = dcg(hits)
    ideal_dcg = dcg(ideal)
    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0


def average_metrics(results: list[dict]) -> dict:
    """Average recall@k, mrr, ndcg across a list of per-query result dicts."""
    if not results:
        return {}
    keys = results[0].keys()
    return {k: sum(r[k] for r in results) / len(results) for k in keys}
