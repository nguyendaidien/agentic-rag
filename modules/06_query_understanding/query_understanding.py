from dataclasses import dataclass, field


@dataclass
class QueryIntent:
    type: str          # "factual" | "navigational" | "exploratory"
    filters: dict = field(default_factory=dict)
    rewritten_query: str = ""


FACTUAL_KEYWORDS = {"what", "who", "when", "where", "how many", "which year"}
NAVIGATIONAL_KEYWORDS = {"find", "show me", "list", "navigate", "open"}


def parse_intent(query: str, use_llm: bool = True) -> QueryIntent:
    if use_llm:
        return _llm_parse(query)
    return _rule_based_parse(query)


def _rule_based_parse(query: str) -> QueryIntent:
    lower = query.lower()
    if any(kw in lower for kw in FACTUAL_KEYWORDS):
        return QueryIntent(type="factual", rewritten_query=query)
    if any(kw in lower for kw in NAVIGATIONAL_KEYWORDS):
        return QueryIntent(type="navigational", rewritten_query=query)
    return QueryIntent(type="exploratory", rewritten_query=query)


def _llm_parse(query: str) -> QueryIntent:
    from core.config import OPENAI_API_KEY, ANTHROPIC_API_KEY
    import json

    prompt = f"""Classify this search query into one of: factual, navigational, exploratory.
Also extract any metadata filters (date_after, category, source).

Query: "{query}"

Return JSON only:
{{"type": "factual|navigational|exploratory", "filters": {{}}, "rewritten_query": "..."}}"""

    try:
        if OPENAI_API_KEY:
            from openai import OpenAI
            resp = OpenAI(api_key=OPENAI_API_KEY).chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            data = json.loads(resp.choices[0].message.content)
        else:
            import anthropic
            resp = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY).messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=128,
                messages=[{"role": "user", "content": prompt}],
            )
            data = json.loads(resp.content[0].text)
        return QueryIntent(**data)
    except Exception:
        return _rule_based_parse(query)
