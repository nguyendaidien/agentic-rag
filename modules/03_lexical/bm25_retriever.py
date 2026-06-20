from rank_bm25 import BM25Okapi


class BM25Retriever:
    def __init__(self, docs: list[dict], k1: float = 1.5, b: float = 0.75):
        self._docs = docs
        self._ids = [str(doc["id"]) for doc in docs]
        tokenized = [doc["text"].lower().split() for doc in docs]
        self._bm25 = BM25Okapi(tokenized, k1=k1, b=b)

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        if not query.strip():
            return []
        tokens = query.lower().split()
        scores = self._bm25.get_scores(tokens)
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self._ids[i] for i in ranked[:k]]
