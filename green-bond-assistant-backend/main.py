"""Green Bond Credibility Assistant — FastAPI backend (memory-light).

Uses scikit-learn TF-IDF for retrieval instead of sentence-transformers,
so it fits comfortably in Render's 512MB free tier (no PyTorch).
"""

import os
import re
import pickle
from pathlib import Path

import anthropic
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
DATA_DIR          = Path(os.environ.get("DATA_DIR", "/data"))
INDEX_PATH        = DATA_DIR / "tfidf_index.pkl"
CHUNK_TOKENS      = 500
CHUNK_OVERLAP     = 80
TOP_K             = 5
MIN_SIMILARITY    = 0.04
LLM_MODEL         = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are a research assistant specialised in sovereign green bond
credibility and the greenium literature. You answer questions strictly from the
context passages provided, with inline citations [1], [2], etc.

You are a KNOWLEDGE TOOL, not an advisory tool. You summarise what the evidence
says — including null, mixed, and contested findings — with uncertainty attached.

The corpus includes a master's thesis (Ibnat, 2026) whose central empirical
results are NULL EFFECTS of climate-news tone and signalling noise on the greenium
in India and Indonesia, with VIX as the dominant daily pricing driver (0.35-0.48 bp
per SD of log VIX). Report such results faithfully; never reframe a null as positive.

HARD RULES:
1. No policy advice. Never tell governments or issuers what they should do.
2. No price predictions.
3. No investment advice.
4. Every factual claim must carry an inline [n] citation.
5. If context is insufficient, say so - do not speculate.
6. Represent genuine disagreement in the literature when sources conflict.

Be concise, plain academic English. State quantities with units (basis points, etc).
Distinguish statistical insignificance from a true zero effect when sources do so."""

app = FastAPI(title="Green Bond Credibility Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_index = None


def load_index():
    global _index
    if _index is None and INDEX_PATH.exists():
        with INDEX_PATH.open("rb") as f:
            _index = pickle.load(f)
    return _index


def save_index():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with INDEX_PATH.open("wb") as f:
        pickle.dump(_index, f)


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


def rebuild_vectorizer():
    global _index
    chunks = _index["chunks"]
    vec    = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=20000)
    matrix = vec.fit_transform(chunks)
    _index["vectorizer"] = vec
    _index["matrix"]     = matrix


def ingest_pdf(pdf_bytes: bytes, filename: str) -> int:
    global _index
    import io
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text   = clean("\n".join(p.extract_text() or "" for p in reader.pages))
    new_chunks = list(chunk(text))
    if not new_chunks:
        return 0

    if _index is None:
        _index = {"chunks": [], "sources": [], "vectorizer": None, "matrix": None}

    keep = [i for i, s in enumerate(_index["sources"]) if s != filename]
    _index["chunks"]  = [_index["chunks"][i]  for i in keep]
    _index["sources"] = [_index["sources"][i] for i in keep]

    _index["chunks"].extend(new_chunks)
    _index["sources"].extend([filename] * len(new_chunks))

    rebuild_vectorizer()
    save_index()
    return len(new_chunks)


def retrieve(question: str):
    idx = load_index()
    if not idx or not idx["chunks"]:
        return [], False
    q_vec  = idx["vectorizer"].transform([question])
    scores = cosine_similarity(q_vec, idx["matrix"])[0]
    ranked = scores.argsort()[::-1][:TOP_K]
    hits = [
        {"text": idx["chunks"][i], "source": idx["sources"][i], "score": float(scores[i])}
        for i in ranked if scores[i] > 0
    ]
    confident = bool(hits) and hits[0]["score"] >= MIN_SIMILARITY
    return hits, confident


class ChatRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/status")
def status():
    idx = load_index()
    if not idx or not idx["chunks"]:
        return {"chunk_count": 0, "sources": []}
    return {"chunk_count": len(idx["chunks"]), "sources": sorted(set(idx["sources"]))}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported.")
    data = await file.read()
    n    = ingest_pdf(data, file.filename)
    return {"message": f"Ingested {n} chunks from {file.filename}", "chunks": n}


@app.post("/chat")
async def chat(req: ChatRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "Question cannot be empty.")

    hits, confident = retrieve(question)

    if not confident:
        idx = load_index()
        if not idx or not idx["chunks"]:
            msg = ("No documents have been uploaded yet. "
                   "Please upload the thesis PDF via the admin panel first.")
        else:
            msg = ("The corpus does not contain enough relevant material to answer "
                   "this reliably. Try rephrasing your question.")

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
