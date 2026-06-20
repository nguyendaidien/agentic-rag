from neo4j import GraphDatabase
from core.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from entity_extractor import _get_nlp


class GraphRetriever:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    def retrieve(self, query: str, k: int = 10) -> list[str]:
        nlp = _get_nlp()
        doc = nlp(query)
        entities = [ent.text for ent in doc.ents]

        if not entities:
            return []

        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (s:Entity)-[r:RELATED*1..2]->(o:Entity)
                WHERE s.name IN $entities OR o.name IN $entities
                RETURN DISTINCT r[0].doc_id AS doc_id
                LIMIT $limit
                """,
                entities=entities,
                limit=k,
            )
            return [record["doc_id"] for record in result if record["doc_id"]]

    def close(self):
        self._driver.close()
