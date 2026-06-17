"""Green Bond Credibility Assistant — FastAPI backend (memory-light, self-contained).

Uses scikit-learn TF-IDF for retrieval (no PyTorch, fits 512MB free tier).
The thesis corpus is bundled as thesis_corpus.txt and indexed automatically on
startup — no persistent disk and no manual upload required.

Session memory: the frontend sends recent conversation history with each request.
History lives in the user's browser only; the backend stores nothing.

Public-deployment hardening:
  * Per-IP rate limiting on /chat (slowapi) so a burst cannot drain API credits.
  * CORS restricted to the GitHub Pages origin.
  * Request-size caps on question length and history depth.
  * No write endpoints: the corpus is read-only and loaded once at startup.
"""

import os
import re
import glob
from pathlib import Path

import anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
BASE_DIR          = Path(__file__).resolve().parent
CHUNK_TOKENS      = 500
CHUNK_OVERLAP     = 80
TOP_K             = 8
MIN_SIMILARITY    = 0.04
LLM_MODEL         = "claude-sonnet-4-6"
MAX_HISTORY       = 8          # cap conversation turns sent to the model
MAX_QUESTION_CHARS = 2000      # reject absurdly long questions before the paid call
MAX_TURN_CHARS     = 4000      # cap each history turn's length

# Restrict browser access to the public site. Add other origins if you host the
# chat UI elsewhere. (Note: this only stops casual cross-site browser calls;
# the per-IP rate limit below is the real abuse protection.)
ALLOWED_ORIGINS = [
    "https://nahianibnat-2000.github.io",
    "http://localhost:8000",   # local testing
]

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
4. Every factual claim must carry an inline [n] citation referring to the context
   passages provided with the LATEST question.
5. If context is insufficient, say so - do not speculate.
6. Represent genuine disagreement in the literature when sources conflict.

You may use the conversation history to understand follow-up questions (e.g. "why
is that?"), but you must still grow every factual claim from the cited context
passages, not from memory of earlier turns.

Be concise, plain academic English. State quantities with units (basis points, etc).
Distinguish statistical insignificance from a true zero effect when sources do so.
Prefer paraphrasing over long verbatim quotes; if you must quote, keep it short
(under 15 words) and use it only when exact wording matters."""

app = FastAPI(title="Green Bond Credibility Assistant")

# Per-IP rate limiter. Protects the paid /chat endpoint from bursts.
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "HEAD"],
    allow_headers=["*"],
)

_index = {"chunks": [], "sources": [], "vectorizer": None, "matrix": None}


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
    if not _index["chunks"]:
        _index["vectorizer"] = None
        _index["matrix"]     = None
        return
    vec    = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=20000)
    matrix = vec.fit_transform(_index["chunks"])
    _index["vectorizer"] = vec
    _index["matrix"]     = matrix


def add_text(text: str, source: str) -> int:
    new_chunks = list(chunk(clean(text)))
    if not new_chunks:
        return 0
    keep = [i for i, s in enumerate(_index["sources"]) if s != source]
    _index["chunks"]  = [_index["chunks"][i]  for i in keep]
    _index["sources"] = [_index["sources"][i] for i in keep]
    _index["chunks"].extend(new_chunks)
    _index["sources"].extend([source] * len(new_chunks))
    rebuild_vectorizer()
    return len(new_chunks)


def load_bundled_corpus():
    for txt in glob.glob(str(BASE_DIR / "*.txt")):
        if Path(txt).name == "requirements.txt":
            continue
        try:
            text = Path(txt).read_text(encoding="utf-8", errors="ignore")
            n    = add_text(text, Path(txt).name)
            print(f"[startup] indexed {n} chunks from {Path(txt).name}")
        except Exception as e:
            print(f"[startup] failed to index {txt}: {e}")
    for pdf in glob.glob(str(BASE_DIR / "*.pdf")):
        try:
            reader = PdfReader(pdf)
            text   = "\n".join(p.extract_text() or "" for p in reader.pages)
            n      = add_text(text, Path(pdf).name)
            print(f"[startup] indexed {n} chunks from {Path(pdf).name}")
        except Exception as e:
            print(f"[startup] failed to index {pdf}: {e}")


@app.on_event("startup")
def _startup():
    load_bundled_corpus()


def retrieve(question: str):
    if not _index["chunks"] or _index["vectorizer"] is None:
        return [], False
    q_vec  = _index["vectorizer"].transform([question])
    scores = cosine_similarity(q_vec, _index["matrix"])[0]
    ranked = scores.argsort()[::-1][:TOP_K]
    hits = [
        {"text": _index["chunks"][i], "source": _index["sources"][i], "score": float(scores[i])}
        for i in ranked if scores[i] > 0
    ]
    confident = bool(hits) and hits[0]["score"] >= MIN_SIMILARITY
    return hits, confident


class Turn(BaseModel):
    role: str       # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    question: str
    history: list[Turn] = []     # prior turns, oldest first; optional


def retrieval_query(question: str, history: list[Turn]) -> str:
    """Improve retrieval for follow-ups and short questions by blending in the
    most recent user turn. Short or context-dependent questions (e.g. 'why is
    that?', 'who does it mention?') don't carry enough distinctive terms on their
    own for TF-IDF, so we prepend the previous user question to widen recall."""
    prior_user = [t.content for t in history if t.role == "user"]
    # blend whenever the question is short OR clearly references prior context
    refers_back = bool(re.search(
        r"\b(that|this|it|they|them|those|these|he|she|his|her|its|their)\b",
        question.lower()
    ))
    if prior_user and (len(question.split()) <= 6 or refers_back):
        return prior_user[-1] + " " + question
    return question


@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}


@app.get("/status")
def status():
    return {"chunk_count": len(_index["chunks"]), "sources": sorted(set(_index["sources"]))}


@app.post("/chat")
@limiter.limit("10/minute;100/day")
async def chat(request: Request, req: ChatRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "Question cannot be empty.")
    if len(question) > MAX_QUESTION_CHARS:
        raise HTTPException(413, "Question is too long.")

    # cap history depth and per-turn length before anything reaches the paid call
    history = (req.history or [])[-MAX_HISTORY:]
    history = [t for t in history if len(t.content) <= MAX_TURN_CHARS]
    rquery  = retrieval_query(question, history)
    hits, confident = retrieve(rquery)

    if not confident:
        if not _index["chunks"]:
            msg = "The corpus failed to load on startup. Please contact the maintainer."
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

    # build the messages list: prior turns, then the current question with context
    messages = [{"role": t.role, "content": t.content} for t in history]
    messages.append({
        "role": "user",
        "content": (
            f"Context passages for THIS question:\n\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer using ONLY the context above. Cite passages inline as [1], [2], etc. "
            "If the context reports a null or insignificant result, state that explicitly. "
            "If context is insufficient, say so instead of speculating."
        ),
    })

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def stream():
        with client.messages.stream(
            model      = LLM_MODEL,
            max_tokens = 1200,
            system     = SYSTEM_PROMPT,
            messages   = messages,
        ) as s:
            for text in s.text_stream:
                yield text

    return StreamingResponse(stream(), media_type="text/plain")
