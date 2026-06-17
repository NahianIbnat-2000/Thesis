# When Governments Say "Green" — Do Bond Markets Believe Them?

### Political Credibility Signals and the Sovereign Green Bond Greenium in Emerging Markets

**Nahian Ibnat**
MA in Economics, Data & Policy — Central European University
Supervisor: Zoltán Csaba Tóth | 2026

---

## 🎮 Try it yourself — no economics background required

| | |
|---|---|
| 🎮 **[The Greenium Game](https://nahianibnat-2000.github.io/Thesis/Play%20it/greenium_game.html?v=2)** | 20-quarter policy simulation — can you make bond markets believe your green promises? |
| 📊 **[Live Simulator](https://nahianibnat-2000.github.io/Thesis/live_simulator/greenium_live_simulator.html)** | Stream the greenium in real time, fire credibility events, inject VIX shocks |
| 🎬 **[Animated Explainer](https://nahianibnat-2000.github.io/Thesis/live_simulator/greenium_explainer.html)** | One-minute animated walkthrough of the core finding — autoplays, or pause and scrub |
| 🤖 **[Green Bond Credibility Assistant](https://nahianibnat-2000.github.io/Thesis/chatbot.html)** | Chat with a research assistant trained on the thesis — citations enforced, null results reported honestly |

---

## Overview

This repository contains the data, code, and written chapters for my MA thesis. The study asks whether **political credibility signals** — proxied by the tone and dispersion of climate-related news — shift the **greenium**, the yield discount on a sovereign green bond relative to a maturity-matched conventional twin, in emerging market economies.

The core sample is **India and Indonesia**, with **Germany and Denmark** serving as a developed-market robustness benchmark. The empirical design is a **twin-bond stacked Difference-in-Differences (DiD)** estimator anchored on two political shocks, with climate-news tone measured from **GDELT V2Tone**.

**Headline result:** In the Asian sample, the political-credibility channel does not move the greenium. All three hypotheses return null. Global risk appetite (VIX) is the dominant pricing driver. A persistent, statistically meaningful greenium *is* recovered in the European benchmark, suggesting the null is specific to the thin, illiquid emerging-market green bond segment rather than a universal feature of sovereign green debt.

---

## Key Findings

| Hypothesis | Channel | Result (Asian sample) |
| --- | --- | --- |
| **H1** | Climate-news tone → greenium | **Null** — daily tone does not predict the greenium in any specification |
| **H2** | Signalling noise (tone dispersion) → greenium | **Null** — no robust relationship between within-day tone dispersion and the greenium |
| **H3** | Inaugural issuance → structural shift in greenium | **Null** — neither treatment event produces a significant break |

- **VIX is the only robust driver** of daily greenium movements in Asia. The coefficient of roughly **−0.0035 to −0.0048 percentage points** translates to about **0.35–0.48 basis points** per standard deviation change in log(VIX) — an economically modest but statistically robust effect across all specifications, pointing to global risk appetite rather than domestic climate politics as the pricing anchor.
- **European robustness check** recovers persistent greeniums of approximately **−1.82 bp (Germany)** and **−2.80 bp (Denmark)**, consistent with the established developed-market green bond literature and confirming the Asian null is not a methodological artifact.

> **Interpretation note:** "Null" here means *precise* nulls — tightly estimated coefficients near zero with p-values around 0.4–0.6, not merely statistically insignificant noisy estimates. The ±6.5 bp confidence interval does contain the Ando et al. benchmark greenium, and the two-country sample limits statistical power.

---

## Empirical Design

### Twin-Bond Framework

Each sovereign green bond is paired with a single **maturity-matched (10Y) conventional twin** from the same issuer. The greenium is the daily yield spread (Green − Conventional), in basis points. One strict twin pair is used per country:

| Country | Green bond (ISIN) | Conventional twin (ISIN) | Coupon | Maturity |
| --- | --- | --- | --- | --- |
| India | IN0020220144 | IN0020190362 | 7.26% | 22 Jan 2033 |
| Indonesia | US71567RAV87 | US455780DN36 | 4.45% | 20 Apr 2032 |
| Germany | DE0001030708 | DE0001102507 | 0% | 15 Aug 2030 |
| Denmark | DK0009924375 | DK0009924102 | 0% | 15 Nov 2031 |

### Stacked DiD and Treatment Events

The design stacks two treatment cohorts and estimates a pooled DiD with cohort-specific event windows of ±180 calendar days:

| Stack | Country | Event | Date |
| --- | --- | --- | --- |
| A | Indonesia | JETP announcement (G20 Bali Summit) | 15 November 2022 |
| B | India | 2nd sovereign green bond auction | 27 October 2023 |

> **Why the 2nd auction for India, not the inaugural?** India's inaugural green bond auction (January 2023) leaves effectively no pre-treatment trading history for the green leg. The October 2023 second auction provides roughly **120 trading days of pre-treatment variation**, which is required for credible parallel-trends testing. F(9,84) = 1.006, p = 0.44 — the identification holds cleanly.

### Identification and Inference

- **Five model specifications (M1–M5)**, building from a baseline greenium regression to fully controlled stacked DiD with pair and monthly time fixed effects.
- **HC3 heteroskedasticity-robust** and **panel-corrected (PCSE)** standard errors throughout.
- **Event study** with leads and lags to test pre-trends and dynamic effects (Roth, 2022).
- **Placebo tests** shifting both treatment dates by −3, +3, and +6 months — all null.
- **Granger causality tests** — reverse causality detected for India at lags 2–4 (Greenium → Noise), reported in Appendix I.
- **European benchmark** (Germany, Denmark) as out-of-sample robustness on the same twin-bond logic.

### Key Variables

| Variable | Description |
| --- | --- |
| `greenium` | Daily yield spread (Green − Conventional), in basis points |
| `tone` (V2Tone) | GDELT average daily climate-news tone — a proxy for the climate information environment |
| `signalling_noise` | Within-day standard deviation of V2Tone (credibility-gap proxy) |
| `dlog_vix` | Log-differenced CBOE VIX |
| `dcds` | First-differenced sovereign CDS spread |
| `dfx` | First-differenced log exchange rate |

> **Note on ClimateBERT:** ClimateBERT was evaluated as an alternative tone measure but **dropped from the main analysis**. Applied to GDELT output it scored theme codes rather than natural-language sentences, producing degenerate results. GDELT V2Tone is the primary and reported tone proxy. ClimateBERT results are retained as a robustness note only.

---

## Data Sources

| Variable | Source | Frequency |
| --- | --- | --- |
| Sovereign green & conventional bond yields | Refinitiv / LSEG Workspace (via CEU) | Daily |
| Climate-news tone (V2Tone) | GDELT Project (BigQuery) | Daily |
| VIX (volatility index) | FRED | Daily |
| Exchange rates (USD/INR, USD/IDR) | Refinitiv / LSEG Workspace | Daily |
| Sovereign CDS spreads | Investing.com | Daily |

**Coverage:** 2020–2024
**Countries:** India, Indonesia (core); Germany, Denmark (robustness).
**Note:** Thailand was excluded — no tradeable sovereign green bond with verifiable secondary-market yield data could be identified on Refinitiv.

Full provenance, the twin-bond ISIN pairs, and the layout of `raw/` and `processed/` are documented in [`data/README.md`](data/README.md). The CEU institutional Refinitiv/LSEG subscription permits redistribution of the extracted series included here.

---

## Repository Structure

```
Thesis/
├── Play it/
│   ├── greenium_game.html           # 🎮 Interactive policy game (play in browser)
│   └── README.md                    # How to play
├── live_simulator/
│   ├── greenium_live_simulator.html # 📊 Live streaming simulator (open in browser)
│   ├── greenium_explainer.html      # 🎬 Animated explainer (autoplay walkthrough)
│   └── README.md                    # How to use the simulator
├── green-bond-credibility-assistant/  # 🤖 Full RAG version (dense embeddings, see §3)
│   ├── src/                         # Ingest, store, retrieve, generate, CLI
│   ├── prompts/                     # System prompt encoding the assistant's charter
│   ├── eval/                        # 15-question evaluation set with trap-null tests
│   ├── corpus/                      # Local PDFs only — gitignored (see SOURCES.md)
│   └── scripts/run.sh               # One-command setup and launch
├── green-bond-assistant-backend/    # 🌐 Hosted backend (FastAPI + TF-IDF, deploys to Render)
│   ├── main.py                      # API: /chat, /status, /health
│   ├── thesis_corpus.txt            # Bundled thesis text, indexed on startup
│   ├── render.yaml                  # Render deployment config
│   └── requirements.txt
├── index.html                       # 🏠 Project landing page (GitHub Pages)
├── chatbot.html                     # 🤖 Public chat UI (GitHub Pages)
├── data/
│   ├── raw/                         # Bond yields, VIX, FX, CDS (CEU-licensed for release)
│   ├── processed/                   # GDELT tone panel + analysis-ready regression panel
│   └── README.md                    # Data provenance and source table
├── notebooks/                       # Regression, event study, GDELT/tone pipelines
├── output/                          # Figures, tables, and rendered (executed) notebooks
├── presentation/                    # Thesis defence slides
├── Nahian_Ibnat_2026_MA_Thesis.pdf  # 📄 Full thesis (final submitted version)
├── AI_Declaration_Nahian_Ibnat.pdf
├── requirements.txt                 # Loose ranges for a quick start
├── requirements-lock.txt            # Pinned versions for exact reproduction
├── .python-version                  # Pinned Python version (3.10)
└── thesis_latex.zip                 # LaTeX source of the written thesis
```

---

## Environment

- Python 3.10+ (pinned in `.python-version`)
- Quick start: `pip install -r requirements.txt`
- Exact reproduction: `pip install -r requirements-lock.txt` (deterministic, pinned versions from the environment that produced the reported results)

| Package | Purpose |
| --- | --- |
| `pandas`, `numpy` | Panel construction and data manipulation |
| `statsmodels` | OLS, DiD, Durbin-Watson, VIF, Granger causality |
| `linearmodels` | PanelOLS, stacked DiD with pair and time fixed effects |
| `scipy` | Statistical tests in the event study |
| `matplotlib` | All thesis figures |
| `requests` / BigQuery client | GDELT V2Tone extraction |
| `openpyxl` | Excel I/O for raw bond data |
| `transformers`, `torch` | ClimateBERT sentiment pipeline only (dropped from the main analysis; see note above) |

Bond data was accessed via Refinitiv (LSEG Workspace) through the CEU Library institutional subscription, which permits redistribution of the extracted series included in `data/`.

---

## How to Reproduce

The repository is built so that **every quantitative claim in the thesis can be verified without re-running anything**, and fully re-run if you want to.

### Verify without running (no setup, no data pull)

1. **Read the executed notebooks.** Fully-rendered versions of all four analysis notebooks, with every cell output, table, and figure intact, are in [`output/html/`](output/html/). Open them in a browser — no Python, no execution. These are the canonical record of what each cell produced.
2. **Check the processed panels.** The analysis-ready CSVs the regressions consume are committed under [`data/processed/`](data/processed/). The figures and tables used in Chapters 4–5 are in [`output/`](output/).

### Re-run the full pipeline

All inputs are included (see [`data/README.md`](data/README.md) for provenance), so the analysis runs end to end:

1. **Environment:** `pip install -r requirements.txt` (or `requirements-lock.txt` for exact versions).
2. **Tone data (optional):** the GDELT V2Tone panel is already in `data/processed/gdelt/`. To regenerate it from BigQuery, run the GDELT notebook in `notebooks/sentiment_colab/`.
3. **Regressions:** run `notebooks/GreenBond_Regression.ipynb` to reproduce M1–M5, robustness checks, and coefficient plots.
4. **Event study:** run `notebooks/GreenBond_EventStudy.ipynb` for leads/lags and parallel-trends diagnostics.
5. **European benchmark:** run `notebooks/GreenBond_Regression_Europe.ipynb` and `GreenBond_EventStudy_Europe.ipynb` for the Germany/Denmark estimates.

All outputs are written to `output/`. The notebooks read from `data/` with relative paths, so no path editing is needed.

---

## 🤖 Green Bond Credibility Assistant

A retrieval-augmented research assistant built on top of this thesis. It answers questions about what the evidence says on sovereign green bond credibility and the greenium — with citations and with the uncertainty attached, including null results reported honestly.

**It is a knowledge tool, not an advisory tool.** It will not tell you what a government should do to improve its greenium (the thesis itself is the argument against that). It tells you what the literature documents, where the evidence is contested, and where it is simply absent. It refuses policy advice, price predictions, and investment recommendations by design, and it reports the thesis's null results faithfully rather than inventing positive effects.

**Features:** inline citations on every claim, a refusal guard that declines low-confidence or out-of-scope questions instead of speculating, and browser-side session memory so follow-up questions ("why is that?") work.

There are three ways to use it, from easiest to most technical:

### 1. Live web chat (recommended — no setup)

**▶️ [Open the live assistant](https://nahianibnat-2000.github.io/Thesis/chatbot.html)** — no login, no API key, just open and ask.

This is the hosted version anyone can use. The chat interface runs on GitHub Pages and talks to a FastAPI backend deployed on Render, which indexes the thesis with a TF-IDF retriever and passes the top passages to Claude under a citation-enforcing system prompt with a hard no-advice charter.

### 2. Deploy your own backend (Render)

The backend lives in [`green-bond-assistant-backend/`](green-bond-assistant-backend/). To host your own copy:

1. On [render.com](https://render.com) → New → Web Service → connect this repo
2. Set **Root Directory** to `green-bond-assistant-backend`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable `ANTHROPIC_API_KEY`
5. Deploy, then point `chatbot.html`'s `BACKEND` constant at your Render URL

The thesis corpus (`thesis_corpus.txt`) is bundled and indexed automatically on startup, so no persistent disk or manual upload is required. A free uptime pinger (e.g. UptimeRobot hitting `/health`) keeps the free instance from sleeping.

### 3. Full RAG version in a Codespace (developers)

The repository also contains a fuller dense-retrieval implementation in [`green-bond-credibility-assistant/`](green-bond-credibility-assistant/) — `bge-small-en-v1.5` embeddings, a ChromaDB vector store, an optional cross-encoder reranker, and a 15-question evaluation set including *trap-null questions* that presuppose an effect the thesis does not find (a correct answer reports the null and the ±6.5 bp confidence interval).

### Run it

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/NahianIbnat-2000/Thesis)

Once the Codespace opens:

```bash
bash green-bond-credibility-assistant/scripts/run.sh
```

You will need a free Anthropic API key from [console.anthropic.com](https://console.anthropic.com) (~$5 credit covers hundreds of queries). The corpus is not redistributed — see `green-bond-credibility-assistant/corpus/SOURCES.md` for the full source list.

---

## Citation

```
Ibnat, N. (2026). When Governments Say 'Green' — Do Bond Markets Believe Them?
MA Thesis, Department of Economics, Central European University — Private University, Vienna.
```

---

## Feedback

Have questions about the thesis or the interactive tools?
[📬 Open the feedback form](https://forms.gle/YMKYULpfnAX5dyV4A)

---

## Contact

**Nahian Ibnat**
MA in Economics, Data & Policy — Central European University
