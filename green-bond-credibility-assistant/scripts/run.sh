#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd "$PROJECT_DIR/.." && pwd)"
cd "$PROJECT_DIR"
echo "=== Installing dependencies ==="
pip install -r requirements.txt -q
echo "=== Checking API key ==="
if [ -z "$ANTHROPIC_API_KEY" ]; then
    read -rp "Paste your Anthropic API key: " key
    export ANTHROPIC_API_KEY="$key"
fi
echo "=== Checking corpus ==="
if [ ! -f "corpus/ibnat_thesis_2026.pdf" ]; then
    THESIS_PDF="$REPO_DIR/Nahian_Ibnat_2026_MA_Thesis.pdf"
    if [ -f "$THESIS_PDF" ]; then
        echo "Copying thesis PDF into corpus..."
        cp "$THESIS_PDF" corpus/ibnat_thesis_2026.pdf
    else
        echo "WARNING: thesis PDF not found -- add it manually to corpus/"
    fi
fi
echo "=== Checking index ==="
if [ ! -d "data/chroma" ]; then
    echo "Building index (first time only, ~1 min)..."
    python -m src.ingest
    python -m src.store
else
    echo "Index exists -- skipping rebuild."
fi
python -m src.cli
