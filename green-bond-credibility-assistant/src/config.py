"""Central configuration for the Green Bond Credibility Assistant.

All paths and model choices live here so that notebooks, CLI, and eval
share one source of truth (same pattern as the thesis repo's config.py).
"""

from pathlib import Path

# ---------------------------------------------------------------- paths
ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "corpus"            # local-only PDFs/txt (gitignored)
CHUNK_STORE = ROOT / "data" / "chunks.jsonl"
VECTOR_DIR = ROOT / "data" / "chroma"   # persisted vector store
PROMPT_PATH = ROOT / "prompts" / "system_prompt.md"
EVAL_QUESTIONS = ROOT / "eval" / "questions.jsonl"

# ------------------------------------------------------------- chunking
CHUNK_TOKENS = 500          # target chunk size (approx, whitespace tokens)
CHUNK_OVERLAP = 80          # overlap between consecutive chunks

# ------------------------------------------------------------ retrieval
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
TOP_K_RETRIEVE = 12         # candidates pulled from the vector store
TOP_K_FINAL = 5             # chunks passed to the LLM after (re)ranking
USE_RERANKER = False        # flip on once a cross-encoder is trained
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # baseline; swap
                            # for your fine-tuned ModernBERT reranker

# Minimum cosine similarity for the best hit; below this the assistant
# refuses rather than answers (hallucination guard).
MIN_RELEVANCE = 0.35

# ------------------------------------------------------------------ llm
LLM_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1200
