#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "=== Installing dependencies ==="
pip install -r requirements.txt -q
echo "=== Checking API key ==="
if [ -z "$ANTHROPIC_API_KEY" ]; then
    read -rp "Paste your Anthropic API key: " key
    export ANTHROPIC_API_KEY="$key"
fi
echo "=== Checking corpus ==="
if [ ! -f "corpus/ibnat_thesis_2026.pdf" ]; then
    THESIS_PDF="$(dirname "$0")/../../Nahian_Ibnat_2026_MA_Thesis.pdf"
    if [ -f "$THESIS_PDF" ]; then
        echo "Copying thesis PDF into corpus..."
        cp "$THESIS_PDF" corpus/ibnat_thesis_2026.pdf
    else
        echo "WARNING: thesis PDF not found -- add it manually to corpus/ (see corpus/SOURCES.md)"
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
