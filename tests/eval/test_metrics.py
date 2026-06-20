import pytest
from evals.metrics import recall_at_k, mrr, ndcg_at_k


def test_recall_at_k_perfect():
    relevant = {"doc1", "doc2", "doc3"}
    retrieved = ["doc1", "doc2", "doc3", "doc4", "doc5"]
    assert recall_at_k(relevant, retrieved, k=5) == 1.0


def test_recall_at_k_partial():
    relevant = {"doc1", "doc2", "doc3"}
    retrieved = ["doc1", "doc4", "doc5"]
    assert recall_at_k(relevant, retrieved, k=3) == pytest.approx(1/3)


def test_recall_at_k_zero():
    relevant = {"doc1"}
    retrieved = ["doc2", "doc3"]
    assert recall_at_k(relevant, retrieved, k=2) == 0.0


def test_mrr_first_position():
    relevant = {"doc1"}
    retrieved = ["doc1", "doc2", "doc3"]
    assert mrr(relevant, retrieved) == 1.0


def test_mrr_third_position():
    relevant = {"doc3"}
    retrieved = ["doc1", "doc2", "doc3"]
    assert mrr(relevant, retrieved) == pytest.approx(1/3)


def test_mrr_not_found():
    relevant = {"doc4"}
    retrieved = ["doc1", "doc2", "doc3"]
    assert mrr(relevant, retrieved) == 0.0


def test_ndcg_perfect():
    relevant = {"doc1", "doc2"}
    retrieved = ["doc1", "doc2", "doc3"]
    score = ndcg_at_k(relevant, retrieved, k=3)
    assert score == pytest.approx(1.0)
