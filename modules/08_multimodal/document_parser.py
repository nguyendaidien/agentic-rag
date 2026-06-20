from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Chunk:
    doc_id: str
    chunk_index: int
    text: str
    metadata: dict = field(default_factory=dict)


class DocumentParser:
    def chunk_text(
        self,
        text: str,
        doc_id: str,
        chunk_size: int = 512,
        overlap: int = 64,
        metadata: dict | None = None,
    ) -> list[Chunk]:
        chunks = []
        start = 0
        idx = 0
        # Ensure overlap is smaller than chunk_size to guarantee forward progress
        effective_overlap = min(overlap, chunk_size - 1) if chunk_size > 1 else 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(Chunk(
                    doc_id=doc_id,
                    chunk_index=idx,
                    text=chunk_text,
                    metadata=metadata or {},
                ))
                idx += 1
            start = end - effective_overlap
        return chunks

    def parse_pdf(self, path: str | Path) -> list[Chunk]:
        import pdfplumber
        doc_id = Path(path).stem
        chunks = []
        with pdfplumber.open(path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                tables = page.extract_tables()
                for table in tables:
                    table_text = "\n".join(
                        " | ".join(str(cell or "") for cell in row)
                        for row in table
                    )
                    text += "\n" + table_text

                page_chunks = self.chunk_text(
                    text, doc_id=doc_id,
                    metadata={"source": str(path), "page": page_num + 1},
                )
                chunks.extend(page_chunks)
        return chunks

    def parse_scan(self, path: str | Path) -> list[Chunk]:
        import pytesseract
        from PIL import Image
        doc_id = Path(path).stem
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        return self.chunk_text(
            text, doc_id=doc_id,
            metadata={"source": str(path), "type": "ocr"},
        )
