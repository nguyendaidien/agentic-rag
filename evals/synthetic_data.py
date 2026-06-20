"""Generate Q&A pairs from corpus using LLM for evaluation golden set."""
import json
import os
from pathlib import Path
from tqdm import tqdm
from core.config import OPENAI_API_KEY, ANTHROPIC_API_KEY


PROMPT_TEMPLATE = """Given this document, generate ONE question that can be answered from the text and the relevant doc IDs.

Title: {title}
Text: {text}

Return JSON only:
{{"question": "...", "answer": "...", "relevant_doc_ids": ["{doc_id}"]}}"""


def generate_pair(doc: dict, client) -> dict | None:
    prompt = PROMPT_TEMPLATE.format(
        title=doc["title"],
        text=doc["text"][:800],
        doc_id=str(doc["id"]),
    )
    try:
        if hasattr(client, "chat"):  # OpenAI
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            raw = resp.choices[0].message.content
        else:  # Anthropic
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text

        return json.loads(raw)
    except Exception:
        return None


def build_golden_set(
    corpus_loader,
    n: int = 500,
    output_path: str = "data/golden_set.jsonl",
) -> None:
    if OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
    elif ANTHROPIC_API_KEY:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    else:
        raise ValueError("Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(output_path, "w") as f:
        for doc in tqdm(corpus_loader.stream(limit=n * 2), total=n, desc="Generating Q&A"):
            if count >= n:
                break
            pair = generate_pair(doc, client)
            if pair:
                f.write(json.dumps(pair) + "\n")
                count += 1

    print(f"Saved {count} Q&A pairs to {output_path}")


def load_golden_set(path: str = "data/golden_set.jsonl") -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]
