import pytest
from query_understanding import QueryIntent, parse_intent


def test_parse_intent_returns_intent_object():
    intent = parse_intent("What is the capital of France?", use_llm=False)
    assert isinstance(intent, QueryIntent)
    assert intent.type in ("factual", "navigational", "exploratory")


def test_factual_query_classified_correctly():
    intent = parse_intent("What year was the Eiffel Tower built?", use_llm=False)
    assert intent.type == "factual"


def test_exploratory_query_classified_correctly():
    intent = parse_intent("Tell me about renewable energy trends", use_llm=False)
    assert intent.type == "exploratory"
