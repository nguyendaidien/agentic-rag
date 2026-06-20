# Module 08 — Document Parsing + Multimodal Search

## What This Module Covers

Parsing real-world documents (PDFs, scanned images) into searchable chunks, and retrieving over mixed text/image content.

## Why This Matters

Most enterprise knowledge lives in PDFs, scanned forms, slide decks, and tables — not clean text. Production retrieval must handle:
- PDFs with complex layouts and tables
- Scanned documents (image → OCR → text)
- Mixed content (text + images on same page)

## Chunking Strategy

```
Full document
  → Pages (pdfplumber)
  → Chunks (512 chars, 64 overlap)
  → Metadata: {source, page, type}
```

Overlap ensures context isn't lost at chunk boundaries.

## Key Tradeoffs

| Parser | Handles | Misses |
|--------|---------|--------|
| pdfplumber | Native PDFs, tables | Scanned PDFs |
| pytesseract OCR | Scanned images | Complex layouts |
| CLIP (optional) | Images by content | Requires GPU |

## Running

```bash
# Test chunking (no external services needed)
uv run pytest modules/08_multimodal/tests/ -v

# Parse a PDF:
uv run python -c "
import sys; sys.path.insert(0, 'modules/08_multimodal')
from document_parser import DocumentParser
parser = DocumentParser()
chunks = parser.parse_pdf('your_file.pdf')
print(f'{len(chunks)} chunks from PDF')
print(chunks[0])
"

# Enable CLIP multimodal (optional, large download):
# Set ENABLE_MULTIMODAL=true in .env
```

## What to Look For

- `chunk_text` → consistent chunk sizes, no empty chunks
- PDF parsing → each page produces chunks with page metadata
- OCR accuracy depends on image quality (300 DPI recommended)
- Multimodal retrieval combines text + image embeddings
