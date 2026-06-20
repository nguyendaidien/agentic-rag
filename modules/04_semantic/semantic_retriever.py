import numpy as np
from qdrant_client import QdrantClient
from core.config import QDRANT_COLLECTION
from core.embeddings import Embedder
from core.qdrant_client import get_client


class SemanticRetriever:
    def __init__(
        self,
        client: QdrantClient | None = None,
        embedder: Embedder | None = None,
        collection: str = QDRANT_COLLECTION,
    ):
        self._client = client or get_client()
        self._embedder = embedder or Embedder()
        self._collection = collection

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        vector = self._embedder.encode_one(query).tolist()
        hits = self._client.search(
            collection_name=self._collection,
            query_vector=vector,
            limit=k,
            with_payload=True,
        )
        return [str(hit.payload.get("doc_id", hit.id)) for hit in hits]
