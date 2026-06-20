# Module 07 — Knowledge Graph + Filesystem Search

## What This Module Covers

Extracting entity relationships from corpus into Neo4j, then using graph traversal to find related documents. Also: corpus navigation as a filesystem.

## Why This Matters

Some questions require following chains of relationships that keyword/semantic search can't answer:
- "What documents relate to organizations that Paris is associated with?"
- Multi-hop: Entity A → related to B → related to C → find docs about C

## Graph Structure

```
(Paris: GPE) --[co-occurs-with]--> (France: GPE) [doc_id: "42"]
(Paris: GPE) --[co-occurs-with]--> (Eiffel Tower: ORG) [doc_id: "7"]
```

## Filesystem Skill

Treats the corpus like a filesystem:
- `list_docs(limit=20)` → like `ls`, shows titles + IDs
- `open_doc(doc_id)` → like `cat`, returns full text

This is the primitive an agent uses to navigate and drill into the corpus.

## Running

```bash
# Install spaCy model (one-time)
uv run python -m spacy download en_core_web_sm

# Build graph index (requires Neo4j running)
uv run python -c "
import sys; sys.path.insert(0, 'modules/07_graph_filesystem')
from graph_indexer import build_graph
build_graph(limit=1000)
"

uv run pytest modules/07_graph_filesystem/tests/ -v
```

## What to Look For

- spaCy extracts GPE/ORG/PERSON/LOC entities
- Each document produces 0–N triples depending on entity density
- Graph retrieval finds documents connected through entity relationships
- Filesystem skill enables agent to browse corpus without knowing doc IDs
