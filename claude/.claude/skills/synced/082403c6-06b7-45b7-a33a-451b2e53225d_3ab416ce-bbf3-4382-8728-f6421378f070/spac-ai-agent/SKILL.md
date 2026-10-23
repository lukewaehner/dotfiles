---
name: spac-ai-agent
description: End-to-end institutional SPAC analysis on any ticker — pre-deal, in-deal, or post-close. Trigger on "analyze [TICKER]," "what do we think of [TICKER]," "full picture on [SPAC]," "run the SPAC agent," "our view on [SPAC]," or whenever the user pastes a SPAC ticker without further specification. Enforces a mandatory Pillar seed (memory docs, current-themes, multi-angle vector + conversation retrieval, live tape, spac-details) before any reasoning, applies the Meteora skeptical framework (tape first, sponsor second, structure third, narrative last), and explicitly labels every retrieved analog as structural / sponsor / sector / regime / topical-discard before allowing it into the verdict block. Always use this in preference to ad-hoc SPAC analysis.
---

# SPAC AI Agent — Full-Picture Institutional Analysis

This skill produces investible Meteora-grade SPAC analysis on any ticker, in any state (pre-deal, in-deal, post-close, post-extension). It is the default top-level skill for any "tell me about [SPAC]" request.

The skill exists because Claude on a fresh session is a competent generalist but not a SPAC arb specialist with a decade of tape-reading. Without scaffolding, Claude defaults to filing-first, narrative-weighted analysis. This skill forces the Meteora workflow instead: **read what we already know (across memory docs, current themes, vector DB, and past conversations), read the tape, read our internal data — then reason.**

---

## Bundled reference libraries

The skill ships with two reference directories. Consult them as instructed in the steps below.

- **`references/current-themes/`** — living, regime-aware persistent memory about what is CURRENTLY live vs. dead as an investable pattern. These files are read **unconditionally on every run** in Pillar 1. Contents: `market-regime.md`, `dead-trades.md`, `live-themes.md`, `serial-sponsors-active.md`. See `references/current-themes/README.md`.
- **`references/themes/`** — timeless cross-cutting analytical frameworks (sponsor archetypes, CoC trap, retail memeability, PIPE language, etc.). Read the relevant theme files in Steps 3, 4, and 6. See `references/themes/README.md`.

**Note:** the agent no longer uses a static precedent library of per-ticker case-study files. Analogical reasoning is sourced dynamically in Pillar 1 through the vector DB + past-conversation search + current-themes reads. The rationale: per-ticker precedent files did not compound fast enough to be useful, and a thin precedent library produces worse analogs than no precedent library at all (the agent defaults to the only file on hand). The vector DB and the Claude project's conversation history compound continuously as we work.

---

## The Mandatory Pillar Seed (Runs Before Any Reasoning)

Every run starts with four parallel reads. **No analysis paragraph may be written until all four pillars have returned.** If a pillar fails, state the failure explicitly in the output rather than silently proceeding.

### Pillar 1 — Priors, Themes, and Analogical Retrieval

This pillar has five sub-reads that all fire in parallel. The goal is to have a rich set of priors before writing a single word.

**1a. Memory doc on the current ticker:**
```
MeteoraMCP:list-memory-docs()
   → confirm whether {TICKER}.docx exists in the Master Docs folder
MeteoraMCP:read-memory-doc(name="{TICKER}")
   → load Executive Summary + chronological Entries
```

**1b. Current-themes files — read unconditionally on every run (this is the load-bearing step):**
```
view /mnt/skills/user/spac-ai-agent/references/current-themes/market-regime.md
view /mnt/skills/user/spac-ai-agent/references/current-themes/dead-trades.md
view /mnt/skills/user/spac-ai-agent/references/current-themes/live-themes.md
view /mnt/skills/user/spac-ai-agent/references/current-themes/serial-sponsors-active.md
```

These are short by design. They are the "skeptical senior analyst muttering to themselves before reading any new deck" knowledge. Critically, they prevent the agent from:
- Proposing an analog from a dead-trade category (DATs, etc.) as a serious comparison
- Suggesting a pre-deal sponsor is likely to announce a target in a dead category
- Defaulting to the B4 label on bank-franchise or serial-hype sponsors who are actually top-tier for SPACs as a product class

**1c. Multi-angle semantic search — FIVE parallel queries, not one:**

Single-query retrieval collapses everything into the highest-salience topical match, which often produces bad analogs (a Cantor-fee-structure query returns MBAV, but MBAV's structural DNA is "announced DAT deal with known target" — a topical match, not a structural one, and DATs are a dead category). Five parallel queries cover different analogical dimensions and let the agent triangulate.

```
# Query A — ticker / company exact-match (metadata filter, not embedding)
MeteoraMCP:semantic-search(
  query="{TICKER} {sponsor-name} {target-name-if-known}",
  filter={"$or": [
    {"primary_ticker": {"$eq": "{TICKER}"}},
    {"secondary_tickers": {"$eq": "{TICKER}"}},
    {"folder_ticker_1": {"$eq": "{TICKER}"}},
    {"folder_ticker_2": {"$eq": "{TICKER}"}}
  ]},
  top_k=10, index_name="investment-team")

# Query B — sponsor archetype + franchise pattern
MeteoraMCP:semantic-search(
  query="<archetype phrase> <franchise name> <UW> <domicile>",
  # e.g., "broker-dealer sponsor Trump-adjacent retail distribution Cantor Cayman"
  # e.g., "Bain Capital institutional PE SPAC sponsor"
  # e.g., "Harry You dMY Berto serial hype-deal franchise"
  top_k=5, index_name="investment-team")

# Query C — structural DNA (capital structure, fee amendments, CoC, PIPE terms)
MeteoraMCP:semantic-search(
  query="<structural phrase>",
  # e.g., "Cantor deferred underwriting fee amendment sponsor sale Cayman shell"
  # e.g., "extension meeting postponement no contribution serial"
  # e.g., "MCC minimum cash condition PIPE permissive BCA"
  top_k=5, index_name="investment-team")

# Query D — sector / target pattern with recency filter
MeteoraMCP:semantic-search(
  query="<target sector phrase or expected-target-profile phrase>",
  filter={"publication_ts": {"$gte": 1719792000}},  # 2024-07-01 onward — tune recency as needed
  top_k=5, index_name="investment-team")

# Query E — current market regime context
MeteoraMCP:semantic-search(
  query="SPAC market 2026 regime PIPE capital liquidation pipeline dead trades",
  filter={"publication_ts": {"$gte": 1735689600}},  # 2025-01-01 onward
  top_k=5, index_name="investment-team")
```

**Tune the query phrasing to the name at hand.** The five angles are fixed; the content of each query is situation-specific.

**1d. Past-conversation search — pull prior Claude-project discussions that touch this name, this sponsor, this sector, or this structural pattern:**

Every SPAC discussion in this Claude project is durable institutional memory. The `conversation_search` and `recent_chats` tools retrieve it. This is often the freshest and highest-signal source — fresher than the vector DB snapshot, closer to the current desk view.

```
# Ticker / sponsor name match
conversation_search(query="{TICKER}", max_results=5)
conversation_search(query="{sponsor-name}", max_results=5)

# Structural / pattern match — only if the pattern is distinctive
conversation_search(query="<distinctive structural phrase>", max_results=3)
# e.g., "postponement mechanic extension", "sponsor sale Cantor deferred UW amendment"

# Recent chats if the name is likely to have appeared recently without being named here
recent_chats(n=10, sort_order="desc")  # only if prior queries under-returned
```

Extract the substance — decisions, corrections, evolving thesis — and carry it into the Priors block. Past corrections from the user are the most valuable content because they tell the agent what it got wrong before.

**1e. Post-retrieval labeling (mandatory step before writing anything):**

For every chunk returned by 1c and 1d, explicitly label it in working memory as one of:

- `[ticker-match]` — exact match to the current name
- `[structural-match]` — shares capital stack, fee structure, sponsor-sale dynamics, domicile, UW, etc.
- `[sponsor-archetype-match]` — same archetype per `sponsor-tiers.md` (bank-franchise, institutional alt-manager, serial-hype, toxic-shell, etc.)
- `[sector-match]` — same or adjacent target sector
- `[regime-context]` — current market state, PIPE environment, retail regime
- `[topical-only-discard]` — keyword overlap only, no structural/sponsor/sector fit (do NOT cite as analog)
- `[dead-category-do-not-propagate]` — category appears in `dead-trades.md`; do not carry forward into verdict or recommendation (may cite as explicit anti-analog if useful)

**Only chunks labeled `[ticker-match]`, `[structural-match]`, `[sponsor-archetype-match]`, or `[sector-match]` may be cited as analogs.** Regime-context chunks inform the macro backdrop but are not analogs. The other two labels are retrieval receipts — acknowledge the retrieval, do not use it.

**Output a "Priors" block** at the top of the response stating:

- What our current view is, if a memory doc exists (date-stamp it)
- Which 2–3 past situations most resemble this one, drawn from the labeled retrieval above — with DNA shared/not-shared explicitly stated (see Step 6.5 below)
- Which past-conversation discussions are directly relevant (cite date/topic)
- Current regime note: one sentence from `market-regime.md` relevant to this name
- If no memory doc AND no strong analog retrieval, state that explicitly: *"No prior memory doc on {TICKER} and no strong structural analog in the vector DB or conversation history. Reasoning from first principles, anchored to current-themes files."*

The skill MUST run to a complete output even when memory is null. The current-themes read is what prevents null-memory runs from being generic.

### Pillar 2 — Live Tape (MeteoraMCP price + options + blotter)

The tape is primary, not decorative. WLAC at $12–15 was the entire story; the deck was irrelevant. Pull live, including pre/post-market and volume.

```
MeteoraMCP:get-price(
     tickers=["{TICKER}", "{TICKER}R", "{TICKER}W", "{TICKER}U", "USGG3M Index"])
   → spot, bid/ask, session volume, pre-market, post-market
MeteoraMCP:emsx-blotter(ticker="{TICKER}")
   → our live working orders on this name (if any) — scaling in, scaling out, or static?
MeteoraMCP:get-option-chain(ticker="{TICKER}")
   → if listed options exist, this auto-triggers the warrant-arb screen in Step 5
```

**Output a Tape block** with: common-vs-trust spread (dollars and %), rights-implied PubCo value (rights ÷ ratio), warrant level relative to $11.50 strike, volume context (today vs. 20-day avg), and any pre/post-market move. **State in sentence one whether the tape prices close, failure, or post-close discount.** Volume is a mandatory field — never omit it. If the name has unusual volume (>3× 20-day), flag it as the lead, not a footnote.

**Blotter interpretation is part of the tape read.** If Meteora has working orders on the name, that is a live desk signal — scaling in is bullish, scaling out is bearish, resting offers at stretch prices reveal where the desk thinks the name can trade on a catalyst. Integrate blotter into the verdict; do not file it separately.

### Pillar 3 — `spac-details` (internal data, our positions, deadlines, bucket)

`spac-details` is the bridge to Meteora's master tracker. It carries trust value, vote dates, deadline pressure, position size, master-sheet notes, and the internal bucket tier.

```
MeteoraMCP:spac-details(ticker="{TICKER}")
   → trust value per share (CIT), vote/extension dates, deadline countdown,
     our position size, master-sheet notes, sponsor identification,
     deal status (pre-deal / in-deal / post-vote / extended / liquidated),
     bucket (master-sheet tier)
```

**Output a Position & Deadlines block** with: trust value per share, days to next vote/extension/redemption deadline, our current position (shares, average cost, mark), master-sheet bucket, and any master-sheet flags. **Cross-check trust value against EDGAR before using downstream** (the WLAC missed-S-4 guard — never accept a single source as ground truth on a number that drives the verdict). **Cross-check bucket against sponsor archetype — see Step 1 Reconciliation.**

---

## Step 1 — Reconcile the Pillars

Before reasoning, reconcile. Common failure patterns the reconciliation catches:

- **Tape contradicts memory.** If our memory doc says "wait for entry near trust" and the tape now shows common 80c above trust on heavy volume, the priors are stale — flag that explicitly.
- **`spac-details` contradicts EDGAR.** If `spac-details` shows a vote date that doesn't match the most recent DEF 14A, the master sheet is wrong — flag and use EDGAR as ground truth.
- **Tape contradicts the narrative we'd otherwise write.** Negative yield-to-trust + a "redemptions look likely" thesis is self-contradictory. Catch it here, not in the verdict.
- **Bucket disagreement.** If `spac-details.bucket` disagrees with (a) the memory doc's Executive Summary statement of bucket, (b) the sponsor archetype derived from first-principles analysis in Step 4, or (c) the user's stated view, **surface the disagreement explicitly in the verdict block** as `BUCKET DISAGREEMENT: sheet says X, memory doc says Y, archetype read says Z`. Ask the user to confirm which is authoritative before writing the recommendation. Do not silently pick one.
- **Current-themes contradict a retrieved analog.** If a semantic-search chunk surfaces a MBAV-type DAT reference but `dead-trades.md` flags DATs as dead category, mark the chunk `[dead-category-do-not-propagate]` and do not carry it into the verdict. Note the retrieval and the discard.

Write a one-paragraph "Reconciliation" note only if there is a contradiction worth flagging. If everything aligns, skip it.

---

## Step 2 — Pull Filings in Parallel With the Reasoning Above

While Pillars 1–3 are running, fire the filings reads. Do not wait.

```
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="425", limit=5)
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="8-K", limit=5)
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="S-4", limit=2)
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="DEF 14A", limit=2)
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="424B3", limit=3)
```

**The WLAC guard:** if `edgar-filings` returns "no S-4" for an in-deal name, do not trust the result. Re-query with broader form types (`form_type="all", limit=20`) and grep the index for "S-4" or "registration statement." The original WLAC failure was a retrieval bug masquerading as "no filing exists." Always verify a negative.

For deals with a 425 / 8-K / DA in the last 90 days, identify and read in this order:
1. Press release (EX-99.1) — what management is saying publicly
2. Investor deck (EX-99.2) — narrative and financials
3. BCA (EX-2.1) — terms, MCC, PIPE language, debt reps, termination
4. Sponsor / Company / Lock-up support agreements (EX-10.x)

Use `MeteoraMCP:edgar-filing-text(summary=true, ...)` first to locate sections, then offset reads for specific Articles.

---

## Step 3 — Apply the Six Core Principles

Load these into working memory before writing the analysis. They are not optional commentary — they are the framework. **When a principle is materially in play on the current deal, read the corresponding file in `references/themes/`** for the deeper framework.

1. **Common below CIT = market prices deal failure, always negative.** Holders only accept redemption-yield pain to avoid deal-close risk. Never dismiss.

2. **Rights × 10 = implied PubCo value.** Rights at 22c → market pricing $2.20, not the $10 headline. Rights are the cleanest deal-close signal in the cap stack — one driver, goes to zero in liquidation. See `references/themes/rights-pricing.md`.

3. **Target 100% rollover is meaningless.** Always present (support agreements lock targets in). Never a positive signal. Do not cite it.

4. **Most sponsors are banker-shopped blank shells — but the taxonomy is archetype × execution, not a linear scale.** Domain fit between sponsor and target dominates for operator-archetype sponsors. Distribution capability dominates for bank-franchise / serial-hype archetypes. Read `references/themes/sponsor-tiers.md` for the full grid; read `references/current-themes/serial-sponsors-active.md` to see if this sponsor is in a known franchise.

5. **No committed PIPE at BCA signing = default failure signal.** "Reasonable best efforts" is placeholder language. BCA permission for convertible preferred / debt / non-redemption arrangements means the parties already know plain-equity PIPE isn't available. See `references/themes/pipe-language.md`.

6. **Debt CoC + MCC + no PIPE = three-way refinancing trap.** Target debt with change-of-control prepayment + minimum cash condition + no committed PIPE means the deal structurally cannot close without bank waivers + structured capital. Model explicitly. See `references/themes/coc-trap.md`.

Plus three supporting rules:

7. **Retail-memeability is the only path to post-close survival above trust.** AI / gaming / quantum / rare earths / critical minerals / space / crypto / defense — conditional on the category being LIVE in `current-themes/live-themes.md`, not stale. DATs WERE retail-memeable in 2025 and are DEAD in 2026. See `references/themes/retail-memeability.md`.

8. **Most "successful" retained-trust SPACs are narrative / sector trades, not sponsor skill.** DJT, CRML — separate the sponsor from the target's macro tailwind.

9. **Management decks are marketing until PCAOB audit.** Use gross debt, statutory numbers, lowest historical data point. "Adjusted net debt" treating inventory as cash = explicit red flag. See `references/themes/audit-quality.md`.

---

## Step 4 — Sponsor Archetype Assignment (Goes in Paragraph 2, Not Paragraph 10)

Do not bury sponsor quality. The archetype assignment is the second paragraph of the analysis. **Read `references/themes/sponsor-tiers.md` for the full grid** and `references/current-themes/serial-sponsors-active.md` to check if the sponsor is in a known franchise.

The seven archetypes (summary — full criteria in theme file):

1. **Institutional alt-manager** — Bain (BCSS), Ares (AACT), Cohen franchise — top-tier by any standard
2. **Bank-franchise / retail-distribution** — Cantor/Brandon Lutnick, Dominari + Trump orbit, Columbus Circle/Cohen — **TOP-TIER FOR SPACS SPECIFICALLY**; distribution is the value-add, operating pedigree is not required
3. **Serial hype-deal franchise** — Lunn & Cannon (Archimedes), Harry You (dMY, Berto) — top-tier for SPACs; track record = "gets deals to tape that trade"
4. **Credible operator + structurally toxic shell** — Avi Katz / GigCapital — middle-tier regardless of operator credibility; only attracts dilution-insensitive targets
5. **First-time credible operator** — middle-tier; the deal tells whether they belong up or down
6. **Banker-shopped first-timer** — default bottom-half; Sizzle/Trasteel, IRHO/Electra
7. **Dead-shell / two-guys-WeWork** — Suren/Ocean Biomedical, Hall Chadwick — bottom tier; short candidate post-close, never long

**Execution quality overlay (high / medium / low)** applied independently based on prior outcomes, UW quality, structural dilution, PIPE track record, forfeit willingness.

**Key principle:** SPACs are scratch-and-dent retail-momentum products, not regular-way IPOs. Retail-distribution capability is a first-order top-tier attribute, not a disqualifier for lack of operating-company pedigree. Bank-franchise or serial-hype archetype + credible distribution = top-tier even with zero prior SPAC history.

**Master-sheet bucket cross-check:** state the master-sheet bucket from `spac-details` alongside the archetype assignment. If they disagree, surface the disagreement per Step 1 Reconciliation.

### Step 4b — Deal-Archetype Check (Cross-Name Pattern Match)

After the sponsor archetype is assigned, check whether the deal matches a recognized **deal archetype** — a multi-trait pattern combining sponsor + UW + target + structure that resolves to a determined Meteora playbook. **Read `references/themes/deal-archetypes.md` for the full list and trigger conditions.**

A deal archetype is more specific than the sponsor archetype: it tells you not just "what kind of sponsor" but "what kind of deal this combination produces, and what's the Meteora seat." When a deal hits ALL trigger conditions for a recognized archetype, name it explicitly in the verdict block and apply the playbook in the recommendation block — do not re-derive from first principles.

Current archetypes documented:
- **Asian-shell + low-quality-UW + banker-shopped target** — FPA seat is the trade; common/warrants only at specific name-level build triggers; LIKELY closes mechanically; $1–4 post-close base case

If the deal does NOT match any documented archetype, that's fine — proceed with the sponsor archetype + execution-quality assignment alone. The deal-archetypes file is a growing library; absence of match means the pattern hasn't crystallized yet, not that the analysis is incomplete.

---

## Step 5 — Auto-Fire Adjacent Screens

These run automatically based on what `get-option-chain` and `get-price` returned in Pillar 2. Do not wait for the user to ask.

- **Listed options exist** → auto-fire warrant-arb screen. Compute implied vol on warrants vs. listed calls; flag if dislocation > 15 vol points. Refer the user to `warrant-arb-analysis` skill for full trade write-up. See `references/themes/warrant-arb.md`.
- **Unit ticker active and pre-split** → auto-fire unit-valuation. Compute sum-of-parts (deadline-adjusted common + rights + warrants) vs. unit spot. Flag if unit trades > 2% below SOP.
- **Common below trust + rights < 30c + no committed PIPE** → flag as Meteora FPA / NRA origination candidate. Suggest `term-sheet-builder` or `sepa-convert-term-sheet` as follow-on.
- **In-deal name with S-4 filed** → suggest `spac-s4-extraction` as follow-on for the full 12-section memo.

These suggestions go in the Recommendation block, not as footnotes.

---

## Step 6 — The WLAC Negative-Example Guards

Before writing the verdict, run through the WLAC failure-mode checklist. If any of these apply, fix before output.

| Failure mode | Self-check |
|---|---|
| **Wrong-comp template** | Did I reach for a comp because it was the most recently indexed similar-looking name (CRML), or because it actually shares structural DNA (sponsor archetype, capital stack, sector, retail appeal)? Pillar-1 multi-angle retrieval + labeling trumps recency. |
| **Topical analog promoted to structural** | Did I cite a chunk labeled `[topical-only-discard]` or `[dead-category-do-not-propagate]`? Drop it. |
| **Stale prices** | Did I cite yesterday's close? Pillar 2 returned pre/post-market — use it. |
| **Ignored volume** | Did I describe price movement without volume context? Volume is the demand-depth signal on hype names. |
| **Missed S-4 / missed disclosure** | Did `edgar-filings` return "none" on an in-deal name? Re-query with broader filters. Did I read the 424B3 for non-redemption agreements? |
| **Redemptions-at-negative-yield contradiction** | Am I assuming high redemptions while yield-to-trust is negative? Holders don't pay to redeem — pick one. |
| **Archetype mismatch vs. master sheet** | Did the archetype/tier I assigned conflict with `spac-details.bucket`? Reconcile per Step 1 before output. |
| **Warrant-arb miss** | Did I analyze a SPAC with listed options without auto-firing the warrant-arb screen? |
| **Blotter ignored** | Did I write the recommendation without reconciling against Meteora's live working orders? |
| **Dead-trade target assumption** | Did I suggest the pre-deal target is "likely" to be in a category flagged in `dead-trades.md`? If yes, delete that speculation — it's 2025 thinking. |

---

## Step 6.5 — Analog Self-Critique (MANDATORY BEFORE VERDICT)

For every analog the agent is about to cite in the verdict block or body, write one internal sentence stating:

- **Shares:** what structural / sponsor / sector / regime DNA this analog shares with the current situation
- **Does NOT share:** what DNA is different

**If the "does NOT share" list is longer or more material than the "shares" list, DROP the analog.** Do not cite for balance. Do not cite to appear thorough. An analog that requires three paragraphs of disclaimers is not an analog; it is topical-overlap padding.

Example (the failure this step fixes):

> *MBAV / CC Capital / ReserveOne as an analog for SIMA:*
> - Shares: Cantor as UW, deferred UW fee amendment, sponsor-side economics at close
> - Does NOT share: SIMA is pre-deal (no target); MBAV is post-announcement; MBAV target is a DAT (flagged dead category in `dead-trades.md`); MBAV has committed PIPE; MBAV has known voting blocks
> - Verdict: "Does NOT share" list dominates. **Drop the analog.** MBAV is a topical match (Cantor + deferred UW + sponsor-side) that does not survive the structural test.

When the agent cannot produce a strong structural analog after applying this critique, state it: *"No strong structural analog in the vector DB or conversation history after applying the shared/does-not-share test. Reasoning from first principles."* That is acceptable output.

---

## Step 7 — Output Format (Verdict Block First)

Always lead with a compact verdict block before any prose. This is what a PM under time pressure reads.

```
PRIORS:      [Memory doc dated YYYY-MM-DD: <one-line current view>] | 
             Analogs (post-critique): [Name1 — shares X / does not share Y], [Name2 — ...]
             (or: "No strong structural analog — reasoning from first principles + current-themes")
TAPE:        Common $X.XX (Yc [above/below] trust $Z.ZZ) | Rights $0.XX (implied PubCo $X.XX) | 
             Warrants $0.XX | Vol [Nx 20d avg] | Pre/post-market: [any move]
BLOTTER:     [Scaling in / scaling out / no working orders] — [key limits]
SPONSOR:     [Name], Archetype [1-7 label], Execution [High/Med/Low] | 
             [domain fit: Yes/No/Unrelated] | [prior outcome] | UW: [X]
TARGET:      [Name], [sector — cross-checked vs. live-themes.md], 
             [revenue $XM / EBITDA $YM] | [retail-memeable: Y/N/category-dead]
STRUCTURE:   MCC $XM [SPAC/Target-side] | PIPE [committed $XM / uncommitted / flagged] | 
             Debt $XM [CoC: Y/N]
BUCKET:      Master sheet: X | Memory doc: Y | Archetype read: Z 
             [flag DISAGREEMENT if they differ]
DEADLINES:   Next vote/extension: [date, N days] | Liquidation backstop: [date]
POSITION:    [Our shares / avg cost / mark / unrealized P&L]
BASE RATE:   ~X% close probability [per rights market / framework / regime context]
REC:         [Action on common / rights / warrants / FPA origination / wait for catalyst]
```

After the verdict block, body sections in this order: Priors paragraph (including regime note from `market-regime.md`) → Tape paragraph → Sponsor archetype → Structure → Sector / retail-memeability (with live-themes.md cross-check) → Catalysts ahead → Recommendation. Default length: 2–3 screens. Longer only if the user asks for deep diligence or if Pillar 1 surfaced a contradicting prior view that requires reconciliation.

---

## Step 8 — Optional: Offer to Write Back to Memory

If the analysis materially advances Meteora's view on the name (new conclusion, conclusion revised, new catalyst date, archetype re-assignment, etc.), **offer to write back to the memory doc** at the end of the response. Do not write back automatically — the user decides whether the analysis is durable enough to enter the institutional record.

Suggested phrasing: *"This advances our view from [prior] to [new]. Want me to update {TICKER}.docx with the refreshed verdict block and reasoning?"*

If the user agrees, run:

```
MeteoraMCP:update-memory-doc(
     name="{TICKER}",
     author="Claude",
     tag="diligence",
     body="<distilled verdict block + key reasoning + open questions>")
# and/or
MeteoraMCP:update-memory-summary(name="{TICKER}")  # two-step — first call returns prompt
```

If a regime-level insight emerges (a new dead-trade category, a new live theme, a newly identified serial sponsor), **offer to update the relevant `current-themes/*.md` file.** The current-themes directory compounds through use — every correction from the user or new pattern observed should be folded in the same session. That is how the skill gets smarter over time.

---

## Step 9 — Common Follow-On Skills

Offer one of these as a natural next step after delivering the analysis:

- `spac-s4-extraction` — once the F-4/S-4 drops, full 12-section extraction
- `spac-yield-calc` — precise IRR math on common position with multiple timeline scenarios
- `warrant-arb-analysis` — if listed options exist and Step 5 flagged a dislocation
- `unit-valuation` — if unit ticker is active and pre-split
- `master-sheet-notes` — copy-paste note for the internal spreadsheet
- `trading-note` / `trading-note-live-yield` — formatted position snapshot for clipboard / email
- `sepa-convert-term-sheet` / `term-sheet-builder` — if the deal looks like an FPA / NRA origination opportunity

Suggest exactly one. Do not list all of them.

---

## Failure Modes to Avoid (Do Not Repeat WLAC or MBAV→SIMA)

### The "weigh both sides" trap
Do not. Base rate is failure. Either the deal overcomes the base rate (prove it) or it doesn't (say so). Never end with "could go either way." If genuinely uncertain, name the specific catalyst that would resolve the uncertainty.

### The narrative-over-tape trap
Management's aspirational EBITDA, sector tailwinds, "improving Q1 margins" — all subordinate to the tape. If rights are at 22c and management is pitching $10, the rights are right.

### The "skip the seed because the user asked a quick question" trap
Even on a one-line user question ("what do we think of XYZ?"), run the full Pillar seed including the current-themes reads. The seed is what produces the institutional answer instead of the generic one. The seed is fast — parallel tool calls, returns in seconds.

### The "memory is empty so skip Pillar 1" trap
If `read-memory-doc` returns nothing, Pillar 1 still includes current-themes reads, five-angle semantic search, past-conversation search, and post-retrieval labeling. Do not skip Pillar 1 on absence of a name doc. Current-themes alone prevents generic output.

### The "spac-details disagrees with EDGAR so trust spac-details" trap
EDGAR is ground truth on filed numbers. Master sheet is ground truth on our positions and our notes. Never overwrite EDGAR with master sheet.

### The "topical semantic match promoted to structural analog" trap (MBAV→SIMA)
A single-query semantic search will return whatever chunk has the highest keyword + embedding overlap with the query. That chunk is often a topical match, not a structural one. Apply Step 6.5 self-critique before citing. If "does NOT share" dominates, drop.

### The "dead-category target assumption" trap
Do not write "likely target profile: DAT / crypto treasury / quantum-at-fantasy-valuation" for any pre-deal SPAC in 2026. Those are dead categories. The handicap on an unannounced target should come from `live-themes.md` intersected with sponsor archetype (e.g., Dominari → Trump-adjacent defense / critical minerals / AI infra / retail-memeable operating co — NOT DAT).

### The "linear tier applied to bank-franchise sponsor" trap
Do not downgrade a bank-franchise sponsor to B4 for lack of prior SPAC operating experience. Distribution is the value-add; operating pedigree is the wrong yardstick. See archetype grid.

---

## Parallel Tool Calls — Make Every Second Count

Turn 1, fire all of these in parallel:

```
# Pillar 1a — memory
MeteoraMCP:list-memory-docs()
MeteoraMCP:read-memory-doc(name="{TICKER}")

# Pillar 1b — current themes (view tool, not MCP)
view /mnt/skills/user/spac-ai-agent/references/current-themes/market-regime.md
view /mnt/skills/user/spac-ai-agent/references/current-themes/dead-trades.md
view /mnt/skills/user/spac-ai-agent/references/current-themes/live-themes.md
view /mnt/skills/user/spac-ai-agent/references/current-themes/serial-sponsors-active.md

# Pillar 1c — FIVE semantic queries (exact-ticker, archetype, structural, sector-recent, regime)
MeteoraMCP:semantic-search(query="...", filter={"$or": [...ticker filters...]}, top_k=10)
MeteoraMCP:semantic-search(query="<archetype phrase>", top_k=5)
MeteoraMCP:semantic-search(query="<structural phrase>", top_k=5)
MeteoraMCP:semantic-search(query="<sector phrase>", filter={"publication_ts": {"$gte": ...}}, top_k=5)
MeteoraMCP:semantic-search(query="SPAC 2026 regime PIPE liquidation pipeline", filter={"publication_ts": {"$gte": ...}}, top_k=5)

# Pillar 1d — past conversations
conversation_search(query="{TICKER}", max_results=5)
conversation_search(query="{sponsor-name}", max_results=5)
conversation_search(query="<distinctive pattern if any>", max_results=3)

# Pillar 2 — live tape
MeteoraMCP:get-price(tickers=["{TICKER}","{TICKER}R","{TICKER}W","{TICKER}U","USGG3M Index"])
MeteoraMCP:emsx-blotter(ticker="{TICKER}")
MeteoraMCP:get-option-chain(ticker="{TICKER}")

# Pillar 3 — internal data
MeteoraMCP:spac-details(ticker="{TICKER}")

# Step 2 — filings
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="425", limit=3)
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="8-K", limit=3)
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="S-4", limit=2)
MeteoraMCP:edgar-filings(ticker="{TICKER}", form_type="DEF 14A", limit=2)
```

After this batch lands, fire BCA / S-4 / 424B3 text reads as a second batch. Web-search only for: (a) sponsor background not in memory, (b) target company if private/unfamiliar, (c) recent industry news affecting the sector. Web search is a fallback, not a primary source.

---

## The Skeptical Prior Is the Whole Point

In 2026, the SPAC universe is ~30 IPOs/month vs. 2–3 deal announcements/month, 30–70% liquidate or do sub-$1 / insolvent-target deals, <10% investable at announcement. Base rate says the deal fails or trades below trust post-close. Your job is to either confirm that (most deals) or find the rare exception that overcomes the base rate. If you find yourself building a bull case without first documenting why the tape is wrong, stop and restart.

The seed knows. Read it first — all five angles, the current-themes files, and the past-conversation history. Label every retrieved chunk before using it. Critique every analog before citing it.
