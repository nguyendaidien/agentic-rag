# Module 06 — Query Understanding + Retrieval Orchestration

## What This Module Covers

Parsing query intent and routing to the right retriever based on what the user is actually trying to do.

## Why This Matters

Not all queries are the same:
- "What is the capital of France?" → factual, needs exact match → BM25
- "Tell me about renewable energy trends" → exploratory, needs broad coverage → hybrid
- "Show me the document about Paris" → navigational, needs concept match → semantic

Sending every query through the same retriever wastes resources and hurts quality.

## Intent Classes

| Intent | Example | Best Retriever |
|--------|---------|----------------|
| factual | "What year was X built?" | BM25 (exact terms) |
| navigational | "Find the document about X" | Semantic (concept) |
| exploratory | "Tell me about X" | Hybrid (coverage) |

## Running

```bash
uv run pytest modules/06_query_understanding/tests/ -v

# Try the router manually:
uv run python -c "
import sys; sys.path.insert(0, 'modules/06_query_understanding')
from query_understanding import parse_intent
print(parse_intent('What is the capital of France?', use_llm=False))
print(parse_intent('Tell me about climate change', use_llm=False))
"
```

## What to Look For

- Rule-based intent classifies obvious factual/exploratory queries correctly
- LLM-based intent handles ambiguous queries better (requires API key)
- Routing reduces average latency vs always using hybrid
