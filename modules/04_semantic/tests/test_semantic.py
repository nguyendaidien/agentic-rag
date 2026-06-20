from unittest.mock import MagicMock
import numpy as np
from semantic_retriever import SemanticRetriever


def test_retrieve_returns_k_results():
    mock_client = MagicMock()
    mock_client.search.return_value = [
        MagicMock(id=i, score=1.0 - i * 0.1, payload={"doc_id": str(i)})
        for i in range(5)
    ]
    mock_embedder = MagicMock()
    mock_embedder.encode_one.return_value = np.zeros(384)

    r = SemanticRetriever(client=mock_client, embedder=mock_embedder)
    results = r.retrieve("Paris capital", k=5)
    assert len(results) == 5


def test_retrieve_calls_qdrant_search():
    mock_client = MagicMock()
    mock_client.search.return_value = []
    mock_embedder = MagicMock()
    mock_embedder.encode_one.return_value = np.zeros(384)

    r = SemanticRetriever(client=mock_client, embedder=mock_embedder)
    r.retrieve("test query", k=3)

    mock_client.search.assert_called_once()
    call_kwargs = mock_client.search.call_args.kwargs
    assert call_kwargs["limit"] == 3
