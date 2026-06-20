import pytest
from entity_extractor import extract_triples
from filesystem_skill import FilesystemSkill


def test_extract_triples_returns_list():
    text = "Barack Obama visited Paris, France to meet with Emmanuel Macron."
    triples = extract_triples("doc_0", text)
    assert isinstance(triples, list)
    assert len(triples) > 0


def test_triple_has_required_fields():
    text = "London is the capital of the United Kingdom."
    triples = extract_triples("doc_1", text)
    for triple in triples:
        assert "subject" in triple
        assert "relation" in triple
        assert "object" in triple
        assert "doc_id" in triple


def test_filesystem_skill_list_docs():
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.corpus import CorpusLoader
    skill = FilesystemSkill(CorpusLoader(source="mock"))
    listing = skill.list_docs(limit=10)
    assert len(listing) == 10
    assert all("id" in d and "title" in d for d in listing)


def test_filesystem_skill_open_doc():
    from core.corpus import CorpusLoader
    skill = FilesystemSkill(CorpusLoader(source="mock"))
    doc = skill.open_doc("0")
    assert "text" in doc
    assert "title" in doc
