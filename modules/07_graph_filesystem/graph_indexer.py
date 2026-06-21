import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from neo4j import GraphDatabase
from core.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from entity_extractor import extract_triples
from core.corpus import CorpusLoader


def get_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def ingest_triples(triples: list[dict], driver) -> None:
    with driver.session() as session:
        for triple in triples:
            session.run(
                """
                MERGE (s:Entity {name: $subject})
                MERGE (o:Entity {name: $object})
                MERGE (s)-[r:RELATED {type: $relation, doc_id: $doc_id}]->(o)
                """,
                subject=triple["subject"],
                object=triple["object"],
                relation=triple["relation"],
                doc_id=triple["doc_id"],
            )


def build_graph(limit: int = 1000) -> None:
    driver = get_driver()
    loader = CorpusLoader()
    count = 0
    for doc in loader.stream(limit=limit):
        triples = extract_triples(str(doc["id"]), doc["text"])
        ingest_triples(triples, driver)
        count += len(triples)
    driver.close()
    print(f"Ingested {count} triples into Neo4j")
