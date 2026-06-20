import json
import time
from pathlib import Path
from typing import Callable
from evals.metrics import recall_at_k, mrr, ndcg_at_k, average_metrics
from evals.synthetic_data import load_golden_set


def run_benchmark(
    retriever_fn: Callable[[str, int], list[str]],
    golden_set: list[dict],
    k: int = 10,
) -> dict:
    results = []
    latencies = []

    for item in golden_set:
        query = item["question"]
        relevant = set(item["relevant_doc_ids"])

        t0 = time.perf_counter()
        retrieved = retriever_fn(query, k)
        latencies.append((time.perf_counter() - t0) * 1000)

        results.append({
            f"recall@{k}": recall_at_k(relevant, retrieved, k),
            "mrr": mrr(relevant, retrieved),
            f"ndcg@{k}": ndcg_at_k(relevant, retrieved, k),
        })

    avg = average_metrics(results)
    latencies_sorted = sorted(latencies)
    avg["latency_p50_ms"] = latencies_sorted[len(latencies_sorted) // 2]
    avg["latency_p95_ms"] = latencies_sorted[int(len(latencies_sorted) * 0.95)]
    avg["n_queries"] = len(golden_set)
    return avg


def save_report(report: dict, name: str, output_dir: str = "data/benchmarks") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = f"{output_dir}/{name}.json"
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Benchmark saved to {path}")
    return path
