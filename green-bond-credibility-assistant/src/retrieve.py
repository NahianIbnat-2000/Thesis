"""Retrieve-then-rerank pipeline with a relevance refusal guard.

Pattern: dense retrieval pulls TOP_K_RETRIEVE candidates; an optional
cross-encoder reranks them (Nogueira & Cho, 2019); the top TOP_K_FINAL
are returned. If the best similarity falls below MIN_RELEVANCE, the
caller should refuse to answer rather than let the LLM improvise.
"""

from src import config, store

_reranker = None


def _rerank(question: str, hits: list[dict]) -> list[dict]:
    global _reranker
    if _reranker is None:
        from sentence_transformers import CrossEncoder
        _reranker = CrossEncoder(config.RERANKER_MODEL)
    scores = _reranker.predict([(question, h["text"]) for h in hits])
    for h, s in zip(hits, scores):
        h["rerank_score"] = float(s)
    return sorted(hits, key=lambda h: h["rerank_score"], reverse=True)


def retrieve(question: str) -> tuple[list[dict], bool]:
    """Return (top chunks, confident). confident=False means the refusal
    guard tripped and the assistant should decline to answer."""
    hits = store.query(question, k=config.TOP_K_RETRIEVE)
    confident = bool(hits) and hits[0]["score"] >= config.MIN_RELEVANCE
    if config.USE_RERANKER and hits:
        hits = _rerank(question, hits)
    return hits[: config.TOP_K_FINAL], confident
