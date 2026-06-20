import pytest
from document_parser import DocumentParser, Chunk


def test_parser_chunks_plain_text():
    parser = DocumentParser()
    text = "This is sentence one. This is sentence two. This is sentence three."
    chunks = parser.chunk_text(text, doc_id="doc_0", chunk_size=50)
    assert len(chunks) > 0
    assert all(isinstance(c, Chunk) for c in chunks)


def test_chunk_has_required_fields():
    parser = DocumentParser()
    chunks = parser.chunk_text("Hello world test text here.", doc_id="doc_1", chunk_size=20)
    for chunk in chunks:
        assert chunk.doc_id == "doc_1"
        assert chunk.text
        assert chunk.chunk_index >= 0


def test_parser_extracts_metadata():
    parser = DocumentParser()
    chunks = parser.chunk_text("Sample text.", doc_id="doc_2", chunk_size=100,
                               metadata={"source": "test.pdf", "page": 1})
    assert chunks[0].metadata["source"] == "test.pdf"
