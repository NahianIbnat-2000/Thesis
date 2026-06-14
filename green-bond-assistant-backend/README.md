# green-bond-assistant-backend

FastAPI backend for the Green Bond Credibility Assistant.
This folder lives inside the main Thesis repo and deploys to Render.com.

## Deploy to Render (one-time)

1. This folder is already in your Thesis repo at `green-bond-assistant-backend/`
2. Go to render.com → New → Web Service → connect the **Thesis** repo
3. **IMPORTANT:** set **Root Directory** to `green-bond-assistant-backend`
4. Render auto-detects the rest from `render.yaml`
5. In Render dashboard → Environment → add `ANTHROPIC_API_KEY`
6. Add a persistent disk: Name `corpus-data`, Mount path `/data`, Size 1GB
7. Deploy — get your URL (e.g. `https://green-bond-assistant.onrender.com`)
8. Update the `BACKEND` constant in `chatbot.html` (in the repo root) with that URL

## Upload corpus (one-time after deploy)

Open `admin.html` locally in your browser, enter your Render URL, upload PDFs.
The index persists on Render's attached disk between restarts.

## Endpoints

| Method | Path      | Description                    |
|--------|-----------|--------------------------------|
| GET    | /health   | Liveness check                 |
| GET    | /status   | Chunk count and source list    |
| POST   | /upload   | Upload a PDF (multipart/form)  |
| POST   | /chat     | { "question": "..." } → stream |
