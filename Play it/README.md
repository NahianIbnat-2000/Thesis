# 🎮 The Greenium Game

**Can you make bond markets believe your green promises?**

A playable simulation of the key finding from:
> Ibnat, N. (2026). *When Governments Say 'Green' — Do Bond Markets Believe Them?*
> MA Thesis, Department of Economics, Central European University — Private University, Vienna.

▶️ **[Play it live here](https://nahianibnat-2000.github.io/Thesis/Play%20it/greenium_game.html?v=2)**

---

## 🌍 What is this game about?

You are the Finance Minister of an emerging market economy. Your government has just issued a sovereign green bond. If bond markets believe your green promises, investors will accept a lower yield — a **negative greenium** — cutting your borrowing costs.

Your challenge: get the greenium to **−2.0 basis points or better** (the level Germany and Denmark earn) and **hold it there for 4 consecutive quarters**.

The game is built around the real empirical finding: in India and Indonesia (2022–2024), no credibility event moved the greenium. Only global risk appetite (VIX) did. Can you figure out why — and what to do about it?

---

## 🎯 How to Win

Hold the greenium at **−2.0 bp or lower for 4 quarters in a row** within 20 quarters total.

---

## 🕹️ How to Play

### Starting the game
- Click **"OPEN THE MARKET"** on the intro screen to begin
- You start with a greenium of **+0.5 bp** — investors don't yet believe you (India's real starting value)

### Each quarter
1. **Spend your 2 action points** on policy cards from the Policy Desk
2. **Click "SETTLE THE QUARTER →"** to let the market price your bond and move forward

### The two types of cards

| Type | Color | What it does |
|------|-------|--------------|
| **Credibility signals** | Green label | Raises your credibility score (auctions, pledges, frameworks) |
| **Market infrastructure** | Navy label | Raises your market depth score (mandates, market-makers, index inclusion) |

### Reading the dashboard
- **Greenium** — your bond's yield spread. 🔴 Positive = no belief. 🟡 Amber = forming. 🟢 ≤ −2 bp = win zone
- **Market depth** — the size of your institutional investor base. Watch the bar — the **gold threshold line is at 60**
- **Credibility** — your accumulated policy signals
- **VIX** — global fear index. When it spikes, your greenium gets compressed regardless of what you announce
- **Win streak** — consecutive quarters at −2 bp or better. You need 4 in a row

---

## 💡 Strategy Tips

### The trap most players fall into
Spending all action points on **green signal cards** (pledges, auctions, frameworks) while ignoring infrastructure. Your credibility events will generate real-world headlines — and the market ledger will tell you the p-value is ~0.6. The market won't blink.

This is the thesis finding made playable.

### The winning approach

**Early game (Q1–Q8): build the receiver first**
Spend both action points every quarter on navy infrastructure cards:
- "Mandate pension & insurer ESG allocations" (+12 depth)
- "Fund a market-making program" (+10 depth)
- "Run index-inclusion roadshow" (+8 depth, +3 credibility)

Get to **depth 60** as fast as possible. Until then, nothing else matters.

**Mid game (Q8–Q14): now use the signals**
Once you see the gold **"Threshold crossed"** message in the ledger, switch to credibility cards:
- Use the international pledge first (+12 credibility) — it's one-time only
- Then framework (+8) and auctions (+6)

**Late game (Q14–Q20): protect the streak**
Keep stacking credibility to push the greenium deeper negative. A greenium of −3 or −4 bp gives you a buffer against random VIX spikes. You need 4 consecutive quarters at or below −2 bp to win.

---

## 📖 The Real-World Connection

| Game mechanic | Real-world equivalent |
|---|---|
| Depth threshold at 60 | Minimum institutional investor base needed for credibility pricing |
| VIX dominating below threshold | India/Indonesia result: β = −0.45 bp per SD, p < 0.05 across all specs |
| Signals doing nothing below threshold | Post-event DiD coefficients: p = 0.59 (pooled), p = 0.40 (Stack A) |
| Stable greenium above threshold | Germany: −1.82 bp · Denmark: −2.80 bp (Ando et al., 2023) |
| Infrastructure cards | Pension mandates, market-making programs, ESG index inclusion |

---

## ⚠️ Disclaimer

This is a stylized model of **one interpretation** of the thesis results — the market development threshold argument. The threshold mechanism is consistent with the evidence but is not directly identified in the empirical design. The two-country Asian sample cannot rule out alternative explanations including differences in investor composition, political salience, or measurement limitations in the GDELT proxy.

---

## 📂 Also in this repository

- 📊 **[Live Simulator](https://nahianibnat-2000.github.io/Thesis/live_simulator/greenium_live_simulator.html)** — stream the greenium in real time, fire credibility events, inject VIX shocks
- 📄 **[Full Thesis](../Nahian_Ibnat_2026_MA_Thesis.pdf)** — the complete empirical paper
- 💻 **[Replication notebooks](../notebooks/)** — all Python code for the DiD regressions and event studies

---

*Built with ❤️ as a public outreach companion to an MA thesis. No prior knowledge of bond markets required.*
