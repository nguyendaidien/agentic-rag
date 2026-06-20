from transformers import pipeline


class CrossEncoderReranker:
    def __init__(self, model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self._pipe = pipeline("text-classification", model=model, device=-1)

    def rerank(self, query: str, docs: list[dict], k: int = 10) -> list[dict]:
        pairs = [{"text": query, "text_pair": doc["text"]} for doc in docs]
        scores = self._pipe(pairs, batch_size=16)
        for doc, score in zip(docs, scores):
            doc["_rerank_score"] = score["score"]
        return sorted(docs, key=lambda d: d["_rerank_score"], reverse=True)[:k]
