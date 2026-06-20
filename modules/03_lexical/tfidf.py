"""TF-IDF from scratch — for learning purposes. Not used in production."""
import math
from collections import Counter


def tokenize(text: str) -> list[str]:
    return text.lower().split()


def build_tfidf(docs: list[dict]) -> tuple[dict, dict]:
    N = len(docs)
    df: dict[str, int] = Counter()
    tf_matrix: dict[str, dict[str, float]] = {}

    for doc in docs:
        tokens = tokenize(doc["text"])
        tf_matrix[doc["id"]] = {}
        for term, count in Counter(tokens).items():
            tf_matrix[doc["id"]][term] = count / len(tokens)
            df[term] += 1

    idf = {term: math.log(N / (1 + freq)) for term, freq in df.items()}
    return tf_matrix, idf


def tfidf_score(query: str, doc_id: str, tf_matrix: dict, idf: dict) -> float:
    score = 0.0
    for term in tokenize(query):
        tf = tf_matrix.get(doc_id, {}).get(term, 0)
        score += tf * idf.get(term, 0)
    return score
