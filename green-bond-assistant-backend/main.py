"""Green Bond Credibility Assistant — FastAPI backend.

Endpoints:
  POST /chat          { "question": "..." } → streaming text response
  POST /upload        multipart PDF upload → ingests into ChromaDB
  GET  /status        corpus status (chunk count, sources)
  GET  /health        liveness check
"""

import os
import json
import re
from pathlib import Path

import anthropic
import chromadb
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

# ── config ────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
DATA_DIR          = Path(os.environ.get("DATA_DIR", "/data"))
VECTOR_DIR        = DATA_DIR / "chroma"
CHUNK_STORE       = DATA_DIR / "chunks.jsonl"
EMBED_MODEL       = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME   = "green_bond_corpus"
CHUNK_TOKENS      = 500
CHUNK_OVERLAP     = 80
TOP_K             = 5
MIN_SIMILARITY    = 0.35
LLM_MODEL         = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are a research assistant specialised in sovereign green bond
credibility and the greenium literature. You answer questions strictly from the
context passages provided, with inline citations [1], [2], etc.

You are a KNOWLEDGE TOOL, not an advisory tool. You summarise what the evidence
says — including null, mixed, and contested findings — with uncertainty attached.

The corpus includes a master's thesis (Ibnat, 2026) whose central empirical
results are NULL EFFECTS of climate-news tone and signalling noise on the greenium
in India and Indonesia, with VIX as the dominant daily pricing driver (0.35–0.48 bp
per SD of log VIX). Report such results faithfully; never reframe a null as positive.

HARD RULES:
1. No policy advice. Never tell governments or issuers what they should do.
2. No price predictions.
3. No investment advice.
4. Every factual claim must carry an inline [n] citation.
5. If context is insufficient, say so — do not speculate.
6. Represent genuine disagreement in the literature when sources conflict.

Be concise, plain academic English. State quantities with units (basis points, etc).
Distinguish statistical insignificance from a true zero effect when sources do so."""

# ── app ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Green Bond Credibility Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten to your GitHub Pages domain after testing
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── singletons ────────────────────────────────────────────────────────────────
_embedder   = None
_collection = None


def embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def collection():
    global _collection
    if _collection is None:
        VECTOR_DIR.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(VECTOR_DIR))
        try:
            _collection = client.get_collection(COLLECTION_NAME)
        except Exception:
            _collection = client.create_collection(
                COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
            )
    return _collection


# ── helpers ───────────────────────────────────────────────────────────────────
def clean(text: str) -> str:
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk(text: str):
    tokens = text.split()
    step   = max(CHUNK_TOKENS - CHUNK_OVERLAP, 1)
    for start in range(0, len(tokens), step):
        piece = tokens[start : start + CHUNK_TOKENS]
        if len(piece) >= 50:
            yield " ".join(piece)


def ingest_pdf(pdf_bytes: bytes, filename: str) -> int:
    import io
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text   = clean("\n".join(p.extract_text() or "" for p in reader.pages))
    chunks = list(chunk(text))
    if not chunks:
        return 0

    col  = collection()
    embs = embedder().encode(chunks, batch_size=32, normalize_embeddings=True)

    # remove existing chunks from this source so re-uploads replace cleanly
    try:
        existing = col.get(where={"source": filename})
        if existing["ids"]:
            col.delete(ids=existing["ids"])
    except Exception:
        pass

    stem = Path(filename).stem
    col.add(
        ids        = [f"{stem}::{i:04d}" for i in range(len(chunks))],
        embeddings = embs.tolist(),
        documents  = chunks,
        metadatas  = [{"source": filename, "chunk_index": i} for i in range(len(chunks))],
    )

    # persist chunk store for reference
    CHUNK_STORE.parent.mkdir(parents=True, exist_ok=True)
    with CHUNK_STORE.open("a", encoding="utf-8") as f:
        for i, c in enumerate(chunks):
            f.write(json.dumps({"id": f"{stem}::{i:04d}", "source": filename,
                                "chunk_index": i, "text": c}) + "\n")
    return len(chunks)


def retrieve(question: str):
    col  = collection()
    if col.count() == 0:
        return [], False
    q    = "Represent this sentence for searching relevant passages: " + question
    emb  = embedder().encode([q], normalize_embeddings=True)
    res  = col.query(query_embeddings=emb.tolist(), n_results=min(TOP_K, col.count()))
    hits = [
        {"text": doc, "source": meta["source"], "score": 1.0 - dist}
        for doc, meta, dist in zip(
            res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]
    confident = bool(hits) and hits[0]["score"] >= MIN_SIMILARITY
    return hits, confident


# ── endpoints ─────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/status")
def status():
    col = collection()
    n   = col.count()
    sources: list[str] = []
    if n > 0:
        sample  = col.get(limit=min(n, 1000))
        sources = sorted({m["source"] for m in sample["metadatas"]})
    return {"chunk_count": n, "sources": sources}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported.")
    data   = await file.read()
    n      = ingest_pdf(data, file.filename)
    return {"message": f"Ingested {n} chunks from {file.filename}", "chunks": n}


@app.post("/chat")
async def chat(req: ChatRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "Question cannot be empty.")

    hits, confident = retrieve(question)

    if not confident:
        if collection().count() == 0:
            msg = ("No documents have been uploaded yet. "
                   "Please upload the thesis PDF via the admin panel first.")
        else:
            msg = ("The corpus does not contain enough relevant material to answer "
                   "this reliably. Try rephrasing, or check corpus/SOURCES.md for "
                   "what documents are indexed.")

        def no_corpus():
            yield msg
        return StreamingResponse(no_corpus(), media_type="text/plain")

    context = "\n\n---\n\n".join(
        f"[{i+1}] (source: {h['source']})\n{h['text']}"
        for i, h in enumerate(hits)
    )
    user_msg = (
        f"Context passages:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using ONLY the context above. Cite passages inline as [1], [2], etc. "
        "If the context reports a null or insignificant result, state that explicitly. "
        "If context is insufficient, say so instead of speculating."
    )

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def stream():
        with client.messages.stream(
            model      = LLM_MODEL,
            max_tokens = 1200,
            system     = SYSTEM_PROMPT,
            messages   = [{"role": "user", "content": user_msg}],
        ) as s:
            for text in s.text_stream:
                yield text

    return StreamingResponse(stream(), media_type="text/plain")
