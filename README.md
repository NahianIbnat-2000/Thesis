# When Governments Say "Green" — Do Bond Markets Believe Them?

### Political Credibility Signals and the Sovereign Green Bond Greenium in Emerging Markets

**Nahian Ibnat**
MA in Economics, Data & Policy — Central European University
Supervisor: Zoltán Csaba Tóth | 2026

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

- **VIX is the only robust driver** of daily greenium movements in Asia. The coefficient of roughly **−0.0035 to −0.0048 percentage points** translates to about **0.35–0.48 basis points** per unit change in VIX — an economically modest but statistically robust effect, pointing to global risk appetite rather than domestic climate politics as the pricing anchor.
- **European robustness check** recovers persistent greeniums of approximately **−1.82 bp (Germany)** and **−2.80 bp (Denmark)**, consistent with the established developed-market green bond literature and indicating the Asian null is not a methodological artifact.

> **Interpretation note:** "Null" here means *precise* nulls — tightly estimated coefficients near zero, not merely statistically insignificant noisy estimates. The distinction matters for how much the result should update priors about the emerging-market greenium.

---

## Empirical Design

### Twin-Bond Framework

Each sovereign green bond is paired with a single **maturity-matched (10Y) conventional twin** from the same issuer. The greenium is the daily yield spread (Green − Conventional), in basis points. One strict twin pair is used per country:

| Country | Green bond (ISIN) | Conventional twin (ISIN) |
| --- | --- | --- |
| India | IN0020220144 | IN0020190362 |
| Indonesia | US71567RAV87 | US455780DN36 |
| Germany | DE0001030708 | DE0001102507 |
| Denmark | DK0009924375 | DK0009924102 |

### Stacked DiD and Treatment Events

The design stacks two treatment cohorts and estimates a pooled DiD with cohort-specific event windows:

| Stack | Country | Event | Date |
| --- | --- | --- | --- |
| A | Indonesia | JETP announcement (G20 Bali Summit) | November 2022 |
| B | India | 2nd sovereign green bond auction | October 2023 |

> **Why the 2nd auction for India, not the inaugural?** India's inaugural green bond auction (January 2023) leaves effectively no pre-treatment trading history for the green leg. The October 2023 second auction provides roughly **120 trading days of pre-treatment variation**, which is required for credible parallel-trends testing.

### Identification and Inference

- **Five model specifications (M1–M5)**, building from a baseline greenium regression to fully controlled stacked DiD.
- **HC3 heteroskedasticity-robust** and **panel-corrected (PCSE)** standard errors.
- **Event study** with leads and lags to test pre-trends and dynamic effects.
- **European benchmark** (Germany, Denmark) as out-of-sample robustness on the same twin-bond logic.

### Key Variables

| Variable | Description |
| --- | --- |
| `greenium` | Daily yield spread (Green − Conventional), in basis points |
| `tone` (V2Tone) | GDELT average daily climate-news tone |
| `signalling_noise` | Within-day standard deviation of V2Tone (credibility-gap proxy) |
| `dlog_vix` | Log-differenced CBOE VIX |
| `dcds` | First-differenced sovereign CDS spread |
| `dfx` | First-differenced log exchange rate |

> **Note on ClimateBERT:** ClimateBERT was evaluated as an alternative tone measure but **dropped from the main analysis**. Applied to GDELT output it scored theme codes rather than natural-language sentences, producing degenerate results. GDELT V2Tone is the primary and reported tone proxy.

---

## Data Sources

| Variable | Source | Frequency |
| --- | --- | --- |
| Sovereign green & conventional bond yields | Refinitiv / LSEG Workspace | Daily |
| Climate-news tone (V2Tone) | GDELT Project (BigQuery) | Daily |
| VIX (volatility index) | FRED | Daily |
| Exchange rates (USD/INR, USD/IDR) | Refinitiv / LSEG Workspace | Daily |
| Sovereign CDS spreads | Investing.com | Daily |

**Countries:** India, Indonesia (core); Germany, Denmark (robustness).
**Note:** Thailand was excluded — no tradeable sovereign green bond with verifiable secondary-market yield data could be identified.

---

## Repository Structure

> Confirm the tree below against the live repo before publishing — the chapter sources and notebook subfolders may have been reorganised since this README was last regenerated.

```
Thesis/
├── data/
│   ├── raw/                         # Bond yields, VIX, FX, CDS (sourced; not all redistributable)
│   └── processed/                   # GDELT tone panel + analysis-ready regression panel
├── notebooks/                       # Regression, event study, GDELT/tone pipelines
├── output/                          # Figures and tables used in Chapters 4–5
├── presentation/                    # Thesis defence slides
├── AI_Declaration_Nahian_Ibnat.pdf
├── requirements.txt
└── thesis_latex.zip                 # LaTeX source of the written thesis
```

---

## Environment

- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`

| Package | Purpose |
| --- | --- |
| `pandas`, `numpy` | Panel construction and data manipulation |
| `statsmodels` / `linearmodels` | DiD, panel regression, HC3/PCSE standard errors |
| `matplotlib` | Thesis figures |
| `requests` / BigQuery client | GDELT V2Tone extraction |
| `openpyxl` | Excel I/O for raw bond data |

Notebooks were developed across VS Code, Kaggle, and Google Colab; bond data was accessed via Refinitiv (LSEG Workspace) through CEU.

---

## How to Reproduce

1. **Tone data:** Run the GDELT notebook to regenerate the daily V2Tone climate-news panel from BigQuery.
2. **Panel construction:** Place raw bond/VIX/FX/CDS files under `data/raw/` following the existing structure, then build the merged regression panel.
3. **Regressions:** Run the regression notebook to reproduce M1–M5, robustness checks, and coefficient plots.
4. **Event study:** Run the event study notebook to reproduce leads/lags figures and parallel-trends diagnostics.
5. **European benchmark:** Run the European comparison notebook to reproduce the Germany/Denmark greenium estimates.

All outputs are written to `output/`.

---

## Contact

**Nahian Ibnat**
MA in Economics, Data & Policy — Central European University
