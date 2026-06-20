from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from core.config import QDRANT_URL, EMBEDDING_DIM, QDRANT_COLLECTION


def get_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def ensure_collection(client: QdrantClient, name: str = QDRANT_COLLECTION) -> None:
    existing = [c.name for c in client.get_collections().collections]
    if name not in existing:
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


def upsert_batch(
    client: QdrantClient,
    collection: str,
    ids: list[int],
    vectors: list[list[float]],
    payloads: list[dict],
) -> None:
    points = [
        PointStruct(id=i, vector=v, payload=p)
        for i, v, p in zip(ids, vectors, payloads)
    ]
    client.upsert(collection_name=collection, points=points)
