import spacy

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def extract_triples(doc_id: str, text: str) -> list[dict]:
    nlp = _get_nlp()
    doc = nlp(text[:1000])
    triples = []

    for sent in doc.sents:
        entities = [ent for ent in sent.ents if ent.label_ in {"PERSON", "ORG", "GPE", "LOC"}]
        for i, subj in enumerate(entities):
            for obj in entities[i + 1:]:
                triples.append({
                    "subject": subj.text,
                    "relation": "co-occurs-with",
                    "object": obj.text,
                    "doc_id": doc_id,
                })

    return triples
