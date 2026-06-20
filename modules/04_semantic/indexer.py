"""Embed corpus and upsert to Qdrant."""
from tqdm import tqdm
from core.corpus import CorpusLoader
from core.embeddings import Embedder
from core.qdrant_client import get_client, ensure_collection, upsert_batch
from core.config import QDRANT_COLLECTION, BATCH_SIZE


def build_index(limit: int | None = None) -> None:
    loader = CorpusLoader()
    embedder = Embedder()
    client = get_client()
    ensure_collection(client)

    docs = list(loader.stream(limit=limit))
    print(f"Indexing {len(docs)} docs into Qdrant...")

    for i in range(0, len(docs), BATCH_SIZE):
        batch = docs[i:i + BATCH_SIZE]
        texts = [d["text"] for d in batch]
        vectors = embedder.encode(texts).tolist()
        ids = [d["id"] for d in batch]
        payloads = [{"doc_id": str(d["id"]), "title": d["title"]} for d in batch]
        upsert_batch(client, QDRANT_COLLECTION, ids, vectors, payloads)

    print(f"Indexed {len(docs)} docs into collection '{QDRANT_COLLECTION}'")


if __name__ == "__main__":
    build_index()
