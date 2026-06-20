from core.embeddings import Embedder
from core.qdrant_client import get_client, upsert_batch, ensure_collection
from core.config import ENABLE_MULTIMODAL
from document_parser import Chunk

MULTIMODAL_COLLECTION = "wiki10k_multimodal"


class MultimodalRetriever:
    def __init__(self):
        self._embedder = Embedder()
        self._client = get_client()
        self._collection = MULTIMODAL_COLLECTION

    def index_chunks(self, chunks: list[Chunk], start_id: int = 0) -> None:
        ensure_collection(self._client, self._collection)
        texts = [c.text for c in chunks]
        vectors = self._embedder.encode(texts).tolist()
        ids = list(range(start_id, start_id + len(chunks)))
        payloads = [
            {"doc_id": c.doc_id, "chunk_index": c.chunk_index, **c.metadata}
            for c in chunks
        ]
        upsert_batch(self._client, self._collection, ids, vectors, payloads)

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        vector = self._embedder.encode_one(query).tolist()
        hits = self._client.search(
            collection_name=self._collection,
            query_vector=vector,
            limit=k,
            with_payload=True,
        )
        return [str(hit.payload.get("doc_id", hit.id)) for hit in hits]
