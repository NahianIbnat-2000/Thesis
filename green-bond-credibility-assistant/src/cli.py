"""Interactive CLI for the Green Bond Credibility Assistant.

Usage:
    python -m src.cli "What drives the sovereign greenium in emerging markets?"
    python -m src.cli            # interactive loop
"""

import sys

from src import generate


def ask(question: str) -> None:
    result = generate.answer(question)
    print("\n" + result["answer"] + "\n")
    if result["sources"]:
        print("Sources:")
        for s in result["sources"]:
            print(f"  [{s['n']}] {s['source']}  ({s['id']})")


def main() -> None:
    if len(sys.argv) > 1:
        ask(" ".join(sys.argv[1:]))
        return
    print("Green Bond Credibility Assistant — Ctrl-C to exit.")
    while True:
        try:
            question = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if question:
            ask(question)


if __name__ == "__main__":
    main()
