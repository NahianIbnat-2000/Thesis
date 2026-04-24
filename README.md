# Do Politicians' Words Have a Dollar Value?
### Measuring the Impact of Climate Policy Sentiment on Sovereign Green Bond Pricing in India and Indonesia

**Nahian Ibnat**  
MA in Economics, Data & Policy — Central European University  
Supervisor: Zoltán Csaba Tóth | April 2026

---

## Overview

This repository contains all data, code, and written chapters for my MA thesis first draft. The content will change as per the Thesis Seminar Comments and Supervisor Comments The study investigates whether daily political climate sentiment influences the **Greenium** — the yield discount on sovereign green bonds relative to maturity-matched conventional twins — in India and Indonesia over 2020–2024.

The empirical design uses a **Twin-Bond quasi-experimental framework** paired with a **staggered Difference-in-Differences (DiD)** estimator, anchored on two political shocks: India's inaugural green bond auction (January 2023) and Indonesia's JETP announcement at the G20 Bali Summit (November 2022). Climate sentiment is measured using **GDELT V2Tone** scores, with a **ClimateBERT** robustness check.

**Key findings:**
- **H1 (Sentiment → Greenium):** Null. Daily climate sentiment does not predict the Greenium in any specification.
- **H2 (Signaling Noise → Greenium):** Significant (p < 0.001). Higher within-day media tone dispersion is associated with a wider, not narrower, Greenium — opposite to the hypothesised Credibility Gap direction.
- **H3 (Political Events → Structural Break):** Null. Neither treatment event produces a significant break, though parallel trends hold in both cases.
- **VIX** is the only robust predictor of daily Greenium movements (β = −0.0035, p < 0.001), pointing to global risk appetite as the dominant driver.

---

## Repository Structure

```
Thesis/
│
├── chapters/                        # Written thesis chapters
│   ├── tex_code/                    # LaTeX source files
│   │   ├── Chapter1_Introduction.tex
│   │   ├── Chapter2_Lit.tex
│   │   ├── Chapter3_Data.tex
│   │   ├── Chapter4_Methodology.tex
│   │   ├── Chapter5_Result.tex
│   │   └── Chapter7_Limitations.tex
│   ├── Chapter1_Introduction.pdf
│   ├── Chapter2_LiteratureReview.pdf
│   ├── Chapter3_Data.pdf
│   ├── Chapter4_Methodology.pdf
│   ├── Chapter5_Results.pdf
│   ├── Chapter7_Limitation.pdf
│   ├── Proposal.pdf
│   └── Thesis_Outline.pdf
│
├── data/
│   ├── raw/
│   │   ├── bond_yield_data/
│   │   │   ├── india_bond/          # India sovereign green & conventional twin bond yields (Refinitiv)
│   │   │   └── indonesia_bond/      # Indonesia sovereign green & conventional twin bond yields (Refinitiv)
│   │   └── control_variables/
│   │       ├── vix/                 # CBOE VIX index (FRED)
│   │       ├── exchange_rate/       # USD/INR & USD/IDR exchange rates (Refinitiv)
│   │       └── cds/                 # Sovereign CDS spreads (Investing.com)
│   └── processed/
│   │   ├── gdelt/
│   │   │   ├── daily_sentiment_gdelt.csv    # GDELT V2Tone daily climate sentiment
│   │   │   ├── daily_climatebert.csv        # ClimateBERT sentence-level scores
│   │   │   └── daily_sentiment_merged.csv   # Merged sentiment panel
│   │   └── regression/
│   │       └── regression_panel.csv         # Final analysis-ready panel dataset
│   └── documentation/
│       ├── DataCollection.pdf           # Data sourcing documentation
│       └── GreenBond_DataSources.html   # Interactive data source reference
│       
├── notebooks/
│   ├── databricks/                  # Production notebooks (run on Databricks)
│   │   ├── GreenBond_Regression.ipynb       # DiD regression & robustness checks
│   │   └── GreenBond_EventStudy.ipynb       # Event study with leads/lags
│   └── sentiment_colab/             # NLP notebooks (run on Google Colab)
│       ├── GreenBond_GDELT_clean.ipynb      # GDELT data collection & V2Tone extraction
│       └── GreenBond_ClimateBERT_clean.ipynb # ClimateBERT sentiment scoring
│
└── output/
    ├── regression/                  # All figures used in Chapter 5
    │   ├── plot1_greenium_timeseries.png
    │   ├── plot2_coefficients.png
    │   ├── plot3_sentiment_scatter.png
    │   ├── plot4_noise_quartiles.png
    │   ├── event_study_india.png
    │   ├── event_study_indonesia.png
    │   ├── event_study_pooled.png
    │   └── event_study_comparison.png
    ├── gdelt/                       # GDELT raw output files
    └── html/                        # Interactive HTML visualisations

    
```

---

## Data Sources

| Variable | Source | Frequency |
|---|---|---|
| Sovereign green bond yields | Refinitiv Eikon | Daily |
| Conventional twin bond yields | Refinitiv Eikon | Daily |
| Climate media sentiment (V2Tone) | GDELT Project | Daily |
| ClimateBERT sentiment scores | GDELT + ClimateBERT (Hugging Face) | Daily |
| VIX (volatility index) | FRED | Daily |
| Exchange rates (USD/INR, USD/IDR) | Refinitiv Eikon | Daily |
| Sovereign CDS spreads | Investing.com | Daily |

**Coverage:** January 2020 – December 2024  
**Countries:** India, Indonesia  
**Note:** Thailand was excluded after no tradeable sovereign green bonds with verifiable secondary-market yield data could be identified on Refinitiv.

---

## Empirical Design

### Twin-Bond Framework
Each sovereign green bond is paired with a **maturity-matched conventional bond** from the same issuer. The Greenium is computed as the daily yield spread between the two (Green Yield − Conventional Yield). For India, two pre-2023 conventional bonds were used to ensure sufficient pre-treatment observations.

### Treatment Events
| Country | Event | Date |
|---|---|---|
| India | Inaugural sovereign green bond auction | January 2023 |
| Indonesia | JETP announcement at G20 Bali Summit | November 2022 |

### Identification Strategy
- **Staggered DiD** with country and time fixed effects
- **Event study** with ±8 weekly leads and lags to test pre-trends and dynamic effects
- **First-differenced** specification as robustness check (Durbin-Watson improved from 0.44 to 2.54)
- **ClimateBERT** as an alternative sentiment measure (54 climate-relevant daily paragraphs identified)

### Key Variables
| Variable | Description |
|---|---|
| `Greenium` | Daily yield spread (Green − Conventional), in basis points |
| `V2Tone` | GDELT average daily climate media sentiment score |
| `Signaling Noise` | Within-day standard deviation of V2Tone (proxy for credibility gap) |
| `Δlog(VIX)` | Log-differenced CBOE VIX |
| `ΔCDS` | First-differenced sovereign CDS spread |
| `ΔFX` | First-differenced log exchange rate |

---

## Notebooks

### Databricks / VSCode (Production)
| Notebook | Description |
|---|---|
| `GreenBond_Regression.ipynb` | Main DiD panel regressions, fixed effects, robustness checks, coefficient plots |
| `GreenBond_EventStudy.ipynb` | Event study leads/lags, parallel trends tests, country-level and pooled plots |

### Google Colab (NLP)
| Notebook | Description |
|---|---|
| `GreenBond_GDELT_clean.ipynb` | GDELT API queries, V2Tone extraction, Signaling Noise construction |
| `GreenBond_ClimateBERT_clean.ipynb` | ClimateBERT inference on GDELT text, V2Tone correlation analysis |

---

## Environment

### Requirements

- Python 3.10+
- See [`requirements.txt`](requirements.txt) for full dependencies

### Cloud Environments Used

| Environment | Runtime | Used For |
|---|---|---|
| Google Colab | GPU (T4) | NLP notebooks — GDELT extraction, ClimateBERT inference |
| Databricks Community Edition | Apache Spark | Regression notebooks — DiD panel, event study |

### Local Reproduction

```bash
pip install -r requirements.txt
```

Key packages:

| Package | Version | Purpose |
|---|---|---|
| `pandas`, `numpy` | ≥1.5, ≥1.23 | Data manipulation and panel construction |
| `statsmodels` | ≥0.13 | OLS regression, DiD, Durbin-Watson, VIF |
| `transformers`, `torch` | ≥4.30, ≥2.0 | ClimateBERT sentiment classification |
| `requests` | ≥2.28 | GDELT DOC API queries |
| `matplotlib` | ≥3.6 | All thesis figures |
| `openpyxl` | ≥3.0 | Excel I/O for raw bond data |
| `tqdm` | ≥4.64 | Progress bars for NLP inference |

> **Note:** The ClimateBERT model (`climatebert/distilroberta-base-climate-sentiment`) is downloaded automatically via Hugging Face `transformers` on first run. A GPU runtime is strongly recommended for the ClimateBERT notebook.

---

## How to Reproduce

1. **Sentiment data:** Run `GreenBond_GDELT_clean.ipynb` and `GreenBond_ClimateBERT_clean.ipynb` on Google Colab to regenerate processed GDELT files.
2. **Panel construction:** Bond yield and control variable data were sourced from Refinitiv, FRED, and Investing.com. Place raw files under `data/raw/` following the existing folder structure.
3. **Regressions:** Run `GreenBond_Regression.ipynb` on Databricks (or a local PySpark/pandas environment) to reproduce all regression tables and coefficient plots.
4. **Event study:** Run `GreenBond_EventStudy.ipynb` to reproduce all event study figures.

All outputs are saved to `output/`.

---

## Thesis Chapters

| Chapter | Status | Description |
|---|---|---|
| 1 — Introduction | Complete | Research question, Credibility Premium/Gap framework, case selection |
| 2 — Literature Review | Complete | Green bond pricing literature, political sentiment, emerging market finance |
| 3 — Data | Complete | Bond data, GDELT, ClimateBERT, control variables |
| 4 — Methodology | Complete | Twin-Bond design, staggered DiD, event study, identification strategy |
| 5 — Results | Complete | Regression results, event study, robustness checks |
| 6 — Discussion | In progress | Interpretation of null results, policy implications |
| 7 — Limitations | Complete | Liquidity constraints, GDELT noise, data coverage |

---

## Contact

**Nahian Ibnat**  
MA in Economics, Data & Policy  
Central European University

## Feedback & Questions

Scan the QR code below to share your thoughts or ask questions about this thesis:

![Feedback Form QR Code](feedback_qr.png)

Or click here: [Open Feedback Form](https://forms.gle/YMKYULpfnAX5dyV4A)
