import pytest
from hybrid_retriever import rrf_fusion
from reranker import CrossEncoderReranker


def test_rrf_fusion_merges_lists():
    list1 = ["a", "b", "c"]
    list2 = ["b", "c", "d"]
    merged = rrf_fusion(list1, list2, k=60)
    assert "b" in merged[:2]  # b appears in both lists, should rank high
    assert len(merged) == 4   # union of both lists


def test_rrf_fusion_item_in_both_ranks_higher():
    list1 = ["shared", "unique1"]
    list2 = ["shared", "unique2"]
    merged = rrf_fusion(list1, list2, k=60)
    assert merged[0] == "shared"


def test_reranker_returns_k_docs():
    docs = [
        {"id": "0", "text": "Paris is the capital of France."},
        {"id": "1", "text": "Berlin is the capital of Germany."},
        {"id": "2", "text": "The Eiffel Tower is in Paris."},
    ]
    reranker = CrossEncoderReranker()
    result = reranker.rerank("capital of France", docs, k=2)
    assert len(result) == 2
    assert result[0]["id"] == "0"
