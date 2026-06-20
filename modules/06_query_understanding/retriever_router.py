from typing import Callable
from query_understanding import QueryIntent


class RetrieverRouter:
    def __init__(
        self,
        bm25_fn: Callable,
        semantic_fn: Callable,
        hybrid_fn: Callable,
        graph_fn: Callable | None = None,
    ):
        self._routes = {
            "factual": bm25_fn,
            "navigational": semantic_fn,
            "exploratory": hybrid_fn,
        }
        if graph_fn:
            self._routes["graph"] = graph_fn

    def route(self, query: str, intent: QueryIntent, k: int = 10) -> list[str]:
        fn = self._routes.get(intent.type, self._routes["exploratory"])
        return fn(query, k)
