import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
CORPUS_DIR: str = os.getenv("CORPUS_DIR", "./data/wiki10k")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
ENABLE_MULTIMODAL: bool = os.getenv("ENABLE_MULTIMODAL", "false").lower() == "true"

EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM: int = 384
QDRANT_COLLECTION: str = "wiki10k"
BATCH_SIZE: int = 64
