"""Ingest the local corpus into overlapping text chunks.

Reads PDFs (via pypdf) and .txt/.md files from corpus/, splits them into
~CHUNK_TOKENS whitespace-token chunks with overlap, and writes one JSON
object per chunk to data/chunks.jsonl with source metadata.

The corpus itself is gitignored: published papers cannot be redistributed.
corpus/SOURCES.md documents what belongs in the folder.

Usage:
    python -m src.ingest
"""

import json
import re

from pypdf import PdfReader

from src import config


def read_pdf(path) -> str:
    reader = PdfReader(str(path))
    pages = [(page.extract_text() or "") for page in reader.pages]
    return "\n".join(pages)


def read_text(path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def clean(text: str) -> str:
    text = re.sub(r"-\n(?=[a-z])", "", text)   # de-hyphenate line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk(text: str, size: int, overlap: int):
    """Split on whitespace tokens with overlap. Simple and inspectable;
    swap for section-aware splitting on the thesis if chunks look bad."""
    tokens = text.split()
    step = max(size - overlap, 1)
    for start in range(0, len(tokens), step):
        piece = tokens[start : start + size]
        if len(piece) < 50:  # drop trailing fragments
            continue
        yield " ".join(piece)


def main() -> None:
    config.CHUNK_STORE.parent.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in config.CORPUS_DIR.rglob("*")
        if p.suffix.lower() in {".pdf", ".txt", ".md"}
        and p.name != "SOURCES.md"
    )
    if not files:
        raise SystemExit(
            f"No documents found in {config.CORPUS_DIR}. "
            "See corpus/SOURCES.md for what to place there."
        )

    n_chunks = 0
    with config.CHUNK_STORE.open("w", encoding="utf-8") as out:
        for path in files:
            raw = read_pdf(path) if path.suffix.lower() == ".pdf" else read_text(path)
            text = clean(raw)
            for i, piece in enumerate(chunk(text, config.CHUNK_TOKENS, config.CHUNK_OVERLAP)):
                record = {
                    "id": f"{path.stem}::{i:04d}",
                    "source": path.name,
                    "chunk_index": i,
                    "text": piece,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                n_chunks += 1
            print(f"  {path.name}: ingested")

    print(f"Wrote {n_chunks} chunks from {len(files)} documents -> {config.CHUNK_STORE}")


if __name__ == "__main__":
    main()
