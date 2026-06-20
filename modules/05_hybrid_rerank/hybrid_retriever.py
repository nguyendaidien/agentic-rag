import sys
from pathlib import Path

# Allow importing BM25Retriever and SemanticRetriever from their sibling module dirs
sys.path.insert(0, str(Path(__file__).parent.parent / "03_lexical"))
sys.path.insert(0, str(Path(__file__).parent.parent / "04_semantic"))

from bm25_retriever import BM25Retriever
from semantic_retriever import SemanticRetriever


def rrf_fusion(
    *ranked_lists: list[str],
    k: int = 60,
) -> list[str]:
    """Reciprocal Rank Fusion across multiple ranked lists."""
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, doc_id in enumerate(ranked, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)


class HybridRetriever:
    def __init__(
        self,
        bm25: BM25Retriever,
        semantic: SemanticRetriever,
        rrf_k: int = 60,
    ):
        self._bm25 = bm25
        self._semantic = semantic
        self._rrf_k = rrf_k

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        n_candidates = k * 4
        bm25_results = self._bm25.retrieve(query, k=n_candidates)
        semantic_results = self._semantic.retrieve(query, k=n_candidates)
        fused = rrf_fusion(bm25_results, semantic_results, k=self._rrf_k)
        return fused[:k]
