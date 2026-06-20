import time
import sys
import os
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Add project root to sys.path for module imports
_project_root = str(Path(__file__).parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class SearchRequest(BaseModel):
    query: str
    method: str = "hybrid"  # "bm25" | "semantic" | "hybrid" | "graph"
    k: int = 10
    rerank: bool = True


class SearchResult(BaseModel):
    doc_id: str
    title: str
    snippet: str
    score: float
    method: str


class SearchResponse(BaseModel):
    results: list[SearchResult]
    trace: list[dict]
    total_ms: float


@router.post("", response_model=SearchResponse)
def search(req: SearchRequest):
    trace = []
    t_start = time.perf_counter()

    # Query understanding (rule-based, no LLM required)
    t0 = time.perf_counter()
    _add_module_to_path("06_query_understanding")
    from query_understanding import parse_intent
    intent = parse_intent(req.query, use_llm=False)
    trace.append({
        "step": "query_understanding",
        "ms": round((time.perf_counter() - t0) * 1000, 1),
        "intent": intent.type,
    })

    # Retrieval
    t0 = time.perf_counter()
    doc_ids = _retrieve(req.query, req.method, req.k * 4)
    trace.append({
        "step": f"{req.method}_retrieval",
        "ms": round((time.perf_counter() - t0) * 1000, 1),
        "candidates": len(doc_ids),
    })

    # Rerank
    if req.rerank and req.method != "bm25" and doc_ids:
        t0 = time.perf_counter()
        doc_ids = _rerank(req.query, doc_ids, req.k)
        trace.append({
            "step": "rerank",
            "ms": round((time.perf_counter() - t0) * 1000, 1),
        })
    else:
        doc_ids = doc_ids[:req.k]

    results = _build_results(doc_ids, req.method)
    total_ms = round((time.perf_counter() - t_start) * 1000, 1)
    trace.append({"step": "total", "ms": total_ms})

    return SearchResponse(results=results, trace=trace, total_ms=total_ms)


def _add_module_to_path(module_dir: str) -> None:
    modules_base = str(Path(__file__).parent.parent.parent / "modules")
    target = str(Path(modules_base) / module_dir)
    if target not in sys.path:
        sys.path.insert(0, target)
    if modules_base not in sys.path:
        sys.path.insert(0, modules_base)


def _retrieve(query: str, method: str, k: int) -> list[str]:
    if method == "bm25":
        _add_module_to_path("03_lexical")
        from indexer import load
        return load().retrieve(query, k=k)
    elif method == "semantic":
        _add_module_to_path("04_semantic")
        from semantic_retriever import SemanticRetriever
        return SemanticRetriever().retrieve(query, k=k)
    elif method == "graph":
        _add_module_to_path("07_graph_filesystem")
        from graph_retriever import GraphRetriever
        return GraphRetriever().retrieve(query, k=k)
    else:  # hybrid
        _add_module_to_path("03_lexical")
        _add_module_to_path("04_semantic")
        _add_module_to_path("05_hybrid_rerank")
        from indexer import load as load_bm25
        from semantic_retriever import SemanticRetriever
        from hybrid_retriever import HybridRetriever
        return HybridRetriever(load_bm25(), SemanticRetriever()).retrieve(query, k=k)


def _rerank(query: str, doc_ids: list[str], k: int) -> list[str]:
    _add_module_to_path("05_hybrid_rerank")
    from reranker import CrossEncoderReranker
    from core.corpus import CorpusLoader
    loader = CorpusLoader()
    docs_map = {str(d["id"]): d for d in loader.stream()}
    docs = [{"id": did, "text": docs_map.get(did, {}).get("text", "")} for did in doc_ids]
    reranked = CrossEncoderReranker().rerank(query, docs, k=k)
    return [d["id"] for d in reranked]


def _build_results(doc_ids: list[str], method: str) -> list[SearchResult]:
    from core.corpus import CorpusLoader
    loader = CorpusLoader()
    docs_map = {str(d["id"]): d for d in loader.stream()}
    results = []
    for i, did in enumerate(doc_ids):
        doc = docs_map.get(did, {"title": "Unknown", "text": ""})
        results.append(SearchResult(
            doc_id=did,
            title=doc.get("title", ""),
            snippet=doc.get("text", "")[:200],
            score=round(max(0.0, 1.0 - i * 0.05), 3),
            method=method,
        ))
    return results
