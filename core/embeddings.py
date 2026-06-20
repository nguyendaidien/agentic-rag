import numpy as np
from sentence_transformers import SentenceTransformer
from core.config import EMBEDDING_MODEL, BATCH_SIZE


class Embedder:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str], batch_size: int = BATCH_SIZE) -> np.ndarray:
        return self._model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=len(texts) > 100,
            normalize_embeddings=True,
        )

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]
