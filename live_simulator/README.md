# 📊 The Greenium Live Simulator

**A real-time streaming model of sovereign green bond pricing under the market development threshold interpretation.**

> Ibnat, N. (2026). *When Governments Say 'Green' — Do Bond Markets Believe Them?*
> MA Thesis, Department of Economics, Central European University — Private University, Vienna.

▶️ **[Open the Live Simulator](https://nahianibnat-2000.github.io/Thesis/live_simulator/greenium_live_simulator.html)**

---

## 🎬 New here? Watch the animated explainer first

Before jumping into the controls, watch the short animated explainer — it walks through the whole argument visually, with the greenium line drawing itself, reacting to a VIX shock, and crossing the depth threshold:

▶️ **[Open the Animated Explainer](https://nahianibnat-2000.github.io/Thesis/live_simulator/greenium_explainer.html)**

It autoplays start to finish like a video, but you can pause, scrub the timeline, or jump between scenes. In about a minute it covers:
- What the greenium is and how to read the colour-coded line
- Why, in a **thin market**, a credibility event doesn't move the price
- Why **global risk appetite (VIX)** is the one thing that does
- What crossing the **depth threshold** changes — and why the same signal then reprices
- Where the greenium *is* real: the Germany / Denmark benchmark

> The simulator itself has a built-in guided walkthrough too — click the **?** button (bottom-right) any time to replay it.

---

## 🌍 What is this?

Unlike the [game](../Play%20it/), the simulator **runs automatically and continuously** — it streams a live greenium series in real time while you manipulate market conditions using sliders and buttons. There is no win or lose. It is a model you can interrogate.

The simulator encodes the central empirical finding: in thin emerging markets, credibility signals cannot reach daily bond prices. Only global risk appetite (VIX) can. Cross the market development threshold and the market structure changes entirely.

---

## 🖥️ What You're Looking At

### Top strip — five status boxes

| Box | What it shows |
|-----|---------------|
| **Greenium** | The live yield spread between the green bond and its conventional twin, in basis points |
| **30-day mean** | Rolling average greenium — more stable than the live number |
| **Market regime** | 🔴 **THIN · MACRO-DOMINATED** or 🟢 **MATURE · MANDATE-ANCHORED** — the most important box |
| **VIX** | Global fear index. Calm / Jittery / Risk-off panic |
| **Day** | Trading days elapsed since the simulation started |

### Main chart — the greenium line

The line **changes color by zone** — no need to read the y-axis:

| Color | Meaning |
|-------|---------|
| 🔴 **Red / Pink** | Greenium > 0 bp — investors demand extra yield, no belief |
| 🟡 **Amber** | Between 0 and −2 bp — a premium is forming but unstable |
| 🟢 **Mint green** | ≤ −2 bp — stable trust, Germany/Denmark grade |
| 🔵 **Blue dashed vertical** | A credibility event you fired |

### Lower chart — VIX

Global fear over time. When VIX spikes up, watch the greenium chart — in a thin market it reacts almost immediately. That is the thesis finding: fear is priced, promises are not.

### Event feed — bottom right

After you fire a credibility event, it waits 20 trading days then reports back:
- 🔴 *"Not distinguishable from noise (p ≈ 0.6)"* — below the threshold, your event had no effect
- 🟢 *"Repriced — mandate-driven investors received the signal"* — above the threshold, it worked

---

## 🎛️ Controls

### Three sliders

| Slider | What it does | Key number |
|--------|-------------|------------|
| **Market depth** | Size of the institutional investor base | **Cross 60** to flip the regime |
| **Credibility stock** | Accumulated green policy signals | Only matters above the threshold |
| **Base VIX** | Global fear level | Higher = more compression in thin markets |

### Two shock buttons

| Button | What it does |
|--------|-------------|
| **⚡ Fire credibility event** | Simulates a discrete political event (auction, pledge, framework). Adds +8 credibility. Runs a 20-day event study and reports the verdict in the feed. |
| **📉 VIX shock** | Injects a sudden spike in global fear. Watch what it does to the greenium in thin vs mature markets. |

### Speed and pause

- **1× / 2× / 4× / 8×** — fast-forward the simulation
- **⏸ PAUSE / ▶ PLAY** — freeze to read the feed carefully

---

## 🧪 The Core Experiment (60 seconds)

This sequence demonstrates the entire thesis argument interactively:

**Step 1** — Leave depth at 25. Hit **⚡ Fire credibility event**. Wait for the event feed verdict after ~20 days. It will report something like *"not distinguishable from noise, p ≈ 0.6"* — mirroring the India/Indonesia result.

**Step 2** — Drag **Market depth** past 60. Watch the regime pill flip from red to green. The greenium line stabilises and shifts downward.

**Step 3** — Hit **⚡ Fire credibility event** again. The feed now reports a real repricing. The same signal, the same market, but now with a receiver.

**Step 4 (optional)** — Hit **📉 VIX shock** in both regimes. In the thin market it moves the price visibly. In the mature market it barely registers. That is the VIX dominance result: 0.35–0.48 bp per standard deviation in Asia, not significant in Europe.

---

## 📖 What the Numbers Are Calibrated To

| Simulator behaviour | Real thesis result |
|---|---|
| Thin market mean greenium ≈ +0.5 bp | India sample mean: +0.50 bp |
| Thin market volatility σ ≈ 4 bp | Indonesia sample σ: 4.12 bp |
| VIX moves price ~0.35–0.48 bp per SD | Thesis: β ≈ −0.0035 to −0.0048 pp per SD of log VIX, significant across specifications |
| Event study verdict p ≈ 0.5–0.9 | M5 pooled Post: p ≈ 0.59; Stack A: p ≈ 0.40 |
| Mature market stable at ~−2.8 bp | Denmark mean: −2.80 bp; Germany: −1.82 bp |
| Mature market σ ≈ 1 bp | Denmark σ ≈ 2.0 bp |

> The exact regression figures live in the [thesis](../Nahian_Ibnat_2026_MA_Thesis.pdf) and [notebooks](../notebooks/) — the simulator is calibrated *to the spirit* of those estimates, not a structural re-estimation of them.

---

## 🔄 How to Reset

Just **refresh the page** (F5 or Cmd+R). Everything resets — day counter, greenium series, event feed, and all sliders.

---

## ⚠️ Disclaimer

This simulator is a stylized model of **one interpretation** of the thesis results — the market development threshold argument. The threshold mechanism is consistent with the empirical evidence but is not directly identified in the research design. The two-country Asian sample (India and Indonesia) cannot rule out alternative explanations including differences in investor composition, political salience of green commitments, or measurement limitations in the GDELT V2Tone proxy.

The model parameters are calibrated to the thesis estimates but the simulator is not a structural model — it is a pedagogical tool.

---

## 📂 Also in this repository

- 🎮 **[The Greenium Game](https://nahianibnat-2000.github.io/Thesis/Play%20it/greenium_game.html)** — a 20-quarter policy simulation where you can win or lose
- 🎬 **[Animated Explainer](https://nahianibnat-2000.github.io/Thesis/live_simulator/greenium_explainer.html)** — the one-minute visual walkthrough of the core argument
- 📄 **[Full Thesis](../Nahian_Ibnat_2026_MA_Thesis.pdf)** — the complete empirical paper with all regression tables
- 💻 **[Replication notebooks](../notebooks/)** — all Python code for the DiD regressions and event studies

---

*Built as a public outreach companion to an MA thesis. No prior knowledge of bond markets or econometrics required.*
