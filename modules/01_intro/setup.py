"""
Module 01: Environment setup.
Run this once to verify infrastructure and download corpus.
Usage: uv run python -m modules.01_intro.setup
"""
import sys
from core.corpus import CorpusLoader
from core.qdrant_client import get_client, ensure_collection
from core.config import QDRANT_URL, NEO4J_URI


def check_qdrant() -> bool:
    try:
        client = get_client()
        client.get_collections()
        print(f"✓ Qdrant reachable at {QDRANT_URL}")
        return True
    except Exception as e:
        print(f"✗ Qdrant not reachable: {e}")
        print("  Run: docker compose up -d")
        return False


def check_neo4j() -> bool:
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(NEO4J_URI, auth=("neo4j", "password"))
        driver.verify_connectivity()
        driver.close()
        print(f"✓ Neo4j reachable at {NEO4J_URI}")
        return True
    except Exception as e:
        print(f"✗ Neo4j not reachable: {e}")
        print("  Run: docker compose up -d")
        return False


def setup_corpus() -> None:
    loader = CorpusLoader()
    try:
        docs = list(loader.stream(limit=1))
        print(f"✓ Corpus found, first doc: '{docs[0]['title']}'")
    except FileNotFoundError:
        print("Corpus not found. Downloading (this takes ~2 min)...")
        loader.download()


def setup_qdrant_collection() -> None:
    client = get_client()
    ensure_collection(client)
    print("✓ Qdrant collection 'wiki10k' ready")


if __name__ == "__main__":
    ok = True
    ok &= check_qdrant()
    ok &= check_neo4j()
    if ok:
        setup_corpus()
        setup_qdrant_collection()
        print("\nSetup complete. Ready to start Module 02.")
    else:
        sys.exit(1)
