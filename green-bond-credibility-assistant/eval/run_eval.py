"""Evaluation harness.

Two metrics, deliberately simple and inspectable:

1. Retrieval hit-rate: for questions with `expect_sources`, did at least
   one retrieved chunk come from an expected source file? (substring match
   on filename, so "thesis" matches "ibnat_thesis_2026.pdf").
2. Keyword faithfulness: does the generated answer contain at least one
   `expect_keywords` entry (case-insensitive)? Crude, but it catches the
   failure mode that matters most here: trap_null questions answered with
   invented positive effects, and boundary questions answered with advice.

Optional richer metrics (RAGAS faithfulness/answer-relevance) can be added
later; keep this harness dependency-light so it always runs.

Usage:
    python -m eval.run_eval               # retrieval only (no API key needed)
    python -m eval.run_eval --generate    # also score generated answers
"""

import argparse
import json

from src import config, retrieve


def load_questions() -> list[dict]:
    return [
        json.loads(line)
        for line in config.EVAL_QUESTIONS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def retrieval_hit(q: dict, hits: list[dict]) -> bool | None:
    expected = q.get("expect_sources")
    if not expected:
        return None
    sources = " ".join(h["source"].lower() for h in hits)
    return any(e.lower().split("_")[0] in sources for e in expected)


def keyword_hit(q: dict, answer: str) -> bool | None:
    expected = q.get("expect_keywords")
    if not expected:
        return None
    low = answer.lower()
    return any(k.lower() in low for k in expected)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true",
                        help="also generate answers and score keywords (uses API)")
    args = parser.parse_args()

    questions = load_questions()
    r_scores, k_scores, rows = [], [], []

    for q in questions:
        hits, confident = retrieve.retrieve(q["question"])
        r = retrieval_hit(q, hits)
        if r is not None:
            r_scores.append(r)

        k = None
        if args.generate:
            from src import generate
            result = generate.answer(q["question"])
            k = keyword_hit(q, result["answer"])
            if k is not None:
                k_scores.append(k)

        rows.append((q["id"], q["type"], r, k, confident))

    print(f"\n{'id':<6}{'type':<12}{'retrieval':<11}{'keywords':<10}{'confident'}")
    for id_, type_, r, k, c in rows:
        fmt = lambda v: "-" if v is None else ("PASS" if v else "FAIL")
        print(f"{id_:<6}{type_:<12}{fmt(r):<11}{fmt(k):<10}{c}")

    if r_scores:
        print(f"\nRetrieval hit-rate: {sum(r_scores)}/{len(r_scores)} "
              f"({100 * sum(r_scores) / len(r_scores):.0f}%)")
    if k_scores:
        print(f"Keyword faithfulness: {sum(k_scores)}/{len(k_scores)} "
              f"({100 * sum(k_scores) / len(k_scores):.0f}%)")


if __name__ == "__main__":
    main()
