from evals.benchmark import run_benchmark
from evals.metrics import recall_at_k


def test_run_benchmark_returns_metrics():
    golden_set = [
        {"question": "q1", "relevant_doc_ids": ["0"]},
        {"question": "q2", "relevant_doc_ids": ["1"]},
    ]

    def mock_retriever(query: str, k: int) -> list[str]:
        return ["0", "1", "2", "3", "4"][:k]

    report = run_benchmark(mock_retriever, golden_set, k=5)
    assert "recall@5" in report
    assert "mrr" in report
    assert "ndcg@5" in report
    assert report["recall@5"] == 1.0
