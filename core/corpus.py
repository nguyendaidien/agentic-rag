import json
import os
from pathlib import Path
from typing import Iterator
from tqdm import tqdm
from core.config import CORPUS_DIR


MOCK_DOCS = [
    {"id": i, "title": f"Doc {i}", "text": f"This is the text of document {i}. It contains information about topic {i % 10}."}
    for i in range(1000)
]


class CorpusLoader:
    def __init__(self, source: str = "disk"):
        self.source = source  # "disk" | "mock" | "hf"
        self.corpus_dir = Path(CORPUS_DIR)

    def stream(self, limit: int | None = None) -> Iterator[dict]:
        if self.source == "mock":
            docs = MOCK_DOCS[:limit] if limit else MOCK_DOCS
            yield from docs
            return

        jsonl_path = self.corpus_dir / "corpus.jsonl"
        if not jsonl_path.exists():
            raise FileNotFoundError(
                f"Corpus not found at {jsonl_path}. Run: uv run python -m core.corpus download"
            )
        count = 0
        with open(jsonl_path) as f:
            for line in f:
                if limit and count >= limit:
                    break
                try:
                    doc = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Malformed JSON at line {count} in {jsonl_path}: {e}") from e
                yield doc
                count += 1

    def download(self) -> None:
        """Download Wikipedia 10k subset from HuggingFace datasets."""
        from datasets import load_dataset

        self.corpus_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.corpus_dir / "corpus.jsonl"

        if out_path.exists():
            print(f"Corpus already exists at {out_path}")
            return

        print("Downloading Wikipedia 10k subset...")
        ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train", streaming=True)
        count = 0
        with open(out_path, "w") as f:
            for item in tqdm(ds, total=10_000):
                if count >= 10_000:
                    break
                doc = {
                    "id": count,
                    "title": item["title"],
                    "text": item["text"][:2000],  # first 2000 chars per doc
                }
                f.write(json.dumps(doc) + "\n")
                count += 1
        print(f"Saved {count} docs to {out_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "download":
        CorpusLoader().download()
