"""Build and query the ChromaDB vector store.

Usage:
    python -m src.store          # (re)build the index from chunks.jsonl
"""

import json

import chromadb
from sentence_transformers import SentenceTransformer

from src import config

COLLECTION = "green_bond_corpus"

_model = None  # lazy singleton


def embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBED_MODEL)
    return _model


def client() -> chromadb.PersistentClient:
    config.VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(config.VECTOR_DIR))


def build() -> None:
    records = [
        json.loads(line)
        for line in config.CHUNK_STORE.read_text(encoding="utf-8").splitlines()
    ]
    if not records:
        raise SystemExit("chunks.jsonl is empty — run `python -m src.ingest` first.")

    co = client()
    try:
        co.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = co.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    texts = [r["text"] for r in records]
    # bge models expect no prefix for passages; queries get a prefix below.
    embeddings = embedder().encode(texts, batch_size=64, show_progress_bar=True,
                                   normalize_embeddings=True)
    collection.add(
        ids=[r["id"] for r in records],
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[{"source": r["source"], "chunk_index": r["chunk_index"]}
                   for r in records],
    )
    print(f"Indexed {len(records)} chunks into {config.VECTOR_DIR}")


def query(text: str, k: int):
    """Return list of dicts: {id, text, source, score} sorted by similarity."""
    co = client()
    collection = co.get_collection(COLLECTION)
    # bge-small recommends a query instruction prefix for retrieval tasks.
    q = "Represent this sentence for searching relevant passages: " + text
    emb = embedder().encode([q], normalize_embeddings=True)
    res = collection.query(query_embeddings=emb.tolist(), n_results=k)
    hits = []
    for id_, doc, meta, dist in zip(
        res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        hits.append({
            "id": id_,
            "text": doc,
            "source": meta["source"],
            "score": 1.0 - dist,  # cosine distance -> similarity
        })
    return hits


if __name__ == "__main__":
    build()
