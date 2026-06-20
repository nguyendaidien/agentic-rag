from core.corpus import CorpusLoader


class FilesystemSkill:
    def __init__(self, loader: CorpusLoader | None = None):
        self._loader = loader or CorpusLoader()
        self._cache: dict[str, dict] = {}

    def list_docs(self, limit: int = 20) -> list[dict]:
        return [
            {"id": str(doc["id"]), "title": doc["title"]}
            for doc in self._loader.stream(limit=limit)
        ]

    def open_doc(self, doc_id: str) -> dict:
        if doc_id in self._cache:
            return self._cache[doc_id]
        for doc in self._loader.stream():
            if str(doc["id"]) == doc_id:
                self._cache[doc_id] = doc
                return doc
        raise KeyError(f"Document {doc_id} not found")
