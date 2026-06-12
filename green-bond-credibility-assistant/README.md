# Green Bond Credibility Assistant

A retrieval-augmented research assistant for the sovereign green bond
("greenium") literature — built on top of my MA thesis,
[*When Governments Say "Green" — Do Bond Markets Believe Them?*](https://github.com/NahianIbnat-2000/Thesis)
(CEU, 2026).

**It is a knowledge tool, not an advisory tool.** It answers questions about
what the evidence says — with citations and with the uncertainty attached —
and it is explicitly designed to report **null results honestly**. That
design choice comes directly from the thesis: across five stacked
difference-in-differences specifications, climate-news tone and signaling
noise show no detectable effect on the greenium in India and Indonesia,
while global risk appetite (VIX) dominates daily pricing. A research
assistant that quietly converted those nulls into positive findings would
be worse than no assistant at all.

## What it does

- Answers questions over a **curated ~30-document corpus**: the thesis, the
  core greenium literature (Zerbib 2019; Ando et al. 2024; Larcker & Watts
  2020; Flammer 2021), DiD methodology papers, and primary policy documents
  (ICMA Green Bond Principles, India/Indonesia sovereign green frameworks,
  the Indonesia JETP statement, second-party opinions).
- Cites every claim inline and lists its source chunks.
- **Refuses** when retrieval confidence is low, when asked for policy
  prescriptions ("what should Indonesia do…"), or for investment advice.
- Represents genuine disagreement in the literature (e.g., Larcker & Watts'
  near-zero greenium vs. positive estimates elsewhere).

## Architecture

```
corpus/ (local PDFs, gitignored)
   │  src/ingest.py        ~500-token overlapping chunks
   ▼
data/chunks.jsonl
   │  src/store.py         bge-small-en-v1.5 embeddings → ChromaDB (cosine)
   ▼
src/retrieve.py            top-12 dense retrieval → optional cross-encoder
   │                       rerank (Nogueira & Cho, 2019) → top-5
   │                       + refusal guard on low max-similarity
   ▼
src/generate.py            Claude + prompts/system_prompt.md
                           (charter: cite, report nulls, never advise)
```

The reranker slot (`USE_RERANKER` in `src/config.py`) ships with an
off-the-shelf MS-MARCO cross-encoder and is designed to be swapped for a
domain-fine-tuned ModernBERT reranker — the same distillation pipeline I
built for a deep learning course (32B Qwen3 teacher → 149M ModernBERT
student) applies directly.

## Evaluation

`eval/questions.jsonl` contains 15 questions across five types, scored by
`eval/run_eval.py` on retrieval hit-rate and keyword faithfulness:

| Type | Tests |
|---|---|
| `factual` | standard retrieval + grounded answering |
| `trap_null` | questions that **presuppose an effect the evidence rejects** ("how much does climate news tone move the Indian greenium?") — a correct answer reports the null and the ±6.5 bp confidence interval |
| `contested` | must present both sides of the greenium-existence debate |
| `boundary` | must refuse policy and investment advice |
| `refusal` | out-of-corpus questions must trigger the refusal guard |

The trap-null questions are the point of the project: they translate the
thesis's epistemics into an eval design.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env            # add your ANTHROPIC_API_KEY
# place corpus documents per corpus/SOURCES.md, then:
python -m src.ingest
python -m src.store
python -m src.cli "Is there a consensus that a greenium exists?"
python -m eval.run_eval --generate
```

The corpus is not redistributed in this repo (copyright); `corpus/SOURCES.md`
documents exactly what to obtain and how to name it.

## Scope and limitations

- Answers are only as good as the curated corpus; it is small by design.
- The thesis evidence covers four countries and one twin pair each, with a
  confidence interval wide enough to contain benchmark greenium estimates —
  the assistant is instructed to surface that, not hide it.
- No price prediction, no policy prescription, no investment advice. Asking
  for them returns a refusal — that behavior is part of the test suite.

## License

MIT (code only; corpus documents retain their original rights).
