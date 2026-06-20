import os
import importlib
import pytest


def test_config_loads_defaults(monkeypatch):
    monkeypatch.delenv("QDRANT_URL", raising=False)
    import core.config
    importlib.reload(core.config)
    assert core.config.QDRANT_URL == "http://localhost:6333"


def test_embeddings_encode_returns_correct_shape():
    from core.embeddings import Embedder
    emb = Embedder()
    vecs = emb.encode(["hello world", "foo bar"])
    assert vecs.shape[0] == 2
    assert vecs.shape[1] > 0  # 384 for MiniLM


def test_corpus_loader_streams_docs():
    from core.corpus import CorpusLoader
    loader = CorpusLoader(source="mock")
    docs = list(loader.stream(limit=5))
    assert len(docs) == 5
    assert "id" in docs[0]
    assert "text" in docs[0]
    assert "title" in docs[0]
