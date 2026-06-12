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
echo "=== Checking index ==="
if [ ! -d "data/chroma" ]; then
    echo "Building index (first time only, ~1 min)..."
    python -m src.ingest
    python -m src.store
else
    echo "Index exists -- skipping rebuild."
fi
python -m src.cli
