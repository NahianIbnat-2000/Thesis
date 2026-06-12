"""Generate a cited answer from retrieved chunks via the Anthropic API.

Requires ANTHROPIC_API_KEY in the environment (see .env.example).
"""

import os

import anthropic

from src import config, retrieve

REFUSAL = (
    "The curated corpus does not contain enough relevant material to answer "
    "this reliably, so I won't guess. Try rephrasing, or check whether the "
    "topic is covered by the sources listed in corpus/SOURCES.md."
)


def _system_prompt() -> str:
    return config.PROMPT_PATH.read_text(encoding="utf-8")


def _format_context(hits: list[dict]) -> str:
    blocks = []
    for i, h in enumerate(hits, 1):
        blocks.append(f"[{i}] (source: {h['source']})\n{h['text']}")
    return "\n\n---\n\n".join(blocks)


def answer(question: str) -> dict:
    """Return {'answer': str, 'sources': list, 'refused': bool}."""
    hits, confident = retrieve.retrieve(question)
    if not confident:
        return {"answer": REFUSAL, "sources": [], "refused": True}

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    user_msg = (
        f"Context passages:\n\n{_format_context(hits)}\n\n"
        f"Question: {question}\n\n"
        "Answer using ONLY the context above. Cite passages inline as [1], "
        "[2], etc. If the context reports a null or insignificant result, "
        "state that explicitly — do not soften it into a positive finding. "
        "If the context is insufficient, say so instead of speculating."
    )
    resp = client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=config.MAX_TOKENS,
        system=_system_prompt(),
        messages=[{"role": "user", "content": user_msg}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    return {
        "answer": text,
        "sources": [{"n": i + 1, "source": h["source"], "id": h["id"]}
                    for i, h in enumerate(hits)],
        "refused": False,
    }
