"""Build BM25 index from corpus and save to disk."""
import pickle
from pathlib import Path
from core.corpus import CorpusLoader
from bm25_retriever import BM25Retriever


INDEX_PATH = "data/bm25_index.pkl"


def build_and_save(limit: int | None = None) -> None:
    loader = CorpusLoader()
    docs = list(loader.stream(limit=limit))
    print(f"Building BM25 index over {len(docs)} docs...")
    retriever = BM25Retriever(docs)
    Path(INDEX_PATH).parent.mkdir(exist_ok=True)
    with open(INDEX_PATH, "wb") as f:
        pickle.dump(retriever, f)
    print(f"Saved BM25 index to {INDEX_PATH}")


def load() -> BM25Retriever:
    with open(INDEX_PATH, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    build_and_save()
