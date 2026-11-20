# green-bond-assistant-backend

FastAPI backend for the Green Bond Credibility Assistant on the thesis website
(`chatbot.html`). This folder lives inside the main Thesis repo and deploys to Render.

## How it works

- **Corpus:** `thesis_corpus.txt` (the thesis text), bundled in this folder and indexed
  automatically at startup. No upload step and no persistent disk.
- **Retrieval:** scikit-learn TF-IDF (word 1-2 grams), cosine similarity, top 8 chunks of
  500 words with 80 words of overlap. If the best match scores below 0.04, the assistant
  returns a fixed "not enough relevant material" message instead of calling the model.
- **Follow-up questions:** when a question is short or uses a pronoun, the previous user
  question is added to the search query. History stays in the visitor's browser; the
  backend stores nothing.
- **Generation:** Anthropic Claude (`LLM_MODEL` in `main.py`), streamed as plain text, with
  inline `[1]`, `[2]` citations requested by the system prompt. Citations are not
  validated automatically.
- **No PyTorch**, so it fits a 512 MB free instance.

## Safeguards

- Per-IP rate limit on `/chat`: 10 per minute, 100 per day (slowapi).
- CORS limited to `https://nahianibnat-2000.github.io` (plus localhost for testing).
- Caps on question length (2,000 characters), history depth (8 turns) and turn length.
- No write endpoints.

## Endpoints

| Method | Path      | Description                         |
|--------|-----------|-------------------------------------|
| GET    | /health   | Liveness check                      |
| GET    | /status   | Chunk count and source list         |
| POST   | /chat     | `{"question": "...", "history": []}` → streamed text |

## Deploy to Render

1. render.com → New → Web Service → connect the **Thesis** repo.
2. Set **Root Directory** to `green-bond-assistant-backend`.
3. Build command `pip install -r requirements.txt`, start command
   `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. Add the environment variable `ANTHROPIC_API_KEY`.
5. Deploy, then set the `BACKEND` constant in `chatbot.html` (repo root) to the service URL.

To update the corpus, replace `thesis_corpus.txt` and redeploy.

Note: `render.yaml` still contains a `disk` block and a `DATA_DIR` variable from an earlier
version. `main.py` uses neither. They can be removed after checking that the live service
was not created from this blueprint with a disk attached.
