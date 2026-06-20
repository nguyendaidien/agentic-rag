import pytest
from bm25_retriever import BM25Retriever


DOCS = [
    {"id": "0", "text": "Paris is the capital of France and a major European city."},
    {"id": "1", "text": "Berlin is the capital of Germany located in central Europe."},
    {"id": "2", "text": "The Eiffel Tower is a famous landmark in Paris, France."},
]


def test_retrieve_returns_k_results():
    r = BM25Retriever(DOCS)
    results = r.retrieve("Paris France", k=2)
    assert len(results) == 2


def test_retrieve_returns_doc_ids():
    r = BM25Retriever(DOCS)
    results = r.retrieve("Paris France", k=3)
    assert all(isinstance(doc_id, str) for doc_id in results)


def test_relevant_doc_ranks_first():
    r = BM25Retriever(DOCS)
    results = r.retrieve("Eiffel Tower landmark", k=3)
    assert results[0] == "2"


def test_empty_query_returns_empty():
    r = BM25Retriever(DOCS)
    results = r.retrieve("", k=3)
    assert results == []
