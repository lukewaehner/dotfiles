---
name: spac-deal-review
description: Skeptical expert-grade review of SPAC business combination announcements (BCA / 8-K / DA / investor deck). Use this skill whenever the user asks to review, analyze, evaluate, or form a view on a newly announced SPAC deal, or pastes a BCA / 8-K / investor deck, or references a ticker in the context of a merger announcement. Also trigger on phrases like 'deep dive on [SPAC deal]', 'what do you think of the deal', 'is this a good deal', 'analyze [SPAC] / [Target]', 'SPAC merger analysis', 'review this BCA', or any version of 'should we be long / short / FPA / sell the rights / sell the warrants'. This skill enforces the Meteora skeptical framework — tape first, sponsor second, structure third, narrative last — and is the default for any SPAC-announcement question. Do NOT attempt SPAC deal analysis without this skill; ad-hoc analysis without the framework produces superficial output that misses the market's pricing signal and over-weights management narrative.
---

# SPAC Deal Review — Skeptical Framework

Review a SPAC business combination announcement the way a 20-year SPAC arb analyst would: **the tape prices the deal; the filings and deck either confirm or refute the tape.** Not the other way around.

This skill exists because the default LLM reasoning mode on a SPAC deal is to weigh both sides and extract narrative from the investor deck. **That produces wrong answers on 2026 SPAC deals.** In a market where 30–70% of SPACs liquidate and <10% are investable, the correct baseline is: **this deal fails unless proven otherwise**. This skill forces that discipline.

---

## Core Principles (Load These Into Working Memory Before Writing Anything)

Read and internalize before touching the BCA:

1. **Common below CIT = market prices deal failure, always negative.** Never dismiss. Holders are willing to take redemption yield pain to avoid deal-close risk — that only happens when the market sees a non-trivial probability the SPAC insiders trap redemption, extend, or the post-close shares trade well below trust.

2. **Rights × 10 = implied PubCo value.** Rights at 22c → market pricing $2.20 per PubCo share, not the $10 headline. Rights are the single cleanest deal-close signal in the cap stack because they have exactly one value driver (does the deal close?) and go to zero in a liquidation. A right under 30c on a deal trading near trust means the market either (a) thinks the deal doesn't close, or (b) thinks the deal closes but PubCo trades at $2–3. Both are bearish.

3. **Target 100% rollover is meaningless.** It is always true — target shareholders are always locked in via support agreements. It is never a positive signal. Do not cite it.

4. **Most sponsors are blank shells that take banker-shopped deals.** One prior successful SPAC is not evidence of operating skill. Evaluate domain fit between sponsor and target: if the sponsor is a restaurateur / footwear CEO / real estate developer and the target is a European steel trader / rare earth miner / quantum computing company, it is banker-shopped. The exceptions are billionaire-backed sponsors, the Daniel/Betsy Cohen franchise, and institutional PE/HF sponsors with demonstrated deal sourcing.

5. **No committed PIPE at BCA signing = default failure signal.** "Reasonable best efforts" covenants with no named investors and no subscription agreements are placeholder language. The BCA's permission for convertible preferred, convertible debt, or non-redemption arrangements is the parties acknowledging upfront that plain-equity PIPE is not available.

6. **Debt CoC + MCC + no PIPE = three-way refinancing trap.** If target debt has change-of-control triggers requiring prepayment, AND there's a minimum cash condition, AND no committed PIPE, the deal structurally cannot close without bank waivers + structured capital. Model this explicitly.

7. **Retail-memeability is the only path to post-close survival above trust.** AI, gaming, quantum, rare earths, critical minerals, space, crypto, defense. If the target is not in one of these sectors, post-close shares will almost certainly trade below trust regardless of fundamentals. "Quality business at fair price" does not survive post-close SPAC tape in 2026.

8. **Most "successful" retained-trust SPACs are narrative trades, not fundamental value.** DJT / Trump Media: $1M revenue at billions. CRML: macro-driven rare earth rerate, not operating execution. Do not treat CRML-style post-close pops as evidence of sponsor skill — separate the sponsor from the target's sector tailwind.

9. **Management decks are marketing until PCAOB audit.** Any EBITDA, margin, or "adjusted" metric on a first-time-audit target is fiction. Use gross debt, statutory numbers, and the lowest historical data point when stress-testing. "Adjusted net debt" that treats inventory as cash-equivalent is an explicit red flag signaling the unadjusted story doesn't support the valuation.

---

## Step 1 — Pull the Tape (Before Anything Else)

This is non-negotiable. The first tool call in any SPAC deal review is `MeteoraMCP:spac-details` and `MeteoraMCP:get-price` — in parallel — for all traded securities (common, warrants, rights, units).

```
MeteoraMCP:spac-details(ticker="<SPAC_TICKER>")
MeteoraMCP:get-price(tickers=["<SPAC>", "<SPAC>R", "<SPAC>W", "<SPAC>U", "USGG3M Index"])
```

Extract and tabulate:

| Security | Spot | Reference Value | Market Signal |
|---|---|---|---|
| Common | $X.XX | CIT $Y.YY | [above/below trust by Zc] |
| Rights | $0.XX | Intrinsic at trust = CIT × right ratio | Implied PubCo value = rights ÷ ratio |
| Warrants (if any) | $X.XX | Strike typically $11.50 | Time value / break probability |
| Units (pre-split) | $X.XX | Common + derivative value | Arb to components |

**Compute immediately:**
- Common-vs-trust spread (positive or negative, in dollars and %)
- Rights-implied PubCo value (rights price ÷ rights ratio, e.g., 22c / 0.10 = $2.20)
- Implied close probability if you assume PubCo trades at trust: (rights price × ratio ÷ CIT) × adjustment-for-time-value

**State upfront — in the first sentence of the response — whether the tape prices close or failure.** If common is below trust or rights are under 30c or warrants are under 10c on a recent-announce deal, the tape is pricing failure or post-close discount. Say so explicitly.

---

## Step 2 — Pull the Filings in Parallel

Use parallel tool calls. While `spac-details` runs, also fire:

```
MeteoraMCP:edgar-filings(ticker="<SPAC>", form_type="425", limit=5)
MeteoraMCP:edgar-filings(ticker="<SPAC>", form_type="8-K", limit=5)
```

From the 8-K / 425 filings index, identify:
- The BCA itself (EX-2.1 — the Business Combination Agreement)
- The investor deck (EX-99.2 typically)
- The press release (EX-99.1)
- Sponsor Support Agreement (EX-10.1)
- Company Support Agreement (EX-10.3)
- Lock-up Agreement form (EX-10.2)

Read in order: press release → deck summary sections → BCA termination, MCC, PIPE, debt reps, interim covenants.

For BCA reading, use `MeteoraMCP:edgar-filing-text` with `summary=true` first to locate sections, then offset-based reading for specific Articles. The key sections to read verbatim on every deal:

| Article / Section | Why it matters |
|---|---|
| §6.7 Financial Statements | Audit status, debt reps, projections quality |
| §6.7(c) Indebtedness | **Check if prepayment restrictions / CoC carved out on Schedule** — any carve-out = smoking gun for CoC risk |
| §8.2 Interim Covenants — Conduct of Target | Can target increase leverage / prepay? Debt moves pre-close |
| §8.16 Use of Trust Proceeds | "Including repayment of existing Indebtedness" = deal proceeds refinancing debt, not funding growth |
| §8.17 PIPE Financing | "Reasonable best efforts" = uncommitted; check sponsor forfeiture language |
| §9.1–9.3 Closing Conditions | **Critical: is MCC on the SPAC side or the Target side?** If Target-side, Target can waive and force close |
| §10.1 Termination | Outside date, audit delivery deadline, MAE termination right, breakup fee |

---

## Step 3 — Run the Sponsor Bucket Rubric

This goes in the second paragraph of the response — not the 10th. Do not bury sponsor quality.

### Bucket framework

| Bucket | Criteria | Examples |
|---|---|---|
| B1–2 | Billionaire-backed, Daniel/Betsy Cohen franchise, institutional PE/HF with successful prior SPACs (multiple deals, not lucky one-offs), Citi/Cantor/Goldman lead UW | Ajax Capital, Churchill, Social Capital |
| B3 | Credible management with capital markets or public company experience, half-warrant units, BTIG/Citigroup UW | Typical "decent first-time" sponsors |
| B3.5 | Standard half-warrant units with credible (even thin) management | Competent but unproven |
| B4 | First-time sponsor, UW-shopped, no domain fit with target, 1/4 rights or smaller | Most of the 2021–2025 retail SPAC cohort |
| B4.5 | Zero domain fit (restaurant sponsor buying steel, footwear CEO buying commodities), one prior banker-shopped deal, thin operating team | Sizzle II / Trasteel |
| B5 | Zero relevant experience, 1/5-right structures, Maxim/D. Boral/AGP underwritten, WeWork-office two-person teams, first-time with no track record or with prior SPAC failures | Avoid |

### Domain fit is the dominant factor

A restaurant sponsor buying a steel trader is B4.5 regardless of whether their first SPAC "succeeded." A successful prior SPAC that was itself a banker-shopped deal in a different sector is not evidence of sponsor skill — it's evidence the banker relationship produces deal flow.

### The CRML template trap

If the sponsor's one prior successful SPAC was a CRML-style macro/narrative win (rare earths, critical minerals, quantum, space, crypto, defense during a geopolitical or thematic tailwind), do NOT treat this as operating skill. CRML's success was Greenland + Trump + DOD stockpile + rare earth macro — not Steve Salis (restaurateur) executing on critical minerals. Separate the sponsor from the target's sector tailwind.

### Underwriter signal

- Cantor: heavy 2025–2026 SPAC volume, mixed deal quality, known to cross-sell PF European targets
- Citi/Cohen/BTIG: higher-quality deal flow on average
- Maxim / D. Boral / AGP: structural negative — exploding-unit and distressed-candidate bias
- Clear Street / I-Bankers: generally weaker deal flow

Note the underwriter in the sponsor assessment and treat it as a secondary signal confirming the bucket.

---

## Step 4 — Compute Sources & Uses at Multiple Redemption Scenarios

Do not trust the deck's "0% redemption" case. Model 0%, 50%, 80%, and 100% redemptions:

```
Trust starting balance from spac-details: $XXX M
Per-share trust value: $Y.YY
Shares outstanding subject to redemption: N M

Scenario A: 0% redemption → Trust cash = $XXX M
Scenario B: 50% redemption → Trust cash = $XXX × 0.5 = $YYY M
Scenario C: 80% redemption → Trust cash = $XXX × 0.2 = $YYY M
Scenario D: 100% redemption → Trust cash = $0

Uses in each scenario:
- Transaction expenses (legal, banker, deferred UW): ~$15–30M (lookup in 10-K deferred UW balance)
- Debt refinancing per §8.16 implied S&U: $X M
- Working capital / growth: residual
```

For each scenario, compute:
- Net cash to post-close balance sheet
- Pro forma share count (starting SPAC public + rollover + sponsor + rights conversion − redemptions)
- Pro forma gross debt (target debt + any assumed bridge)
- PF EV/EBITDA (using gross debt, not "adjusted")

**The MCC test:** at what redemption % does trust cash + committed PIPE fall below the MCC? If MCC can't be satisfied above 50% redemptions without PIPE, and PIPE is uncommitted, the deal needs structured capital.

---

## Step 5 — Debt and CoC Analysis

This is the single most common place where SPAC deals die in 2026. Do not skip it.

### Check §6.7(c) rep language

A clean rep says "no debt contains restrictions on prepayment or CoC triggers." A rep that says "except as set forth on Schedule 6.7(c)" is carving out CoC risk. **The carve-out itself is the signal.** You don't need to see Schedule 6.7(c) to know CoC triggers exist — the rep structure tells you.

### Check §8.16 Use of Proceeds

Language like "working capital and general corporate purposes, including repayment of the existing Indebtedness of the Target Companies" confirms the parties expect deal proceeds to service existing debt. This is a refinancing SPAC, not a growth SPAC. Model accordingly.

### Compute implied debt refinance in S&U

If the deck's sources & uses shows a large "debt paydown" line (or if post-close net debt is materially lower than pre-close gross debt), that delta is the implied bank waiver / CoC prepayment cost. Common ranges:
- Deals where banks demand 100% prepayment: 100% of acquisition debt tranche refinanced
- Deals where banks accept consent for fee + partial paydown: 20–40% of tranche
- Deals where banks consent with no paydown: rare, only for investment-grade targets

### Gross vs "adjusted" net debt discipline

Always use statutory gross debt for underwriting. If management's "adjusted net debt" deducts inventory as cash-equivalent, note this as an adjustment not accepted by lenders or public comps. The proper underwriting basis:

```
Gross debt (all financial liabilities, current + non-current + sub loans)
− Cash and equivalents
= Net debt
```

No inventory adjustment. No security deposit deduction. Klöckner and Worthington Steel report statutory; there is no reason to let the SPAC target use a different framework.

### Debt service sustainability

On the lowest historical EBITDA year (not peak, not recent), compute interest coverage and leverage:
```
Lowest 3-yr EBITDA / assumed blended rate × gross debt = interest coverage
Gross debt / lowest 3-yr EBITDA = trough leverage
```

If trough leverage is above 5x or trough coverage is below 1.5x, the business is structurally distressed regardless of recent recovery. Rating agency downgrades (Moody's/S&P/Fitch/Creditreform) corroborate this.

---

## Step 6 — PIPE Assessment

### Committed vs uncommitted

- **Committed PIPE at signing, named investors, subscription agreements filed:** Positive signal. Rare in 2026. Size the PIPE discount to $10 for dilution impact.
- **"Reasonable best efforts" language, no named investors, flexibility for convertible/preferred/non-redemption:** Default failure signal. The parties acknowledge plain-equity PIPE is not available.
- **Explicit sponsor no-forfeit clause (sponsor will not give up founder shares to attract PIPE):** Major red flag. Means PIPE investors can only be compensated through target dilution, which target rollover holders will resist.

### Realistic structured PIPE terms for a distressed target

If PIPE happens, expect:
- 15–30% discount to $10 (effective price $7–$8.50)
- Liquidation preference senior to public shareholders
- Anti-dilution / ratchet provisions
- Board rights
- Covenants on post-close business

Each of these dilutes the $10 narrative. Compute PIPE-adjusted post-close ownership.

### When PIPE fails and alternative capital is needed

If the deal needs $50–100M of structured capital and conventional PIPE won't get done, the menu is:
- **FPA / NRA (Non-Redemption Agreement)** — Meteora's primary paper
- **ELOC (Equity Line of Credit)** — B Riley, Yorkville, similar
- **Convertible pre-paid advance** — for distressed situations
- **Bridge debt with convert kicker** — already contemplated in most BCAs

Flag this explicitly as a Meteora origination opportunity. Most deals with common below trust + rights < 30c + no PIPE are exactly where Meteora's FPA/structured paper wins.

---

## Step 7 — Retail Memeability Filter

This determines whether post-close shares can trade above trust. Score the target:

**Retail-friendly sectors (post-close can trade $8–$20+):**
- AI / machine learning / applied AI
- Gaming / esports / gambling
- Quantum computing
- Rare earths / critical minerals (especially with geopolitical angle)
- Space / satellite / defense tech
- Crypto / blockchain / stablecoin infrastructure
- Electric aviation / eVTOL
- Nuclear / SMR / fusion
- Defense (drone, hypersonics, counter-UAS)

**Neutral sectors (post-close typically $3–8):**
- Consumer tech with differentiation
- Climate / clean energy (commodity biofuel, not story-specific)
- Adjacent-tech (fintech, healthtech without clear narrative)

**Negative sectors (post-close almost certainly below trust):**
- Steel trading / metals distribution
- European industrial / manufacturing
- Commodity trading houses (absent geopolitical story)
- Restaurants / hospitality
- Traditional services / staffing
- Generic real estate
- Apparel / retail

A target in the negative list is a hard constraint — the deal closing at $10 is irrelevant because the shares will not hold $10 post-close. Public investors lose.

---

## Step 8 — Output Format (Verdict Block First)

Always lead with a compact verdict block before any prose:

```
TAPE:       Common $X.XX (Yc [above/below] trust $Z.ZZ) | Rights $0.XX (implied PubCo $X.XX)
SPONSOR:    [Name], Bucket X.X | [domain fit: Yes/No/Unrelated] | [prior deal outcome] | UW: [X]
TARGET:     [Name], [sector], [revenue $XM / EBITDA $YM] | [retail-memeable: Y/N]
STRUCTURE:  MCC $XM [SPAC/Target-side] | PIPE [committed $XM / uncommitted] | Bridge $XM | Debt $XM [CoC flagged: Y/N]
BASE RATE:  ~X% close probability [per rights market / framework]
REC:        [Action on common / rights / warrants / FPA origination]
```

Everything after this is supporting detail — sized by how much the user actually needs to see. Default length: 2–3 screens for a standard deal review, longer only if the user asks for deep diligence.

---

## Step 9 — Avoid These Failure Modes

### The "weigh both sides" trap
Do not. The base rate is failure. Either the deal overcomes the base rate (prove it) or it doesn't (say so directly). Do not end with "it could go either way."

### The narrative-over-tape trap
Management's aspirational EBITDA, sector tailwinds, "improving Q1 margins" — all of these are subordinate to what the market is pricing. If rights are at 22c and management is pitching $10, the rights are right. Cite the tape first, narrative second.

### The "sponsor did one deal" trap
One prior deal ≠ skill. Evaluate whether that prior deal succeeded on macro/sector tailwind or on sponsor execution. Almost always, SPAC successes are target-side or macro-side, not sponsor-side. Separate them.

### The "100% rollover" positive-signal trap
It's always present. It's never a positive. Do not cite it as validation.

### The first-time-PCAOB EBITDA trap
Swiss GAAP, IFRS-only unaudited, management accounts — all are pre-audit marketing. Use the lowest historical EBITDA year when stress-testing. Assume at least one material reclassification or write-down will surface in PCAOB conversion.

### The "adjusted net debt" trap
If management's slide 14-type debt page reduces gross debt by treating inventory as cash or deducting security deposits, note this explicitly as non-standard and recompute using statutory net debt.

### The "PIPE could be structured" trap
"Could be" is not "is." Uncommitted PIPE with convertible-preferred flexibility is a placeholder, not financing. Size the dilution to the target rollover if structured PIPE actually executes.

---

## Step 10 — Position Recommendation

Conclude with concrete action. A good SPAC deal review ends with a paragraph the user can act on:

- **Common at spread to trust:** Hold / add / sell based on yield vs. close risk. Most Bucket 1–2 deals trading below trust are attractive redemption-yield plays.
- **Rights:** Sell below 30c into rising market; hold if >50% implied close probability; sell entire position if sponsor is Bucket 4.5+ and audit/PIPE gates are ahead.
- **Warrants:** Generally sell; post-close deSPAC trades $3–7 in 2026, making $11.50 strike warrants structurally near-worthless absent retail-memeable target with strong PIPE.
- **FPA origination:** For deals with common below trust + rights <30c + no PIPE, proactively flag as Meteora FPA/NRA origination opportunity. Suggest approaching sponsor with structured paper terms (spread to trust, reset on breakage, reset on trust interest).

Do not end with "more analysis needed" or "let's see what the F-4 says." Commit to a position given the information available. If the deal is a clear fail, say so. If it's a clear investable deal, say so. If it's truly uncertain, define the specific catalyst that would change the view (PCAOB audit delivery, PIPE announcement, bank waiver disclosure).

---

## Parallel Tool Calls — Make Every Second Count

SPAC deal reviews are tool-heavy. Fire these in parallel on turn 1:

```
MeteoraMCP:spac-details(ticker="<SPAC>")
MeteoraMCP:get-price(tickers=["<SPAC>", "<SPAC>R", "<SPAC>W", "<SPAC>U", "USGG3M Index"])
MeteoraMCP:edgar-filings(ticker="<SPAC>", form_type="425", limit=3)
MeteoraMCP:edgar-filings(ticker="<SPAC>", form_type="8-K", limit=3)
```

While that data lands, read the relevant memory items (SPAC principles #14, skeptical prior #15, CRML template #16, workflow #17, bucket rubric #18).

After tape + filings land, fire BCA text reads:

```
MeteoraMCP:edgar-filing-text(summary=true, url="<BCA_URL>")
```

Then target specific sections via offset / section parameter.

Web-search only for: (a) sponsor background if not already in memory, (b) target company if private / unfamiliar, (c) recent industry news affecting the sector.

---

## Common Follow-On Skills

After this review, the natural next skills are:

- `spac-s4-extraction` — once the F-4/S-4 drops, full 12-section extraction
- `spac-yield-calc` — precise IRR math on common position
- `master-sheet-notes` — copy-paste note for internal spreadsheet
- `sepa-convert-term-sheet` / `term-sheet-builder` — if the deal is an FPA origination opportunity
- `warrant-analysis` — if warrants are a tradeable instrument in this deal

Offer the user one of these as a follow-up after delivering the initial review.

---

## Reminder: The Skeptical Prior Is the Whole Point

In 2026, the SPAC universe is:
- ~30 IPOs/month vs. 2–3 deal announcements/month
- 30–70% expected to liquidate or do sub-$1 / insolvent-target deals
- <10% investable at announcement

The base rate says the deal fails or trades below trust post-close. Your job is to either confirm that (most deals) or find the rare exception that overcomes the base rate. If you find yourself building a bull case without first documenting why the tape is wrong, stop and restart.

The tape knows. Read it first.
