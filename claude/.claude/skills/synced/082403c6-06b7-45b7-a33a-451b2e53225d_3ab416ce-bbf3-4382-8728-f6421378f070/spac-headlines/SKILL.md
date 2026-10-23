---
name: spac-headlines
description: "Cross-reference SPAC morning headlines against Meteora's internal book using spac-details and EDGAR filings. Trigger when the user pastes chat transcripts, headline blasts, or news with multiple SPAC tickers and asks to 'compare against our book', 'check these against our positions', 'analyze the morning notes', or 'cross-reference the headlines'. Processes ALL tickers: enriches with positions, trust data, deadlines, pulls filings for in-deal names, flags upcoming votes and deadlines."
---

# SPAC Headlines Analysis — Cross-Reference Against Internal Book

## Overview

This skill takes raw morning chat notes / headline blasts containing SPAC news and produces a single enriched bullet per ticker, suitable for copy-pasting directly into Bloomberg chat.

**Input:** Pasted text block (morning chat, Bloomberg IB messages, headline summaries) containing SPAC-related news items.

**Output:** Plain text, one multi-line block per ticker, combining the headline news with our internal position data, full trust context (CIT, trust balance, IPO date, key dates), live Bloomberg prices for common/warrant/rights with C-T spread, filing context, actionable flags, working open orders (EMSX), and a 3-sentence thesis distilled from the Meteora memory doc. No markdown, no headers, no bold/italic — just plain text that pastes cleanly into Bloomberg IB chat.

**Memory doc sync (Step 7):** After the output file is written and presented, the skill patches every EXISTING memory doc for tickers addressed in the run — appending an entries-log record and adding at least one bullet to the exec summary. Deeper section patches happen when the headline materially changes terms/dates/cap/chronology already in the summary. The thesis is never touched unless the headline materially shifts the directional view. This skill does NOT create new memory docs — `not_found` tickers are skipped (doc creation is the job of `seed-memory`).

**Note on yields:** Live yield recomputation and extension-deposit modeling were removed from this skill — they took too long to compute and the 8-K extension extraction was not consistently accurate. If you need yields on a specific ticker, run `trading-note-simple` (T-bill only) or `trading-note-extended` (with extension deposits) on the individual name. The full prior spec is preserved at `references/SKILL_with_yields.md` inside this skill bundle if it ever needs to be reinstated.

**Note on S-4/F-4 count:** Headlines DOES render an EDGAR-verified `s/f-4s:` count for ALL in-deal headlined names, using a **3-pass workflow** (limit=50 scan reuse + conditional targeted backup + conditional PubCo CIK lookup for FPI deals) — see Step 3c. This matches `trading-note-extended`'s full coverage. The PubCo CIK is cached in the memory doc when discovered (Step 7, only if a doc exists), so subsequent runs skip the web search.

---

## Critical Domain Knowledge

### 1. Common Outstanding, 9.9% Threshold, and Unit Coverage

The `spac-details` tool returns three separate size/structure reference fields that must ALL be surfaced in every bullet for a SPAC in our book:

**a) `common_outstanding`** — total common shares outstanding (public + sponsor). This is the full cap-table number, abbreviated in the output as "SO: X" (e.g., "SO: 27.6M" or "SO: 1.3M"). Always report this for every SPAC in our book.

**b) `pct_9_outstanding`** — the **9.9% ownership threshold** — the maximum number of shares Meteora can own before triggering a beneficial ownership filing (Schedule 13D/13G). It is NOT the total shares outstanding or the public float.
- Report the threshold as "9.9%: X" where X is the `pct_9_outstanding` value, abbreviated (e.g., "9.9%: 2.2M" or "9.9%: 594K").
- **Do NOT calculate or report our position as a percentage of the 9.9% threshold.** Just report both numbers and let the reader compare.
- If `pct_9_outstanding` is `#N/A` or 0, report "9.9%: N/A" and still report position sizes in absolute terms.

**c) `warrants_in_unit` and `rights_in_unit`** — the unit coverage (how many warrants and rights each unit contained at IPO). Render in the trading-note inline format `U=S+W/n+R/m` (NOT the legacy `Unit: W ... / R ...` style):

- `warrants_in_unit = "1/2"` → `W/2`
- `warrants_in_unit = "1/3"` → `W/3`
- `warrants_in_unit = "1"` → render as `+W` without denominator
- `warrants_in_unit = "1 for 3/4"` → `W*3/4` (fractional; render literally)
- `warrants_in_unit = "None"` or null → omit the W term

- `rights_in_unit = "1 for 1/10"` → `R/10`
- `rights_in_unit = "1 for 1/8"` → `R/8`
- `rights_in_unit = "1/5"` → `R/5`
- `rights_in_unit = "1/7 for 1"` → `R*7` (inverse — 7 rights make 1 share)
- `rights_in_unit = "None"` or null → omit the R term

**Rendering rules:**
- Both present: `U=S+W/2+R/10`
- Only warrants: `U=S+W/2`
- Only rights: `U=S+R/10`
- Neither: `U=S`

**Combined output convention:** These three fields sit on the second (positions) line of the bullet. The line reads: `C: X / W: Y / R: Z | U=S+W/n+R/m | SO: AM | 9.9%: BM`.

**Why this matters:** The 9.9% threshold alone is ambiguous without knowing the full float — a 9.9% cap of 594K could be 9.9% of 6M SO (small SPAC) or a compliance-adjusted figure. Common outstanding provides context. Unit coverage is essential for understanding dilution mechanics and rights-adjustment calculations at deal close — a SPAC with "1 warrant per unit" has very different dilution than "1/4 warrant per unit."

### 2. Position Types — ALWAYS Report All Three (Distinguishing N/A vs. 0)

Meteora holds positions across four instrument types per SPAC:
- `common_position` — Class A ordinary shares (redeemable at trust)
- `warrants_position` — Public warrants (right to buy at $11.50, typically)
- `rights_position` — Rights (convert to fraction of a share at deal close)
- `units_position` — Unsplit units (common + warrant/right bundle)

**ALWAYS report common, warrants, and rights for every SPAC in our book.** This makes it immediately clear what we do and don't hold. If units_position is non-zero, append it as well.

**CRITICAL — Distinguishing "N/A" (security doesn't exist) from "0" (security exists, we hold none):**

- **Check `warrant_ticker` and `rights_ticker` from spac-details** to determine whether the security exists at all.
- If `warrant_ticker` is 0 or null → the SPAC has NO public warrant security. Report **"W: N/A"**.
- If `warrant_ticker` is a valid ticker (e.g., "VCICW") AND `warrants_position` is 0 → the warrant exists but we hold none. Report **"W: 0"**.
- If `warrant_ticker` is a valid ticker AND `warrants_position` > 0 → report the position (e.g., "W: 785K").
- Apply the same logic to `rights_ticker` / `rights_position`: valid ticker with 0 position → "R: 0"; ticker is 0/null → "R: N/A".
- Common shares always exist for SPACs, so `common_position` of 0 is always reported as "C: 0" (never N/A).
- Units: only include if `units_position` > 0.

**Examples:**
- SPAC has warrants (VCICW) but no rights → "C: 1.1M / W: 0 / R: N/A"
- SPAC has rights (DMAAR) but no warrants → "C: 351K / W: N/A / R: 177K"
- SPAC has both warrants and rights → "C: 0 / W: 329K / R: 0"
- SPAC has neither warrants nor rights → "C: 751K / W: N/A / R: N/A"

Abbreviate large numbers: 1,104,612 → 1.1M, 784,739 → 785K, 0 → 0.

### 3. Trust Value Context

- `cash_in_trust` = per-share trust value (NAV floor for redemptions)
- `trust_balance` = total trust in millions (in-deal SPACs only)
- Trust values accrue interest over time; headline-reported trust confirmations should be compared against our model

### 4. Bucket System

Quality buckets rate SPACs from 1 (best) to 5 (worst). In-deal SPACs use `bucket`, pre-deal SPACs use `quality_bucket`:
- **Bucket 1:** High-conviction in-deal names, often with large positions
- **Bucket 2-3:** Moderate conviction
- **Bucket 4-5:** Lower conviction or smaller positions

### 5. Deadline Urgency

- `deadline` (pre-deal) or `max_deadline` (in-deal) = last date for SPAC to consummate deal or liquidate
- **Flag any SPAC with deadline within 30 days** — these are time-critical
- Extension votes near deadline are do-or-die events

### 6. In-Deal Filing Cadence

- DEFM14A = definitive merger proxy (vote is imminent)
- PREM14A = preliminary merger proxy (vote coming but not final)
- 424B3 / 424B4 = combined proxy/prospectus (definitive proxy for S-4-registered SPACs)
- S-4 / F-4 = registration statement for the combined entity's shares (F-4 used for FPI/foreign-target deals); each S-4/A or F-4/A amendment adds 1 to the count
- 8-K = current report (trust confirmations, material events, extensions)

**S-4/F-4 cadence as deal-progress signal:** A rising amendment count generally indicates the SEC review is active and the deal is progressing toward effectiveness. Stagnant counts or no S-4 on file >60 days post-announcement warrant scrutiny, especially for FPI deals where filings sometimes live on the PubCo CIK rather than the SPAC CIK — headlines now runs the PubCo CIK lookup inline (see Step 3c Pass 3).

### 7. Thesis Block — 3 Sentences from Memory Doc

Every SPAC in our book gets a `Thesis:` line below the main bullet. This is the Meteora view on the name, distilled to **3 sentences** from the Executive Summary returned by `MeteoraMCP:read-memory-doc`. Same methodology as `trading-note-simple`, just a tighter sentence cap to keep the headlines output scannable.

**Source — EXCLUSIVELY:** `MeteoraMCP:read-memory-doc(name="[TICKER]", summary_only=true)`. Pass the base common ticker (e.g., `IPCX`, `KDK`, not `IPCXR` or `KDKRW`).

**Forbidden sources** (never use any of these for the thesis, even paraphrased):
- `spac_details.notes` — sheet free-text field, systematically stale
- `spac_details.recommendation` — sheet free-text field, stale price levels and abandoned trade ideas
- The header / position / pricing lines (no re-stating CIT, position size, or C-T spread)
- Web search, EDGAR filings, sponsor / structure / sector reasoning from first principles
- Prior conversation context unless that context is a memory doc read in this same session

If the only source available is one of the above, render the missing-doc fallback instead.

**Three response cases:**

*Case 1 — Doc exists, summary returned:*
Distill the Executive Summary into **3 sentences** using the stage-bifurcated framework below. Drop a sentence (down to 2) if the doc only speaks to two dimensions; never pad to hit three.

```
Thesis: [Sentence 1.] [Sentence 2.] [Sentence 3.]
```

*Case 2 — No memory doc exists (`status: "not_found"` or equivalent):*
```
Thesis: No memory doc exists for [TICKER].
```

*Case 3 — Tool error (network / timeout / MCP down):*
```
Thesis: Memory doc fetch failed — retry or check manually.
```

Never drop the line entirely — absence is information.

**Pre-deal framework** (in priority order; drop a slot if doc is silent on it):
1. Sponsor franchise read — prior vehicle outcome, PIPE quality on prior deals, UW choice signal
2. Mandate / pipeline credibility — named industry advisors, banker movement, specialist hires vs. boilerplate
3. Current Meteora posture — exact thresholds from doc (price, size, GTC bid level)

**In-deal framework** (in priority order; drop a slot if doc is silent on it):
1. Closing-probability read — MCC status, PIPE structure and quality of names, CoC/debt overhang
2. Sponsor-incentive read — deferred UW math, WCW draws, founder-share forfeit, shell-purchase economics
3. Current Meteora posture — exact thresholds from doc (price triggers, sizing, wake-up sells)

**Distillation rules:**
- Mirror exact thresholds from the doc — `$10.75 × 200K GTC bid` not `build at a discount`
- Specificity test — if the sentence could appear verbatim in another SPAC's note, it's too generic
- Mirror the doc's calibration — don't strip hedging ("likely", "base case", "could slip") to sound more confident than the doc
- No raw header re-statement — the matrix and header already carry CIT / structure / sponsor
- No verbatim Executive Summary paragraphs — distill into your own active-voice sentences

**Tone:** Walter-facing, voice of a colleague who read the doc this morning. Terse, concrete, directional. No headings or bullets inside the rendered Thesis line.

### 8. Open Orders — EMSX Blotter (Flag-Only)

Walter's working orders on the EMSX blotter are surfaced as a per-ticker indicator **only when open orders exist**. Headlines is not the place for the full ORDERS section that lives in trading notes — just a one-line flag so Walter knows what's working before he reads the headline.

**Eligibility:** every ticker in our book gets an `emsx-blotter` call (in-deal AND pre-deal). Skip for NOT IN BOOK and non-SPAC tickers.

**Coverage — all instruments:** the blotter call returns orders across common, warrants, rights, AND units. Render orders for ALL instruments where they exist, not just common. Walter often has working warrant or rights orders that are equally relevant to the morning read.

**Call:**
```
MeteoraMCP:emsx-blotter(ticker="VCIC")
```

Pass the BASE common ticker — the blotter returns all related instruments (warrants, rights, units) automatically.

**Filter:** include only orders with `status = "WORKING"`. Drop filled, cancelled, expired, or partially-filled-and-done orders.

**Output indicator:** if any WORKING orders exist across any instrument, render a one-line `Orders:` flag in the ticker block:

```
  Orders:   BUY 25k VCIC @ $10.66 GTC | SELL 10k VCICW @ $0.55 GTC | BUY 200 VCICR @ $0.30
```

Format: `[SIDE] [size] [ticker] @ [limit] [duration]`. Comma-separated by `|`. If multiple working orders on same instrument, list each.

- **Size formatting:** equity uses k notation (`25k`, `22.5k`, `4.6k`, `300`); options/warrants/rights show raw integer contract count (`200`, `100`, `300`).
- **Side:** SIDE = `BUY` or `SELL`.
- **Duration:** GTC if the order has tif=GTC; otherwise omit (DAY is implied).
- **Sort:** SELL before BUY; within each side, sort by limit price ascending.

**Omit the Orders: line entirely if no WORKING orders exist on any instrument.** Never render an empty Orders line.

If `emsx-blotter` returns an error for a ticker, render `Orders: ⚠ blotter fetch failed` once and move on — do not retry.

---

## Tool Call Budget

This skill is designed to minimize tool calls to stay within turn limits. For a typical 10-ticker morning with ~5 in-deal names and ~7 names in our book:

| Step | Calls | What |
|---|---|---|
| Step 2 | 2-3 | Bulk spac-details (ALL indeal, ALL predeal — no position filter). +1 bash if predeal result exceeds context and needs grep extraction. |
| Step 2b | 1 | Batch get-price for all common/warrant/rights tickers (bid/ask/last for mid + C-T spread) |
| Step 2c | ~7 | `read-memory-doc(name=TICKER, summary_only=true)` — one per ticker in our book. Not batchable. |
| Step 2d | ~7 | `emsx-blotter(ticker=TICKER)` — one per ticker in our book. Not batchable. |
| Step 3 | ~5 | edgar-filings(limit=50), one per in-deal headline ticker (proxy/vote search) |
| Step 3b | ~3-5 | edgar-filing-text(summary=true) for proxies found |
| Step 3c | 0-5 | S-4/F-4 count: Pass 1 (limit=50 scan reuse — zero net calls), Pass 2 (1-2 targeted form_type calls when Pass 1 returns zero and deal_announced >60d), Pass 3 (read-memory-doc cache check + 1-2 web searches + 1 edgar-filings PubCo call when Passes 1+2 return zero and deal looks FPI) |
| Non-SPAC | ~1-2 | Web searches for non-SPAC tickers |
| **Total** | **~25-35** | |

**Eligibility gates that bound the budget:**
- Step 2c (memory doc) and 2d (blotter) skip NOT IN BOOK and non-SPAC tickers entirely.
- We do NOT run extension-deposit 8-K extraction (that workflow was removed when yields were removed — too slow and inconsistently accurate; if you need yields on a specific name, run `trading-note-extended`).
- We DO render an EDGAR-verified S-4/F-4 count for ALL in-deal headlined names, using the **full 3-pass workflow**: limit=50 scan reuse (Pass 1, zero net calls), targeted `form_type="S-4"`/`"F-4"` calls (Pass 2, conditional on zero Pass 1 + >60 days), and PubCo CIK lookup (Pass 3, conditional on zero Passes 1+2 + FPI indicator). Pass 3 is no longer deferred — Walter shouldn't have to chase the count manually when an FPI name is at a vote. The PubCo CIK is cached in the memory doc once discovered (Step 7, but only if a memory doc already exists — this skill doesn't create new docs).

**No per-ticker fallbacks needed for spac-details.** The two unfiltered bulk pulls return every SPAC in our book.

**Step 7 (memory doc patches) is intentionally UNBUDGETED.** It runs after the output file is written/presented and may span multiple turns. Patches are independent per-ticker; do not compress them to hit a turn limit — finish the current ticker cleanly and continue in the next turn if needed. Per-ticker, expect 1 `update-memory-doc` call (entries log) + 1 `patch-memory-summary` call (exec summary, all edits batched), but only for tickers with EXISTING docs.

---

## Workflow

### Step 1: Extract All Tickers from the Headlines

Parse the input text and extract every ticker symbol mentioned. Include:
- Standard SPAC common tickers (e.g., VCIC, HYAC, DMYY)
- Unit tickers (ending in U, e.g., FGIIU, XFLH/U)
- Warrant tickers (ending in W, /WS, e.g., PLMKW, HYAC/WS)
- Rights tickers (ending in R, e.g., CHACR, DMAAR)
- Non-SPAC tickers mentioned in context (e.g., HIMS, TALK) — note these separately
- New S-1 filings that may not be in our book yet

Also extract the key event for each ticker:
- Deal announcement / LOI
- Proxy filing (PREM14A, DEFM14A)
- Vote date set or changed
- Trust confirmation
- Extension vote
- Charter extension
- Unit split
- Over-allotment exercise
- IPO / S-1 filing
- Halt / pending news
- Material agreement / 8-K
- PIPE announcement or supplement

### Step 2: Bulk Pull Internal Book (TWO Calls Total)

Pull the ENTIRE book in TWO unfiltered bulk calls upfront:

**Call 1 — ALL in-deal SPACs:**
```
spac-details(stage="indeal")
```

**Call 2 — ALL pre-deal SPACs:**
```
spac-details(stage="predeal")
```

These two calls return every SPAC in our tracking sheet — with or without positions. Cache both result sets and match headline tickers against them.

**Handling oversized results:** The predeal bulk pull (218+ SPACs) frequently exceeds the context window and gets stored as a JSON file at a path like `/mnt/user-data/tool_results/3_17_spac-details_toolu_XXXXX.json`. When this happens, use `bash_tool` with a Python one-liner to extract ONLY the headline tickers from the stored file:

```python
cat /mnt/user-data/tool_results/<STORED_FILE>.json | python3 -c "
import json, sys
raw = json.load(sys.stdin)
# Handle MCP response wrapper: the file may be a list with a 'text' entry containing the JSON
if isinstance(raw, list):
    for item in raw:
        if isinstance(item, dict) and item.get('type') == 'text':
            data = json.loads(item['text'])
            results = data.get('results', [])
            break
    else:
        results = []
elif isinstance(raw, dict):
    results = raw.get('results', [])
else:
    results = []

tickers_needed = ['GDST', 'IBAC', 'AACI', 'SAAQ', 'GIX', 'FTW']  # <-- replace with actual headline tickers not found in indeal
for r in results:
    st = str(r.get('spac_ticker', '')).upper()
    ut = str(r.get('unit_ticker', '')).upper()
    wt = str(r.get('warrant_ticker', '')).upper()
    rt = str(r.get('rights_ticker', '')).upper()
    all_tickers = [st, ut, wt, rt]
    for t in tickers_needed:
        for at in all_tickers:
            if t.upper() == at or t.upper() in at:
                print(json.dumps(r, indent=2))
                break
"
```

This extracts only the matching SPAC records from the stored file, keeping the output small enough for context. Substitute the actual stored file path and the list of tickers still needed after checking the indeal results. The indeal bulk pull is typically small enough to fit in context directly.

**Matching logic:**
- For each headline ticker, strip suffixes (W, R, U, /WS, /U, /R) to get the common ticker
- Search the cached in-deal and pre-deal results for a match on `spac_ticker`, `warrant_ticker`, `rights_ticker`, or `unit_ticker`
- If found → use the cached data directly (no additional spac-details call needed)
- If NOT found → the ticker is NOT IN BOOK. No individual fallback lookup needed — the unfiltered bulk pulls are the complete book.

**Do NOT call spac-details for obvious non-SPAC tickers** (e.g., JOBY, WALD, BZFD, MAPS) — use web search for those instead.

For tickers confirmed NOT IN BOOK (new S-1 filings, recently IPO'd SPACs), use web search to gather basic details (sponsor, size, focus, underwriter).

### Step 2b: Pull Bid / Ask / Last for All SPAC Tickers

For all SPAC tickers in our book, make ONE batched `get-price` call. The Pricing line uses the live mid `(bid + ask) / 2` for the C-T spread and to display each instrument's price.

```
get-price(
  tickers=["PELI US Equity", "VCIC US Equity", "HYAC US Equity", ...],
  fields=["BID", "ASK", "PX_LAST"],
  period="5d"
)
```

**Ticker format rules** (mirroring `trading-note-simple`):
- **Common**: pass with ` US Equity` suffix (`VCIC US Equity`, `BACQ US Equity`)
- **Warrant**: if it contains a slash (`HYAC/WS`), pass with ` US Equity` suffix (`HYAC/WS US Equity`); if plain alphanumeric (`PLMKW`), pass with ` US Equity` (`PLMKW US Equity`)
- **Rights**: pass with ` US Equity` (`DMAAR US Equity`)
- **Unit (unsplit)**: pass with ` US Equity` (`FGIIU US Equity`, `XFLH/U US Equity`)
- Skip if ticker is 0, null, empty, or starts with `#N/A`

**Price selection per ticker:**
- **Mid** (computed as `(bid + ask) / 2`) is authoritative for the displayed Pricing line and the C-T spread.
- Fall back to `PX_LAST` (last trade) only if both bid and ask are unavailable AND the last trade is recent.
- If all three are unavailable, report `[TICKER] no trade | C-T: N/A` for that ticker.

**Compute C-T** for each ticker: `mid - cash_in_trust` (from spac-details). Signed.

**Formatting rules:**
- Report as `Pricing: [TICKER] $X.XX (mid) | ... | C-T: $X.XX` (or `-$X.XX` if below trust)
- For unit tickers, note the unit ticker used (e.g., `[XCBEU] $9.95`)
- Round C-T to 2 decimal places
- If Bloomberg returns no data (illiquid, no recent trades), report `[TICKER] no trade` and `C-T: N/A`

**Why this matters:** The spread to trust is the core risk/return metric for SPAC arb. A tight spread (e.g., -$0.03) means the position is well-protected by trust. A wide discount (e.g., -$0.50) flags potential basis risk or market concern. A premium (e.g., +$0.15) may indicate deal momentum or squeeze potential.

### Step 2c: Pull Memory-Doc Summaries (One Per Ticker In Our Book)

For every ticker in our book — in-deal AND pre-deal — call `read-memory-doc` to fetch the Executive Summary that drives the `Thesis:` line:

```
MeteoraMCP:read-memory-doc(name="VCIC", summary_only=true)
```

Pass the **base common ticker** (e.g., `VCIC`, not `VCICW`). One call per ticker — these are not batchable but are cheap relative to `get-price`.

**Three response cases** (handled per Section 7):
- Doc exists → distill to 3 sentences using the stage-bifurcated framework
- Doc missing (`status: "not_found"`) → render `Thesis: No memory doc exists for [TICKER].`
- Tool error → render `Thesis: Memory doc fetch failed — retry or check manually.`

**Skip memory-doc reads for:**
- Tickers NOT IN BOOK (no Meteora view exists)
- Non-SPAC tickers (HIMS, JOBY, etc.)
- New S-1 filings not yet in book

### Step 2d: Pull EMSX Blotter (One Per Ticker In Our Book)

For every ticker in our book — in-deal AND pre-deal — call `emsx-blotter` to fetch any working orders Walter has on the book. The call returns orders across common, warrants, rights, AND units automatically — pass only the BASE common ticker.

```
MeteoraMCP:emsx-blotter(ticker="VCIC")
```

**Filter:** Keep only orders with `status = "WORKING"`. Drop FILLED, CANCELLED, EXPIRED, or any "done" status.

**Output:** Section 8 covers the rendering rules. Render an `Orders:` line in the ticker block ONLY if at least one WORKING order exists across any instrument. Omit entirely if no working orders.

**Skip blotter reads for:**
- Tickers NOT IN BOOK (no orders possible)
- Non-SPAC tickers
- New S-1 filings not yet in book

If `emsx-blotter` returns an error for a ticker, render `Orders: ⚠ blotter fetch failed` once and proceed — do not retry within the session.

### Step 3: Pull Recent Filings for In-Deal SPACs (ONE Call Per Ticker)

For every ticker that is `stage: "indeal"` AND is mentioned in the headlines, pull recent SEC filings using a **single call with limit=50**:

```
edgar-filings(ticker=TICKER, limit=50)
```

This returns the 50 most recent filings of ANY type, which is deep enough to surface proxy filings even when buried under bursts of 425s and DEFA14As. **No fallback cascade.** Scan the returned list in-line for:

- **DEFM14A** — definitive merger proxy (vote is imminent)
- **PREM14A** — preliminary merger proxy (vote coming but not final)
- **424B3 / 424B4** — combined proxy/prospectus for S-4 registered SPACs (serves same function as DEFM14A)
- **8-K** — trust confirmations, material agreements, extensions, PIPE supplements
- **S-4 / F-4** — proxy/registration statement amendments

**Priority logic:** If the limit=50 list contains a DEFM14A, use that as the proxy. If no DEFM14A but a 424B3 or 424B4 is present, use that instead (some SPACs register on S-4 and file their definitive proxy as a 424B supplement — see BACQ case study below). If neither, check for PREM14A. If none of the above exist in the 50 filings, note "No proxy filed yet" in the output.

**BACQ CASE STUDY (discovered 3/10/26):** BACQ (Inflection Point Acquisition Corp. IV) had NO DEFM14A or PREM14A on file. The proxy was filed as a **424B3** (accession 0001213900-26-015629, filed 2026-02-12) because the merger shares were registered on an S-4 (filed 2026-01-14). The 424B3 title section read: `"NOTICE OF EXTRAORDINARY GENERAL MEETING TO BE HELD ON MARCH 12, 2026"` and the Date/Time subsection confirmed: `"The extraordinary general meeting will be held at 10:00 a.m. Eastern Time, on March 12, 2026."` The redemption deadline was TODAY (3/10/26) when we ran headlines — and we hold 1.8M shares. **This is why scanning for 424B3/424B4 matters — don't just look for DEFM14A in the list.**

For any filing with a vote date, extract:
- Meeting date and time
- Record date
- Redemption deadline

**To read vote date from a proxy:** Call `edgar-filing-text` with `summary=true` to get the TOC. **Often the vote date is visible directly in the TOC section titles** (e.g., `"NOTICE OF EXTRAORDINARY GENERAL MEETING TO BE HELD ON MARCH 12, 2026"`). If the date is already clear from the TOC title, do NOT waste a call reading the subsection — just extract the date and move on. Only read into a subsection if the TOC titles do not contain a specific date.

### Step 3b: MANDATORY Vote Date Extraction for In-Deal Positions

**THIS STEP IS NON-NEGOTIABLE.** For every in-deal SPAC where we hold ANY position (common, warrants, rights, or units), you MUST:

1. Scan the limit=50 filing list from Step 3 for any **DEFM14A**, **424B3**, **424B4**, or **PREM14A** filing.
2. If a DEFM14A is found — read it to extract the vote date (regardless of what the headline event is about).
3. If no DEFM14A but a **424B3 or 424B4** is found — read that instead (it serves as the proxy for S-4 registered SPACs).
4. If only a **PREM14A** is found — note the expected vote date if disclosed.
5. If none of the above appear in the 50 filings — note "No proxy filed yet" in the output.

**Why this matters:** A headline may mention a SPAC for a minor event (grant, press release, PIPE supplement) while a definitive proxy with an imminent vote date is already on file. The headline event does NOT determine whether a vote is coming — only the EDGAR filings do. Missing a vote date means missing a redemption deadline, which is a direct P&L risk.

**Extraction procedure:**
- Call `edgar-filing-text(accession_number=..., ticker=..., summary=true)` on the proxy (DEFM14A, 424B3, or 424B4)
- **Check the TOC titles first.** The vote date is often directly in a section title like `"NOTICE OF EXTRAORDINARY GENERAL MEETING TO BE HELD ON MARCH 12, 2026"`. If you can see the date in the title, extract it immediately — do NOT read into the subsection.
- Only if the TOC titles are ambiguous (no specific date visible), read the "Date, Time and Place" or "Extraordinary General Meeting" subsection using offset/max_chars
- Extract: meeting date, meeting time, virtual/physical location, record date if visible

**If a vote date is found within 30 days, flag it prominently in the bullet — even if the headline event itself is unrelated to the vote.**

### Step 3c: S-4/F-4 Count (In-Deal Names — EDGAR 3-Pass)

**Eligibility:** ALL in-deal SPACs mentioned in headlines. Skip pre-deal, NOT IN BOOK, and non-SPAC tickers — S-4/F-4 cadence isn't relevant outside of an active business combination.

For every eligible in-deal ticker, derive an EDGAR-verified S-4/F-4 amendment count using the **full 3-pass workflow** — this matches `trading-note-extended`'s coverage. Pass 3 (PubCo CIK) is no longer deferred; deferring it was a false economy because Walter has to chase the count manually anyway when an FPI name comes up at a deal vote.

**Pass 1 (zero net calls — reuse Step 3 result):** Scan the `limit=50` filing list already pulled for the proxy search. Count any filing whose `form` field is **S-4, S-4/A, F-4, or F-4/A**. The base S-4 (or F-4) is amendment #0 and counts as 1; each amendment adds 1.

**Pass 2 (1 backup call, conditional):** ONLY run this if Pass 1 returned **zero** S-4/F-4 filings AND `deal_announced` is more than **60 days ago**. The reason: an in-deal name with a chatty filing cadence (lots of 8-K, 425, DEFA14A) can push S-4 filings outside the 50-most-recent window. Run a single combined targeted call:

```
edgar-filings(ticker="[TICKER]", form_type="S-4", limit=10)
```

If that returns nothing, also try `form_type="F-4"` (one additional call) — but only if domicile or target name suggests an FPI deal (Cayman, BVI, China, UK, Israel target). Cap Pass 2 at **2 calls per in-deal name maximum**.

**Pass 3 (PubCo CIK lookup, conditional):** Run when ALL of these hold:
- Passes 1 + 2 returned zero S-4/F-4 on the SPAC CIK
- The deal looks like an FPI (foreign target, foreign domicile, or memory doc / spac-details `notes` mentions a foreign Pubco)
- `deal_announced` is more than 60 days ago (avoids spinning on freshly-announced deals)

The Pass 3 procedure:

1. **Check the memory doc first.** If `read-memory-doc(name="[TICKER]", summary_only=true)` (already pulled in Step 2c) contains a PubCo CIK in the Identity section — phrased as `PubCo CIK: NNNNNNN` or similar — use that directly and skip the web search. Treat the cached CIK as authoritative; the doc is the durable cache for this lookup.

2. **If no cached CIK, web-search to discover it.** Use queries like:
   ```
   web_search: "[TARGET NAME] F-4 SEC EDGAR"
   web_search: "[PUBCO NAME] [target jurisdiction] SEC registration statement"
   ```
   Look for `https://www.sec.gov/Archives/edgar/data/[CIK]/...` URLs in search results. The CIK is the numeric segment after `/data/`.

3. **Run the PubCo EDGAR call:**
   ```
   edgar-filings(cik="[PUBCO_CIK]", limit=20)
   ```
   Scan the result for `form` values **S-4, S-4/A, F-4, F-4/A** (almost always F-4/F-4/A for FPI Pubcos). Count them; that is the EDGAR-verified count. Also note any **DRS / DRS/A** on the PubCo for the confidential-draft callout.

4. **Patch the discovery back into the memory doc (Step 7 obligation).** If Pass 3 discovered a PubCo CIK that was NOT already in the memory doc Identity section, Step 7 MUST patch it in — this is what turns the second headlines run on this name from a 2-search lookup into a zero-search cache hit. See Step 7 for the patch shape.

Cap Pass 3 at **3 calls per in-deal name maximum** (1 read-memory check, ~1-2 web searches, 1 edgar-filings call). If web search yields no CIK after 2 queries, abandon Pass 3, render the count as `0 (EDGAR — none on SPAC CIK; PubCo lookup failed, retry manually)`, and log a footnote so Walter knows to follow up.

**DRS / DRS/A:** Note separately if visible in any Pass, but do NOT aggregate with public S-4/F-4 unless the filing has flipped public. For headlines purposes, just include the public count — DRS callouts go in the `Filing:` line free-text only when material.

**Counting rule (mirrors `trading-note-extended`):**
- 0 filings on SPAC CIK and 0 on PubCo CIK after Pass 3 → `s/f-4s: 0 (EDGAR)`
- 0 filings on SPAC CIK, N filings on PubCo CIK → `s/f-4s: N (EDGAR — PubCo CIK NNNNNNN)`
- N filings on SPAC CIK → `s/f-4s: N (EDGAR)`
- If Pass 3 was triggered but PubCo CIK could not be resolved → `s/f-4s: 0 (EDGAR — none on SPAC CIK; PubCo lookup failed, retry manually)`

**Output:** Append the count as a segment on the existing `Filing:` line, separated by ` | `. Do NOT create a dedicated S-4 line — keep the block compact.

```
Filing:     DEF 14A 4/22, vote 5/12 | s/f-4s: 3 (EDGAR — PubCo CIK 2097725)
```

If no proxy context applies but the count is still derivable:
```
Filing:     no proxy yet | s/f-4s: 1 (EDGAR)
```

**Do NOT use `s4_amendments` from `spac-details`** — that field is flagged as bugged and is systematically unreliable. The count comes from EDGAR only.

### Step 4: Cross-Reference Headline Data vs. Our Model

For each ticker, compare headline-reported data against our internal model:

| Headline Data | Internal Field | Flag If |
|---|---|---|
| Trust per share | `cash_in_trust` | Differs by > $0.02 |
| Total trust balance | `trust_balance` | Differs by > $1M |
| Vote date | Filing / proxy | New or changed date |
| PIPE size | Prior PIPE info | Increased or new PIPE |
| Redemption price | `cash_in_trust` | Should approximately match |
| Deal valuation | Notes | Compare to prior if available |
| Estimated close/event | `est_date` | Moved materially — note in the Filing or Flags line |

### Step 5: Compose the Output

**FORMAT: Write output to a .txt file and present it to the user.** The file must be copy-pasteable directly into Bloomberg IB chat without losing formatting. This means:

- Write ALL output to a plain text file saved at `/mnt/user-data/outputs/spac_headlines_YYYY-MM-DD.txt` (using today's date)
- Use the `create_file` tool to write the file, then `present_files` to share it with the user
- One **multi-line block per ticker**, separated by ONE blank line. Each ticker block leads with a `-` bullet on the headline line; subsequent lines of the same block are indented with 2 spaces (no leading `-`)
- NO markdown formatting (no **, no ##, no >, no backtick code blocks)
- NO categories, groupings, or section headers — flat list of ticker blocks in order of urgency
- Use ALL CAPS sparingly for critical flags (VOTE 3/19, DEADLINE 3/11, NO POSITION, NOT IN BOOK)
- **Bloomberg Ticker Formatting:** Format the first mention of each SPAC common ticker as `{TICKER US Equity} [TICKER]` — curly-brace version renders as a live Bloomberg security link, bracket version survives copy-paste round-trips (Bloomberg strips curly braces on copy). For non-SPAC tickers, also use this dual format. The warrant and/or rights ticker (if they exist in spac-details) appear on a final line of the block as `Tickers: {VCICW US Equity} [VCICW] | {VCICR US Equity} [VCICR]`. Omit the line entirely if neither warrant nor rights ticker exists.
- The .txt file should contain ONLY the plain text ticker blocks and the summary line — no preamble, no explanation
- After presenting the file, add a brief conversational summary in the chat (e.g., "X names with positions, Y votes upcoming") but the full detail lives in the .txt file

**Ordering:** Sort ticker blocks by urgency:
1. Tickers with votes/deadlines within 14 days where we hold a position
2. Tickers with votes/deadlines within 30 days where we hold a position
3. Tickers where we hold a position (other events)
4. Tickers with no position but still SPAC-relevant
5. Non-SPAC mentions (brief, 1 line each)
6. New S-1 filings not in book (brief, 1 line each)

**Per-Ticker Block Layout (SPACs in our book):**

The block is a sequence of labeled lines under the headline. Lines that don't apply (e.g., `Deal:` for pre-deal, `Orders:` when none working) are OMITTED entirely — never rendered as empty.

```
- {TICKER US Equity} [TICKER] (news event): [headline summary in 1-2 sentences].
  Position:   C: XK / W: YK / R: ZK | U=S+W/n+R/m | SO: AM | 9.9%: BM
  Profile:    B[N] [Category] | Dom: XX | UW [underwriter]
  Pricing:    [TICKER] $X.XX (mid) | [TICKERW] $X.XX | [TICKERR] $X.XX | C-T: $X.XX
  Trust:      $XXXmm | CIT $X.XX                                          ← in-deal only
  IPO:        M/D/YY | proceeds $XXmm                                     ← proceeds = pre-deal only
  Deal:       Target: TargetCo | announced M/D/YY | PIPE $XXmm            ← in-deal only
  Dates:      est. M/D/YY | deadline M/D/YY | outside M/D/YY              ← outside = in-deal only
  Filing:     [proxy type filed M/D, vote M/D — or "no proxy yet"] | s/f-4s: N (EDGAR)   ← s/f-4s = ALL in-deal headlined names
  Flags:      [VOTE M/D, DEADLINE M/D, LARGE POSITION, TRUST DELTA]        ← only if any apply
  Orders:     SELL 25k VCIC @ $10.66 GTC | BUY 200 VCICW @ $0.50            ← only if WORKING
  Thesis:     [3-sentence distillation from memory doc — see Section 7]
  Memory:     [one-line summary of Step 7 patch — entries log + exec summary edits]  ← only if memory doc exists
  Tickers:    {TICKERW US Equity} [TICKERW] | {TICKERR US Equity} [TICKERR]
```

**Line-by-line construction rules:**

- **Headline line (the `-` bullet line):** `{TICKER US Equity} [TICKER] (news event): [summary]`. The parenthetical describes ONLY the event from the headlines (e.g., "PREM14A filed", "trust confirmation", "halted for news", "unit split", "ARPA-E grant"). Do NOT include target name or deal status in the parenthetical — that goes on the `Deal:` line.

- **Position line:** `Position: C: X / W: Y / R: Z | U=S+W/n+R/m | SO: AM | 9.9%: BM`
  - Use the N/A vs. 0 distinction from Section 2 (warrant_ticker null → `W: N/A`)
  - Unit notation per Section 1 (`U=S+W/2+R/10`, `U=S+W/2`, `U=S+R/10`, `U=S`)
  - SO from `common_outstanding`; abbreviate (27,600,000 → 27.6M). If 0/null/`#N/A`, render `SO: N/A`.
  - 9.9% from `pct_9_outstanding`; abbreviate. If 0/null/`#N/A`, render `9.9%: N/A`.
  - If `units_position` > 0, append ` | U: WK` to the position list (e.g., `C: 0 / W: 0 / R: N/A / U: 142K`).

- **Profile line:** `Profile: B[N] [Category] | Dom: XX | UW [underwriter]`
  - Bucket from `bucket` (in-deal) or `quality_bucket` (pre-deal); render as `B1`, `B2`, etc.
  - Domicile from `domicile` field (e.g., `DE`, `KY`, `BVI`). Omit `Dom:` segment entirely if missing.
  - Underwriter from `underwriter` field. Omit `UW` segment if missing.

- **Pricing line:** `Pricing: [TICKER] $X.XX (mid) | [TICKERW] $X.XX | [TICKERR] $X.XX | C-T: $X.XX`
  - Common mid from Bloomberg `(bid+ask)/2`; if no data, render `[TICKER] no trade`.
  - Warrant mid: from Bloomberg if `warrant_ticker` exists and price returned; OMIT the warrant segment if `warrant_ticker` is null or no price data.
  - Rights mid: same logic as warrant.
  - C-T from `mid - cash_in_trust`, signed; if mid is missing, render `C-T: N/A`.
  - Use the bracketed ticker label so the reader can match price to instrument.

- **Trust line (in-deal ONLY):** `Trust: $XXXmm | CIT $X.XX`
  - Trust balance from `trust_balance` (in $mm). Render as `$XXXmm` (whole millions) or `$XX.Xmm` (one decimal if fractional).
  - CIT from `cash_in_trust` per share.
  - **Pre-deal SPACs:** OMIT this line entirely. CIT for pre-deal is captured on the IPO line (see below) along with proceeds — pre-deal trust balance is implicit from proceeds.
  - **PRE-DEAL ALTERNATIVE:** for pre-deal, render `Trust: CIT $X.XX` (CIT only, no balance). This keeps the line for completeness without inventing a `trust_balance` value spac-details doesn't return for pre-deal.

- **IPO line:** `IPO: M/D/YY | proceeds $XXmm`
  - IPO date from `ipo_date`, formatted M/D/YY. If missing, render `IPO: n/a`.
  - **Pre-deal:** include `proceeds $XXmm` from `ipo_proceeds` (in $mm). Omit segment if missing.
  - **In-deal:** OMIT the proceeds segment (less relevant once a deal is announced; trust balance on the Trust line carries the equivalent info).

- **Deal line (in-deal ONLY):** `Deal: Target: TargetCo | announced M/D/YY | PIPE $XXmm (per spac-insider)`
  - Target from `target` field. Strip any "Announced: " prefix that may be embedded.
  - Announced date from `deal_announced`, M/D/YY.
  - PIPE from `pipe_size` ($mm). Render rules per `trading-note-extended` PIPE-line spec:
    - `> 0` → `PIPE $XXmm (per spac-insider)`. Format whole millions as `$500mm`; fractional ≥1 as one decimal `$11.5mm`; sub-million as `$0.45mm`.
    - `== 0` → `PIPE: none disclosed (per spac-insider)`
    - null/missing → `PIPE: N/A (per spac-insider)`
  - Always include the `(per spac-insider)` disclaimer.
  - **Pre-deal SPACs:** OMIT this line entirely.

- **Dates line:** `Dates: est. M/D/YY | deadline M/D/YY | outside M/D/YY`
  - est_date from spac-details, formatted M/D/YY
  - deadline from `deadline` (pre-deal) or `max_deadline` (in-deal), formatted M/D/YY
  - **outside_date (in-deal ONLY):** from `outside_date` field. Append as third segment. OMIT for pre-deal.
  - If a field is missing/null, render `n/a` in that slot but keep the line.

- **Filing line:** `Filing: [proxy type filed M/D, vote M/D, or "no proxy yet"] | s/f-4s: N (EDGAR)`. Include the trust comparison here too if material (`trust matches model` or `headline trust $10.49 vs. model $10.51 — TRUST DELTA`).
  - **`s/f-4s:` segment (ALL in-deal headlined names):** Append per Step 3c — count of S-4, S-4/A, F-4, F-4/A on EDGAR derived from the 3-pass workflow (limit=50 scan + conditional targeted backup + conditional PubCo CIK lookup for FPI deals). Always suffix with `(EDGAR)`. When Pass 3 ran and returned the count, include the PubCo CIK in the suffix: `s/f-4s: 3 (EDGAR — PubCo CIK 2097725)`. When Pass 3 was triggered but PubCo CIK could not be resolved: `s/f-4s: 0 (EDGAR — none on SPAC CIK; PubCo lookup failed, retry manually)`. **NEVER** use `s4_amendments` from `spac-details` — that field is bugged.
  - OMIT the `s/f-4s:` segment for pre-deal SPACs, NOT IN BOOK, and non-SPAC tickers (S-4 cadence isn't relevant outside an active business combination).
  - Omit the entire Filing line if no filing context applies AND there's no s/f-4s segment to render (e.g., pre-deal SPAC with no proxy or 8-K activity in headlines).

- **Flags line:** Only render if there is at least one flag. Comma-separated, ALL CAPS. Omit the entire line if no flags apply.

- **Orders line (conditional):** Per Section 8. Render ONLY if at least one WORKING order exists across any instrument (common, warrant, rights, units). Format: `[SIDE] [size] [ticker] @ [limit] [duration]`, separated by ` | `. SELL before BUY; ascending limit price within each side. OMIT entirely if no working orders.

- **Thesis line:** Per Section 7. Always rendered for SPACs in our book — never dropped, even when the doc is missing or fetch fails (use the explicit fallback strings).

- **Memory line (conditional):** Per Step 7. Renders ONLY when a memory doc EXISTS for the ticker (Step 2c Case 1) — i.e., the same condition under which Step 7 will execute a patch. One-line summary of what Step 7 will patch (the planned action; Step 7 itself executes after the file is presented). Format:
  - Floor only (entry + bullet): `Memory: entry logged + bullet in [section name] of exec summary`
  - With deeper edits: `Memory: entry logged + bullet + [Identity / Key Dates / Deal Terms / Cap Structure / F-4 Timeline / Filing Chronology / Current Posture] updated ([brief reason])`
  - With thesis touch (rare): `Memory: entry logged + bullet + [section] + thesis updated ([what shifted])`
  - When fetch failed in Step 2c (Case 3): OMIT the line; the Thesis line already renders the fallback string and Step 7 will skip this ticker.
  - When doc is `not_found` (Case 2): OMIT the line; nothing to patch.

  Examples:
  - `Memory: entry logged + bullet in Key Filings`
  - `Memory: entry logged + bullet + Key Dates updated (vote 6/9)`
  - `Memory: entry logged + bullet + Cap Structure + Key Dates updated (PIPE upsized to $100mm)`
  - `Memory: entry logged + bullet + thesis updated (deal terminated)`

- **Tickers line:** Only render if `warrant_ticker` and/or `rights_ticker` exist in spac-details. Omit the line entirely if neither exists. Format: `Tickers: {WT US Equity} [WT]` or `Tickers: {RT US Equity} [RT]` or `Tickers: {WT US Equity} [WT] | {RT US Equity} [RT]`. For unsplit-unit tickers held in book, append ` | {UT US Equity} [UT]` if `units_position > 0`.

**Per-Ticker Block Layout (SPACs NOT in our book):**

Single-line bullet — no multi-line structure needed since we have no position context to render:

```
- {TICKER US Equity} [TICKER]: [headline summary]. NOT IN BOOK. [any additional context from web search]
```

**Per-Ticker Block Layout (Non-SPAC tickers):**

Single-line bullet:

```
- {TICKER US Equity} [TICKER]: [1-line headline summary]. Not SPAC.
```

**Examples of complete ticker blocks (plain text, copy-paste ready):**

```
- {VCIC US Equity} [VCIC] (PREM14A filed): Amended proxy sets 3/27 vote, NAV $10.68.
  Position:   C: 1.1M / W: 0 / R: N/A | U=S+W/2 | SO: 22.1M | 9.9%: 2.2M
  Profile:    B1 Crypto | Dom: DE | UW Cantor
  Pricing:    [VCIC] $10.67 (mid) | [VCICW] $0.42 | C-T: -$0.02
  Trust:      $241mm | CIT $10.69
  IPO:        12/14/23
  Deal:       Target: ChainCo | announced 1/22/26 | PIPE $50mm (per spac-insider)
  Dates:      est. 6/9/26 | deadline 6/10/26 | outside 9/14/26
  Filing:     PREM14A 3/14, no DEFM14A yet — vote 3/27 per proxy | s/f-4s: 2 (EDGAR)
  Flags:      VOTE 3/27, LARGE POSITION
  Orders:     SELL 25k VCIC @ $10.67 GTC | BUY 10k VCICW @ $0.40
  Thesis:     Repeat sponsor with prior PIPE-raising track record on first vehicle; UW upgrade signals move upmarket. Long 1.1M commons at -2c, sponsor depositing $0.025/sh/mo per memory doc — closing-probability read is constructive. Hold; do not chase above $10.68.
  Memory:     entry logged + bullet + Key Dates updated (vote 3/27, NAV $10.68)
  Tickers:    {VCICW US Equity} [VCICW]

- {DMAA US Equity} [DMAA] (trust confirmation): Trust confirmed $241.3M (~$10.49/sh), disputed withdrawal did NOT impact trust.
  Position:   C: 351K / W: N/A / R: 177K | U=S+R/8 | SO: 23.0M | 9.9%: 2.3M
  Profile:    B4 Pharma | Dom: DE | UW Cohen
  Pricing:    [DMAA] $10.42 (mid) | [DMAAR] $0.18 | C-T: -$0.07
  Trust:      $241mm | CIT $10.49
  IPO:        9/14/23
  Deal:       Target: PharmaCo | announced 11/4/25 | PIPE: none disclosed (per spac-insider)
  Dates:      est. 4/29/26 | deadline 10/29/26 | outside 4/29/27
  Filing:     trust matches model | s/f-4s: 3 (EDGAR)
  Thesis:     Bucket-4 pharma SPAC with rights-only structure; sponsor playbook is extension-driven and committed to closing. Long 351K commons at -7c plus 177K rights as deal-closing optionality. Hold; do not add above trust.
  Memory:     entry logged + bullet in Key Filings
  Tickers:    {DMAAR US Equity} [DMAAR]

- {CDAQF US Equity} [CDAQF] (preliminary proxy for extension): Files preliminary proxy for 3-month charter extension.
  Position:   C: 0 / W: 329K / R: N/A | U=S+W/3 | SO: 115K | 9.9%: 11K
  Profile:    B3 Mining | Dom: KY | UW Maxim
  Pricing:    [CDAQF] no trade | [CDAWF] $0.12 | C-T: N/A
  Trust:      $1.2mm | CIT $10.85
  IPO:        4/20/22
  Deal:       Target: MineCo | announced 8/1/24 | PIPE $11.5mm (per spac-insider)
  Dates:      est. 4/19/26 | deadline 4/20/26 | outside 7/20/26
  Filing:     PREM14A 3/15 — extension vote upcoming | s/f-4s: 0 (EDGAR — none on SPAC CIK; PubCo lookup failed, retry manually)
  Flags:      DEADLINE 4/20
  Thesis:     No memory doc exists for CDAQF.
  Tickers:    {CDAWF US Equity} [CDAWF]

- {PELI US Equity} [PELI] (S-1 priced): IPO priced at $10.00, $200mm raise.
  Position:   C: 200K / W: 0 / R: N/A | U=S+W/2 | SO: 25.0M | 9.9%: 2.5M
  Profile:    B2 General | Dom: DE | UW BTIG
  Pricing:    [PELI] $9.98 (mid) | [PELIW] $0.30 | C-T: -$0.02
  Trust:      CIT $10.00
  IPO:        4/15/26 | proceeds $200mm
  Dates:      est. 1/15/28 | deadline 4/15/28
  Thesis:     First-time sponsor backed by [HF name]; B2 placement reflects clean sheet but unproven mandate. Tracker positioning at $10.00 while we monitor for opportunistic adds at -2c. Pass on adds above NAV.
  Memory:     entry logged + bullet in Recent Headlines
  Tickers:    {PELIW US Equity} [PELIW]

- {AACP US Equity} [AACP]: S-1 filed, $250M IPO. NOT IN BOOK. Monitor for allocation.

- {HIMS US Equity} [HIMS]: +47% pre-mkt on Novo obesity deal. Not SPAC.
```

**Notes on the examples:**
- VCIC, DMAA, CDAQF, and PELI all show the simplified post-yields layout — Pricing line carries C-T spread, no Yields grid, no Extensions line.
- VCIC, DMAA, CDAQF render `s/f-4s:` on the Filing line (ALL in-deal headlined names get this). VCIC: 2 (base S-4 + 1 amendment, SPAC CIK). DMAA: 3 (base + 2 amendments, SPAC CIK). CDAQF: 0 with Pass 3 attempted and PubCo CIK lookup failed — flagged for manual retry.
- PELI is pre-deal → NO `s/f-4s:` segment (rule: ALL in-deal headlined names get the segment; pre-deal does not).
- VCIC has WORKING orders → Orders line rendered. DMAA, CDAQF, PELI have no working orders → Orders line OMITTED.
- CDAQF is illiquid (no Bloomberg trade) → Pricing shows `no trade` for common and `C-T: N/A`. With yields removed, this no longer requires a separate "bid/ask not available" line.
- PELI is pre-deal → no Deal line, no Outside Date in Dates line, Trust line shows CIT only (no balance for pre-deal), and IPO line carries the proceeds segment.
- VCIC, DMAA, PELI render the `Memory:` line because docs exist (Step 2c Case 1). VCIC has deeper edits (Key Dates updated) because the vote date is new in the headline; DMAA and PELI render the floor-only form (entry + bullet). CDAQF renders `Thesis: No memory doc exists for CDAQF.` and OMITS the `Memory:` line entirely — no doc means nothing to patch.

**Actionable flags (ALL CAPS, comma-separated on the `Flags:` line):**
- VOTE M/D — Vote date within 30 days
- DEADLINE M/D — Deadline within 14 days
- LARGE POSITION — Common position > 40% of 9.9% threshold
- NEW DEAL — Just-announced business combination
- NO POSITION — We have zero exposure across all instruments
- NOT IN BOOK — Ticker not found in our tracking sheet
- TRUST DELTA — Headline trust differs from model by > $0.02
- SPLIT PENDING — Units splitting, position tracking update needed

### Step 6: Summary Line and Footer

After all the individual ticker blocks, add a separator line and a summary line at the bottom:

```
---
X names with position, Y without. Actions: [votes to submit, splits to track, book updates needed]
```

### Step 7: Patch Existing Memory Docs (Existing Docs Only — No Creation)

After the output file is written and presented, patch memory docs for every ticker addressed in the run where a memory doc ALREADY EXISTS. This keeps memory docs in sync with the morning headline events so that the next time a name comes up, the exec summary already reflects the latest state — without a reader having to scan the chronological entries log to reconstruct it.

**Coordination with Step 5 (`Memory:` line):** The `Memory:` line in each ticker block is the announcement of what Step 7 will patch. Compose the Memory line content in Step 5 by deciding ahead of time what the patch will be (floor only, or floor + deeper edits, or floor + thesis touch). Step 7 then executes that plan. If the planned patch fails at execution time, log the failure in chat — the file is already on Walter's screen with the announced intent, so the failure mode is "promised X but tool returned error Y" rather than silent inconsistency.

**No tool call budget for this step.** It may span multiple turns if needed. Patches are independent per-ticker; do not compress them at the cost of completeness. If the turn is getting long, finish the current ticker cleanly and continue patching in the next turn.

**Eligibility:**
- ONLY patch docs that EXIST. Step 2c (`read-memory-doc`) results identify which tickers have docs (Case 1) vs. which do not (Case 2 `not_found`).
- For `not_found` tickers — DO NOTHING. **This skill never creates new memory docs**, even when the headline event is obviously material. Doc creation is the responsibility of `seed-memory`, not headlines.
- For tickers without Step 2c reads (NOT IN BOOK, non-SPAC, new S-1 filings) — skipped entirely.
- For tickers where Step 2c returned a tool error (Case 3) — skip Step 7 for that ticker (no doc content to anchor patches against).

**Floor — always do BOTH when the doc exists:**

**(A) Append a tagged entry to the entries log:**
```
MeteoraMCP:update-memory-doc(
  name="[TICKER]",
  author="Claude",
  tag="filing",
  body="[Headlines YYYY-MM-DD] — terse 2-4 sentence summary of the headline event. Include filing type if applicable, key dates, any model-vs-headline deltas (NAV, trust, deadline), and any immediate action implications consistent with existing doc posture. Tone: terse, concrete, directional, mirroring the doc."
)
```

The entries log is append-only — the durable raw record. Default tag is `filing`; use `trade` if the headline directly affected one of our orders (e.g., a unit split that splits an open unit order), `misc` for non-filing operational events.

**(B) Add at least one bullet to the exec summary via `patch-memory-summary`:**

The minimum-bullet rule: every headline event for an existing doc lands as at least a one-line bullet in the exec summary — even when the deeper sections of the doc are not affected by the event. This is the FLOOR. No exceptions.

The bullet lives in a "Recent Headlines" / "Recent Events" / "Key Filings / Event Chronology" / "Key Dates / Catalysts" sub-section near the top of the exec summary. Pick the existing anchor that already serves this purpose in the doc. If no such section exists in the doc, create one by anchoring on the doc's first chronological-style section (or directly on the `## Executive Summary` header as a last resort).

Bullet format: `- [M/D/YY] <one-line headline summary, including filing type if applicable>`.

**Ceiling — also patch deeper sections IN PLACE when the event is materially relevant:**

The bullet alone is sometimes enough. But when the headline event materially changes terms, dates, capitalization, or filing chronology that the exec summary already covers, ALSO issue targeted edits to update those specific sections so a reader returning to the doc sees the current state from the exec summary alone — without needing to read the entries log.

Sections to consider patching in place when the headline event touches them:
- **Identity / Header** — if Step 3c Pass 3 discovered a PubCo CIK that is NOT already in the doc's Identity section, patch it in (`PubCo CIK: NNNNNNN` next to the Pubco entity name). This is the durable cache that turns the next headlines run from a 2-search lookup into a zero-search hit. MANDATORY whenever Pass 3 ran and produced a CIK that wasn't already cached.
- **Key Dates / Catalysts** — new vote date, redemption deadline, outside date, unit split date, lock-up expiration. REPLACE superseded dates rather than appending "UPDATE:" notes.
- **Deal Terms / Structure** — BCA amendment substance (lockup changes, valuation changes, MCC, structure changes). Rewrite the affected paragraph in place.
- **Cap Structure** — material capitalization changes (PIPE upsize/downsize, new convert, sponsor share forfeiture, NRA, FPA, sponsor sale). Update the relevant cap stack lines.
- **Filing Chronology / F-4 Timeline** — if the doc maintains a chronological filings list, append the new filing in date order. For FPI deals, surface the EDGAR-verified count line at the TOP of the F-4 Timeline section (`**EDGAR-verified count: s/f-4s = N** (...) on PubCo CIK NNNNNNN`) so the next run sees it immediately on summary read.
- **Current Posture / Trade View / Live Orders** — only if the headline actually changes what we'd do (new level triggers, GTC adjustments, action implications). Otherwise leave alone.

**Thesis-touching rule (NARROW):**
- DO NOT touch the core thesis (sections like "Core Thesis", "Verdict block", "Tape / Sponsor / Structure / Base rate / Rec", "Recommendation", "REC", "Thesis") unless the headline materially shifts the directional view.
- Material thesis change examples: target swap; sponsor change or sponsor sale to a different tier; PIPE termination; deal termination; going-concern flag; fraud disclosure; deal vote outcome (pass/fail); failed BCA; FPA termination; CEO/CFO resignation; restatement.
- Non-material to thesis examples: yet-another S-4/F-4 amendment in an ongoing review cycle; routine monthly extension deposit; expected vote date scheduling; routine 10-K/10-Q; promotional 425 cadence; routine trust confirmation that matches model.

**"More than a bullet" principle (Walter):**
A reader returning to the doc next week must reconstruct the current state from the exec summary alone — without reading entries chronologically. Means:
- When dates change, REPLACE the old date in place — don't append "UPDATE:" lines.
- When terms change, REWRITE the affected paragraph in place rather than appending an addendum.
- When the dates list grows, keep it chronological and remove or strike superseded dates.
- The minimum-bullet rule is the FLOOR, not the CEILING — always do at least a bullet, but do more whenever the event genuinely shifted something already in the doc.

**Batching edits:**
When a single headline event produces multiple discrete edits to one doc (e.g., a bullet add + a date update + a cap structure rewrite), batch them all into a SINGLE `patch-memory-summary` call via the `edits` array. The tool applies edits sequentially in one transaction — if any one edit fails, the whole patch aborts cleanly.

**Failure handling:**
- If `update-memory-doc` fails (network, validation) — note in chat, continue with `patch-memory-summary`.
- If `patch-memory-summary` fails (old_str not found / not unique) — re-read the doc to confirm the exact anchor text, retry once with corrected `old_str`. If retry fails, log the failure in chat and move to the next ticker.
- If the tunnel is down (multiple consecutive tool failures across tickers) — log it in chat, stop Step 7, do not retry the whole batch.

---

## Tool Usage Reference

### spac-details (internal book) — 2 bulk calls, no fallbacks
```
spac-details(stage="indeal")     # Bulk pull 1: ALL in-deal SPACs (no position filter)
spac-details(stage="predeal")    # Bulk pull 2: ALL pre-deal SPACs (no position filter)
```
**Strategy:** The two unfiltered bulk pulls return the complete book. Headline tickers are matched against the cache. If a ticker is not in either result set, it is NOT IN BOOK — no individual `spac-details(ticker=...)` fallback needed. **Note:** The predeal pull frequently exceeds context limits and gets stored as a file — see "Handling oversized results" in Step 2 above for the grep/python extraction pattern.

### edgar-filings (SEC filings list) — 1 call per in-deal ticker (+ optional Pass 2 / Pass 3 backups)
```
edgar-filings(ticker="VCIC", limit=50)             # Pass 1 — single deep pull; scan for DEFM14A, PREM14A, 424B3, 424B4, 8-K, AND S-4/S-4/A/F-4/F-4/A
edgar-filings(ticker="VCIC", form_type="S-4", limit=10)   # Pass 2 — conditional backup ONLY when limit=50 returns zero S-4/F-4 AND deal_announced is >60 days ago
edgar-filings(cik="2097725", limit=20)             # Pass 3 — PubCo CIK lookup for FPI deals where Passes 1+2 returned zero; CIK resolved from memory doc cache OR web search
```
**Strategy:** Pass 1 (one call with limit=50) replaces the old multi-call proxy cascade AND serves double-duty as the first scan of the 3-pass S-4/F-4 count workflow (Step 3c). Scan the returned list for proxy-type filings (DEFM14A > 424B3/424B4 > PREM14A) AND for S-4/S-4/A/F-4/F-4/A counts. Run the targeted `form_type="S-4"` (Pass 2, and optionally `"F-4"`) backup ONLY when the limit=50 scan returns zero S-4/F-4 and the deal is >60 days old. Cap Pass 2 at 2 calls per in-deal name. **Run Pass 3 (PubCo CIK lookup) inline when Passes 1+2 return zero and the deal looks FPI** — check the memory doc summary first for a cached `PubCo CIK: NNNNNNN`; only web-search if not cached. Step 7 patches the discovered CIK back into the memory doc's Identity section so the next run is a cache hit.

### edgar-filing-text (read filing content)
```
edgar-filing-text(accession_number="...", ticker="...", summary=true)           # TOC — check titles for vote date first!
edgar-filing-text(accession_number="...", ticker="...", offset=X, max_chars=Y)  # Read section (only if TOC title doesn't contain date)
```
**Optimization:** When calling summary=true, check if the vote date is already visible in a TOC section title (e.g., `"NOTICE OF EXTRAORDINARY GENERAL MEETING TO BE HELD ON MARCH 12, 2026"`). If yes, extract the date directly — do NOT make an additional call to read the subsection.

### web_search
- For non-SPAC tickers and context
- For new S-1s not yet in our book
- For deal details not in EDGAR (press releases)

### get-price (Bloomberg bid / ask / last)
```
get-price(
  tickers=["PELI US Equity", "VCIC US Equity", "HYAC US Equity", ...],
  fields=["BID", "ASK", "PX_LAST"],
  period="5d"
)
```
**Batch efficiently:** Pass all SPAC tickers (common, warrant, rights, unit) in a single call. The displayed Pricing line uses the live mid `(bid + ask) / 2` and feeds the C-T spread. Use `period="5d"` to get the most recent trading day. For unit tickers that haven't split, use the unit format (e.g., `"FGIIU US Equity"`, `"GLED/U US Equity"`). Some illiquid SPACs may return no data — report `[TICKER] no trade | C-T: N/A` for those.

### read-memory-doc (Meteora Executive Summary — for Thesis line)
```
MeteoraMCP:read-memory-doc(name="VCIC", summary_only=true)
```
**Strategy:** One call per ticker in our book (in-deal AND pre-deal). Pass the BASE common ticker (no W/R/U suffix). Distill the returned Executive Summary into 3 sentences per Section 7. If the doc is missing, render `Thesis: No memory doc exists for [TICKER].` — never synthesize from `notes`, `recommendation`, filings, or first principles.

### emsx-blotter (Working Orders — for Orders line)
```
MeteoraMCP:emsx-blotter(ticker="VCIC")
```
**Strategy:** One call per ticker in our book. Pass the BASE common ticker — the blotter returns orders across all related instruments (common, warrant, rights, units) automatically. Filter for `status="WORKING"` only. Render an `Orders:` line per Section 8 ONLY if at least one working order exists across any instrument; omit the line entirely otherwise. Skip blotter calls for NOT IN BOOK tickers, non-SPAC tickers, and new S-1s.

### update-memory-doc (Step 7 — entries log append)
```
MeteoraMCP:update-memory-doc(name="VCIC", author="Claude", tag="filing", body="[Headlines YYYY-MM-DD] — ...")
```
**Strategy:** Step 7 only. One call per ticker with an EXISTING memory doc (per Step 2c Case 1). Default tag is `filing`; use `trade` if the event directly affected one of our open orders, `misc` for non-filing operational events. Never invoked for `not_found` docs — this skill does not create memory docs.

### patch-memory-summary (Step 7 — exec summary edits)
```
MeteoraMCP:patch-memory-summary(name="VCIC", edits=[{"old_str": "...", "new_str": "..."}, ...])
```
**Strategy:** Step 7 only. One call per ticker with an EXISTING memory doc. The FLOOR is at least one bullet added to a "Recent Headlines" / "Key Filings / Event Chronology" / equivalent section. Batch all per-ticker edits (bullet add + date update + term rewrite) into a single call via the `edits` array — they apply sequentially in one transaction. NEVER touch the core thesis section unless the headline materially shifts the directional view (see Step 7 thesis-touching rule).

---

## Edge Cases

### Ticker Not Found in Bulk Pulls
1. Strip suffixes (W, R, U, /WS, /U, /R) and check again against cached results
2. If still not found → NOT IN BOOK. No individual spac-details fallback — the unfiltered bulk pulls are the complete book.
3. For non-SPAC tickers or new S-1 filings, web search for context

### Multiple Events per Ticker
Combine into a single bullet covering all events for that ticker.

### Non-SPAC Tickers
Quick web search, 1 line of context. Note any indirect SPAC relevance (former deSPAC, sector read-through).

### Unit Splits
Note which instruments begin separate trading. Flag if we hold units that need position tracking update.

### New S-1 Filings
Web search for: sponsor name, IPO size, sector focus, underwriter, warrant structure.

### Data Quality Issues
- If `pct_9_outstanding` is `#N/A` or 0, report "9.9%: N/A" and still report position sizes in absolute terms
- If `common_outstanding` is 0, null, or `#N/A`, report "SO: N/A"
- If `warrants_in_unit` or `rights_in_unit` is "None", omit that term from the inline `U=...` notation per Section 1
- If `cash_in_trust` is `#N/A`, render `CIT N/A` on the Trust line and `C-T: N/A` on the Pricing line
- If `domicile`, `underwriter`, or `pipe_size` are missing, OMIT that segment from the line (do not render a placeholder); the rest of the line still renders
- If `ipo_date` is missing, render `IPO: n/a`
- If `trust_balance` is missing for an in-deal SPAC, render `Trust: CIT $X.XX` (CIT only, no balance segment); do not invent a balance from `trust_balance_per_share × common_outstanding`
- If `target` or `deal_announced` is missing for an in-deal SPAC, OMIT that segment from the Deal line (do not drop the entire line); render `Deal: PIPE $XXmm` if PIPE is the only field available
- If `outside_date` is missing for an in-deal SPAC, OMIT the outside segment from the Dates line (don't render `n/a` — outside is optional)
- If `est_date` is missing, render `est. n/a` in the Dates line
- If Bloomberg returns no bid/ask for a ticker, render `[TICKER] no trade` on the Pricing line for that instrument and `C-T: N/A` if it's the common
- If `emsx-blotter` returns an error, render `Orders: ⚠ blotter fetch failed` once and proceed; do not retry within the session

---

## Quality Checks

Before finalizing:

1. **Completeness:** Every ticker from input is addressed (none missed).

2. **Position line correct:** Every block for a SPAC in our book has the line `Position: C: X / W: Y / R: Z | U=S+W/n+R/m | SO: AM | 9.9%: BM`. The N/A vs. 0 distinction is preserved (warrant_ticker null → `W: N/A`; warrant_ticker valid + zero position → `W: 0`). If `units_position > 0`, append ` | U: WK`. If `common_outstanding` is 0/null/`#N/A`, render `SO: N/A`. If `pct_9_outstanding` is 0/null/`#N/A`, render `9.9%: N/A`.

3. **Unit notation in trading-note style:** Use `U=S+W/n+R/m`, `U=S+W/n`, `U=S+R/m`, or `U=S` per Section 1. Do NOT use the legacy `Unit: W ... / R ...` format.

4. **Profile line correct:** `Profile: B[N] [Category] | Dom: XX | UW [underwriter]`. Bucket from `bucket` (in-deal) or `quality_bucket` (pre-deal). Domicile from `domicile` field; OMIT segment if missing. UW from `underwriter`; OMIT segment if missing.

5. **Pricing line correct (MANDATORY):** Every block for a SPAC in our book has `Pricing: [TICKER] $X.XX (mid) | [TICKERW] $X.XX | [TICKERR] $X.XX | C-T: $X.XX`. Common mid from Bloomberg `(bid+ask)/2`; if no data, render `[TICKER] no trade`. Warrant and rights segments rendered ONLY if their tickers exist in spac-details AND Bloomberg returned a price. C-T from `mid − cash_in_trust`, signed; if mid is missing, render `C-T: N/A`.

6. **Trust line correct:**
   - In-deal: `Trust: $XXXmm | CIT $X.XX` — both `trust_balance` and `cash_in_trust` rendered. If `trust_balance` missing, render `Trust: CIT $X.XX` (CIT only).
   - Pre-deal: `Trust: CIT $X.XX` — CIT only (no balance for pre-deal in spac-details).

7. **IPO line correct:** `IPO: M/D/YY | proceeds $XXmm`. IPO date from `ipo_date`. Proceeds segment ONLY for pre-deal (from `ipo_proceeds`); OMIT for in-deal. If `ipo_date` missing, render `IPO: n/a`.

8. **Deal line correct (in-deal only):** `Deal: Target: TargetCo | announced M/D/YY | PIPE $XXmm (per spac-insider)`. Target from `target` field (strip embedded "Announced: " prefix). Announced from `deal_announced`. PIPE from `pipe_size` per the rendering rules in Step 5 / per the trading-note PIPE spec — always include `(per spac-insider)` disclaimer. **OMIT entire line for pre-deal SPACs.**

9. **Dates line correct:** `Dates: est. M/D/YY | deadline M/D/YY | outside M/D/YY`. Use `n/a` for missing fields, never drop the line. **Outside Date segment in-deal only** — OMIT for pre-deal.

10. **Thesis line (MANDATORY):** Every block for a SPAC in our book has a `Thesis:` line per Section 7. Three sentences distilled from `MeteoraMCP:read-memory-doc(name=TICKER, summary_only=true)`, using the stage-bifurcated framework. If the doc is missing → `Thesis: No memory doc exists for [TICKER].`. If fetch fails → `Thesis: Memory doc fetch failed — retry or check manually.`. **NEVER synthesize from forbidden sources** (`spac_details.notes`, `spac_details.recommendation`, header data, web search, first principles). Never drop the line.

11. **Orders line correct (conditional):** Per Section 8 — `emsx-blotter` called for every ticker in our book. Render `Orders:` line ONLY if at least one WORKING order exists across any instrument (common, warrant, rights, units). Format: `[SIDE] [size] [ticker] @ [limit] [duration]`, separated by ` | `. SELL block before BUY block; ascending limit price within each side. OMIT line entirely if no working orders. Equity uses k notation; option/warrant/rights uses raw integer contract counts.

12. **Trust comparison:** Headline trust vs. model trust noted on the `Filing:` line where applicable.

13. **Filings pulled:** All in-deal names mentioned in headlines have had `edgar-filings(limit=50)` called and the results scanned for both proxy filings AND S-4/F-4/S-4/A/F-4/A counts. For ALL in-deal headlined names where the limit=50 scan returns zero S-4/F-4 AND `deal_announced` is >60 days ago, the targeted `form_type="S-4"` backup call has been made (and `form_type="F-4"` if the deal looks FPI). For ALL in-deal headlined FPI names where Passes 1+2 returned zero, Pass 3 (PubCo CIK lookup) has been run — memory doc checked first for a cached `PubCo CIK: NNNNNNN`, then web search if not cached, then `edgar-filings(cik=PUBCO_CIK, limit=20)`.

14. **Vote Date Extraction (CRITICAL):** For EVERY in-deal SPAC where we hold a position, the limit=50 filing list was scanned for DEFM14A, 424B3, 424B4, and PREM14A. If ANY proxy-type filing was found, it was read for the vote date. TOC section titles checked FIRST (vote date is often embedded directly in the title — extract without an extra subsection read).

15. **Vote / Deadline flags:** Any vote within 30 days is on the `Flags:` line. Any deadline within 14 days is on the `Flags:` line.

16. **No fabrication:** Fields that are 0, null, or `#N/A` are reported accurately, not invented or filled in from elsewhere.

17. **Parenthetical scope:** The parenthetical after each ticker describes ONLY the news event from the headlines. The target name and deal status appear on the `Deal:` line (in-deal) or `Filing:` line, NOT in the parenthetical.

18. **File output:** Output is written to `/mnt/user-data/outputs/spac_headlines_YYYY-MM-DD.txt` and presented via `present_files`. NO markdown — just plain text with `-` bullets, 2-space indent for sub-lines, blank line between ticker blocks. Pastes cleanly into Bloomberg chat.

19. **Bloomberg ticker formatting:** First mention of each common ticker uses `{TICKER US Equity} [TICKER]` dual format. The final `Tickers:` line for SPACs in our book uses the same dual format for warrant and/or rights tickers. Line is OMITTED entirely if neither warrant nor rights ticker exists.

20. **N/A vs. 0 distinction:** "N/A" = security does not exist (warrant_ticker or rights_ticker is 0/null in spac-details). "0" = security exists, we hold none. Never confuse these.

21. **No yields rendered:** Headlines does NOT compute or render live yields. The Yields grid, Extensions line, and yields footer were removed because the calculation took too long (USGG3M batching + per-eligible-ticker 8-K extraction with follow-up filing-text reads) and was inconsistently accurate. If yields are needed on a specific name, run `trading-note-simple` (T-bill only) or `trading-note-extended` (with extension deposits). The full prior spec is preserved at `references/SKILL_with_yields.md` inside this skill bundle.

22. **S-4/F-4 count rendered (ALL in-deal headlined names):** Every in-deal SPAC mentioned in headlines has an `s/f-4s: N (EDGAR)` segment appended to the `Filing:` line, derived per Step 3c (full 3-pass workflow: limit=50 scan reuse + conditional targeted backup + conditional PubCo CIK lookup). The count NEVER comes from `spac_details.s4_amendments` (that field is bugged) — only from EDGAR. For pre-deal SPACs, NOT IN BOOK, and non-SPAC tickers, the `s/f-4s:` segment is OMITTED (S-4 cadence isn't relevant outside an active business combination). When Pass 3 (PubCo CIK) returned the count, the segment includes the PubCo CIK: `s/f-4s: N (EDGAR — PubCo CIK NNNNNNN)`. When Pass 3 was triggered but no PubCo CIK could be resolved, the segment reads: `s/f-4s: 0 (EDGAR — none on SPAC CIK; PubCo lookup failed, retry manually)`.

23. **Memory docs patched (existing docs only — Step 7):** For every ticker addressed in the run where a memory doc EXISTS (Step 2c Case 1), Step 7 has been executed. Minimum: one `update-memory-doc` call (entries log append) AND one `patch-memory-summary` call (at least one bullet added to a "Recent Headlines" / equivalent section of the exec summary). Deeper section patches (key dates replaced in place, deal terms rewritten, cap structure updated, filing chronology appended) done WHEN the event materially changes terms/dates/cap/chronology already in the summary. Thesis sections (Core Thesis, Verdict block, Rec, etc.) UNTOUCHED unless the headline materially shifted the directional view. No new docs created — `not_found` tickers are skipped entirely (doc creation belongs to `seed-memory`). Failures logged in chat and skipped past. This step has no tool call budget and may span multiple turns.

24. **Memory line rendered (existing docs only):** Every ticker block where a memory doc EXISTS (Step 2c Case 1) has a `Memory:` line below `Thesis:` and above `Tickers:`, summarizing in one line what Step 7 will patch. Floor form: `Memory: entry logged + bullet in [section name]`. Deeper form: `Memory: entry logged + bullet + [section names] updated ([reason])`. Thesis-touch form (rare): `Memory: entry logged + bullet + [section] + thesis updated ([what shifted])`. The Memory line is OMITTED for tickers where the doc is `not_found` (Case 2), where Step 2c errored (Case 3), where the ticker is NOT IN BOOK, or where the ticker is non-SPAC. The Memory line text matches the patch Step 7 actually executes — no announcing edits that won't be made.
