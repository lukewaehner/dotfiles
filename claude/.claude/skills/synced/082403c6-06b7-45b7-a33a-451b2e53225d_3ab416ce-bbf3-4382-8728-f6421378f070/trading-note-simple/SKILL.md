---
name: trading-note-simple
description: >
  Generate a formatted SPAC trading note with live-recomputed yields (Bloomberg mid + USGG3M, gross T-bill accrual, no extensions or leakage), a VWAP-centered yield matrix (±1c/±2c/±3c plus bid/ask), an EDGAR-verified S-4/F-4 count (3-pass: SPAC CIK + PubCo CIK) for in-deal names, and a `Thesis:` line pulled from the Meteora memory doc. Trigger on 'simple note', 'short note', 'trading note', 'note for [ticker]', 'snip', 'clipboard note', 'position note', 'what does [ticker] look like', or any request for a SPAC position snapshot. Unit renders inline as `U=S+W/2+R/10` or `U=S`. Always use this skill for simple trading notes — do not produce them ad hoc. For extension-deposit modeling, use `trading-note-extended`.
---

# Trading Note — Simple Variant

Generate formatted SPAC position notes with:
- Live Bloomberg prices and live-recomputed yields (gross T-bill accrual only — no leakage, no extension deposits)
- Inline unit-structure notation (`U=S+W/2+R/10` or `U=S`) placed near positions
- A VWAP-centered yield matrix showing yield at ±1c/±2c/±3c price steps plus live bid/ask
- An **EDGAR-verified S-4/F-4 amendment count** (3-pass workflow; sheet value ignored) for in-deal SPACs
- A 3–4 sentence thesis block distilled from the Meteora memory doc (bifurcated pre-deal vs in-deal framework) or a "no memory doc" flag, placed inside the code block, directly above the `---` that precedes ORDERS
- **EDGAR-verified `s/f-4s` count** for in-deal names (3-pass workflow — see "S-4/F-4 Verification" below). Sheet `s4_amendments` ignored.
- Live EMSX orders appended

For extension-deposit modeling and EDGAR-verified S-4/F-4 counts, use `trading-note-extended`.

## Workflow

1. Call `MeteoraMCP:spac-details` with the requested ticker to get positions, trust data, deadlines, scenario dates, `vwap_5d`, and the correct warrant/rights tickers.
2. In parallel with step 1 if possible:
   - `MeteoraMCP:emsx-blotter` with `ticker` set to the base ticker.
   - `MeteoraMCP:get-price` with `tickers` set to a batch containing **all valid security tickers** (common, warrant, rights) **plus `"USGG3M Index"`** for the T-bill rate. Single batched call.
   - `MeteoraMCP:read-memory-doc` with `name` set to the base ticker and `summary_only=true`. See "Thesis Block" below for how to handle the response.
3. Determine `stage` from the spac-details response (`predeal` or `indeal`).
4. **EDGAR S-4/F-4 verification** (in-deal only — skip for pre-deal):
   - Run the 3-pass registration-statement workflow (see "S-4/F-4 Verification" below).
   - Produce an **amendment count** sourced from EDGAR. **Do NOT use `s4_amendments` from the sheet** — that field is unreliable.
5. Extract live common bid/ask/mid, warrant mid, rights mid from the Bloomberg response. Extract T-bill rate as `USGG3M Index.price / 100`.
6. Recompute `C-T = bbg_common_mid − cash_in_trust` (signed).
7. **Compute yields** at each (price × scenario date) combination needed for the matrix — see "Yield Formula" and "Yield Matrix" below. The 5-line EST/6MON/9MON/12MON/MAX schedule is NOT rendered in the main note anymore — yields live exclusively in the matrix.
8. **Build the VWAP-centered yield matrix** (see "Yield Matrix" below).
9. **Distill the thesis block** from the memory doc summary — see "Thesis Block" below.
10. Assemble the note using the appropriate template. In-deal notes include `s/f-4s: [EDGAR count]` — **explicitly labeled as EDGAR-verified, NOT from the sheet**. **Insert the thesis block directly above the `---` that precedes ORDERS.**
11. Append the ORDERS section.
12. Output the note inline as a fenced code block, followed by the yield matrix as a second fenced block, followed by the footer line.
13. For batch requests: one note per ticker, separated by a blank line and `---`. Use a single batched `get-price` call covering all tickers across all SPACs plus `"USGG3M Index"`. Memory-doc reads and EDGAR verification are per-ticker (not batchable) — one `read-memory-doc` call and one EDGAR

Prices come from Bloomberg via `MeteoraMCP:get-price`. Sheet `common_price` / `warrants_price` / `rights_price` are fallback only.

### Price selection

For common: use `mid` as authoritative (`(bid+ask)/2`). Also extract `bid` and `ask` separately — they go into the yield matrix. Fall back to `last_trade` only if mid is unavailable AND `last_trade_time` is recent; otherwise fall back to the sheet price.

For warrant/rights: use `mid`. Fall back to sheet price, then suppress if both unavailable.

### Ticker format rules

- **Common**: pass as-is (`FCRS`, `BACQ`, `KDK`).
- **Warrant**:
  - If it contains a slash (`FCRS/WS`, `BACQ/WS`, `LEGT/WS`), pass with ` US Equity` suffix: `FCRS/WS US Equity`.
  - If plain alphanumeric (`KDKRW`, `OPTXW`), pass as-is.
- **Rights**: plain, pass as-is.
- Skip if ticker is 0, null, empty, or starts with `#N/A`.
- **Always include `"USGG3M Index"` in the batch.**

### T-bill rate

`USGG3M Index` returns the yield as a whole-number percentage (e.g., `4.32` = 4.32%). Divide by 100 for the decimal rate. If it fails to resolve, fall back to 3.66% and flag in the footer.

---

## S-4/F-4 Verification (EDGAR, 3-Pass — In-Deal Only)

The sheet's `s4_amendments` field is systematically unreliable. For in-deal SPACs, always re-derive the count from EDGAR using the full 3-pass workflow. The goal is a **count of registration-statement filings on record** (public S-4/F-4 plus amendments; DRS counted separately when present).

### Pass 1 — Broad listing on the SPAC's CIK
```
edgar-filings(ticker="[TICKER]", limit=30)
```
Scan for any S-4, S-4/A, F-4, F-4/A, DRS, DRS/A.

### Pass 2 — Targeted registration-statement filter on the SPAC's CIK
Always run these even if pass 1 looked complete:
```
edgar-filings(ticker="[TICKER]", form_type="S-4", limit=10)
edgar-filings(ticker="[TICKER]", form_type="S-4/A", limit=10)
edgar-filings(ticker="[TICKER]", form_type="F-4", limit=10)
edgar-filings(ticker="[TICKER]", form_type="F-4/A", limit=10)
edgar-filings(ticker="[TICKER]", form_type="DRS", limit=10)
edgar-filings(ticker="[TICKER]", form_type="DRS/A", limit=10)
```

### Pass 3 — Locate the off-CIK PubCo (FPI / Delaware-PubCo structures)

Run if ANY of these apply:
- Target is non-US (Cayman, BVI, UK, Israel, China, etc.) or domicile suggests an FPI deal.
- Passes 1–2 returned zero registration statements despite `deal_announced` being >60 days ago.

The SPAC's CIK won't have the S-4 because a separately-incorporated Delaware PubCo (e.g., "[Sponsor] Merger Corporation", "[Target] Holdings Inc.") is the registrant. Your job: find that PubCo's CIK, then call `edgar-filings(cik="[PUBCO_CIK]")`.

**Step 3a — Extract the PubCo's exact legal name.** It's already in hand — read the Pass 1 filings list, pick the deal-announcement 8-K's Exhibit 2.1 (the BCA / Agreement and Plan of Merger), and grab the name from its preamble. Don't search the web for the PubCo name; it's a free lookup from a filing you already have. Names look like `"D. Boral ARC Merger Corporation"`, `"Exascale Labs Holdings Inc."`, etc.

**Step 3b — Search the web for the CIK, with fetchable URLs only.** Use this query shape:

```
web_search: "[PubCo full legal name]" S-4 site:sec.gov
web_search: "[PubCo full legal name]" stocktitan OR spacresearch
```

What is fetchable from this environment (and what isn't):

| URL pattern | Fetchable? | Use for |
|---|---|---|
| `sec.gov/Archives/edgar/data/[CIK]/...` | ✓ | The CIK is right there in the path — read it off the URL, no fetch needed |
| `stocktitan.net/sec-filings/[TICKER]/...` | ✓ | Aggregator pages mirror SEC filings; CIK often in page content |
| `spacresearch.com`, `justia.com`, `prnewswire.com`, news sites | ✓ | Confirmatory only |
| `efts.sec.gov/LATEST/search-index?...` | ✗ | SEC's full-text search backend — **not fetchable from here, don't try** |
| `sec.gov/cgi-bin/browse-edgar?...` | ✗ | EDGAR's company browser — **not fetchable from here, don't try** |

The CIK is the digit string in any `sec.gov/Archives/edgar/data/[DIGITS]/` URL the search returns. Pull it directly from the URL — no fetch required to read a CIK. Then call `edgar-filings(cik="[CIK]", limit=20)` and count S-4 / S-4/A / F-4 / F-4/A normally.

**Step 3c — If no `/data/[CIK]/` URL surfaces.** Two well-shaped searches that return no SEC archive URL means the PubCo's filings simply haven't been indexed yet (common in the first days after filing) or the name has a variant. Try one alternative spelling (drop punctuation, vary "Inc." vs "Corporation") and one more search. If still nothing, render:

```
... s/f-4s: unverified (EDGAR — PubCo CIK not located via web)
```

…and add a footer flag: `⚠ PubCo S-4 filing not confirmable via EDGAR — verify manually`. This is the honest output; do NOT guess `0` or `1` when you couldn't confirm — that's a different signal than "checked and not filed yet."

**Anti-pattern — don't waste calls on:**
- Fetching `efts.sec.gov` or `sec.gov/cgi-bin` — they return permission errors here.
- Generic re-queries of the same phrase ("PubCo CIK", "SEC EDGAR PubCo S-4") — they hit the same press-release pool. Vary the *PubCo name spelling*, not the boilerplate around it.
- Fetching news stories that quote the BCA boilerplate — they're paraphrasing the same 8-K text you already have.

### Counting rule

Count = total number of registration-statement filings on record. The base S-4/F-4 is amendment #0 and counts as 1; each S-4/A or F-4/A adds 1.

- Base S-4 (or F-4), no amendments yet → `s/f-4s: 1 (EDGAR)`
- Base S-4 + amendment #1 → `s/f-4s: 2 (EDGAR)`
- Base S-4 + amendments #1, #2 → `s/f-4s: 3 (EDGAR)`
- **DRS and DRS/A are noted separately** (confidential draft — flag but don't aggregate with public amendments unless they have flipped public).
- No public S-4/F-4 on file after all 3 passes → `s/f-4s: 0 (EDGAR — none filed)`

### Output

In-deal template line:
```
... s/f-4s: 3 (EDGAR);
```

If the EDGAR workflow returned zero registration statements after all 3 passes:
```
... s/f-4s: 0 (EDGAR — none filed);
```

If pass 3 was not attempted because pre-conditions weren't met but the count looks suspiciously low, flag in the footer rather than silently reporting low numbers.

---

## Yield Formula

The same formula is applied to every (price × scenario date) cell in the yield matrix below. The 5-line EST/6MON/9MON/12MON/MAX schedule is NOT rendered in the main note — those scenario dates appear only as row labels in the matrix.

### Inputs

| Input | Source |
|-------|--------|
| `price` (common mid, $/share) | Bloomberg mid from `get-price` |
| `cit_today` ($/share) | `cash_in_trust` from spac-details |
| `tbill_rate` (decimal) | `USGG3M Index.price / 100` |
| `today` | current date (ET) |
| Scenario dates | `est_date`, `six_month_date`, `nine_month_date`, `twelve_month_date`, `max_date` from spac-details |

### Formula

For each scenario date `D`:

```
days_to_exit   = (D − today).days          # calendar days
trust_accrual  = cit_today × tbill_rate × days_to_exit / 365
cit_at_exit    = cit_today + trust_accrual
total_return   = cit_at_exit / price − 1
annualized     = total_return × 365 / days_to_exit   # simple annualization
```

Format: `#.##%` (two decimal places).

### Simplifications

- **No trust leakage** (taxes, WC withdrawals). Gross accrual only.
- **No extension deposits**. For that, use `trading-note-extended`.
- **Simple annualization** (×365/days), not compound.

### Edge cases

- `days_to_exit ≤ 0` → drop that scenario date entirely (don't show negative-days yields).
- Missing scenario date → drop that row from the matrix.
- `price ≤ 0` or CIT missing → render `--` in every cell of that column (or row).

---

## Yield Matrix (VWAP-centered)

Below the main note, render a table showing the annualized yield at multiple hypothetical common prices, per scenario date.

### Center selection

- **Primary**: `vwap_5d` from spac-details (the sheet's 5-day VWAP).
- **Fallback**: if `vwap_5d` is 0, null, or obviously invalid (e.g., < $1 for a SPAC), center on the live Bloomberg mid. Flag this in the matrix footer (`Centered on mid — no valid 5d VWAP`).

### Cent step computation — locked

Round the center to 2 decimals BEFORE generating column offsets. Use the rounded prices for BOTH display AND the yield formula — don't feed the unrounded VWAP into the calc:

```
center_display = round(vwap_5d, 2)     # e.g., 10.6669 → 10.67
−3c = center_display − 0.03            # 10.64
−2c = center_display − 0.02            # 10.65
−1c = center_display − 0.01            # 10.66
center = center_display                # 10.67
+1c = center_display + 0.01            # 10.68
+2c = center_display + 0.02            # 10.69
+3c = center_display + 0.03            # 10.70
```

Steps are fixed 1-cent increments. No sorting, no interleaving. Bid and Ask are always the rightmost two columns regardless of where they fall numerically relative to the grid.

### Column labels and edge cases

- Center column **label** is `VWAP` normally, or `Mid` when `vwap_5d` is invalid and we fell back to live mid.
- If bid or ask is unavailable from Bloomberg, omit that column (don't leave a blank cell). Note the omission in the header annotation: `Bid = --, Ask = $10.28`.

### Rows

One row per scenario date that passes the edge-case filter (days-to-exit > 0, date not null):

- `EST (mm/dd/yyyy)`
- `6 MON (mm/dd/yyyy)`
- `9 MON (mm/dd/yyyy)`
- `12 MON (mm/dd/yyyy)`
- `MAX (mm/dd/yyyy)`

### Coincident-date dedup

If two or more scenario rows resolve to the same exit date, collapse them into a single row with a slash-joined label. Yields would be identical anyway — duplicate rows are visual noise.

- `est_date == max_date` → label `EST/MAX (mm/dd/yyyy)`
- `est_date == six_month_date` (sponsor on a known short deadline) → `EST/6 MON (mm/dd/yyyy)`
- More than two collide → join with slashes in canonical order: `EST/6 MON/MAX (mm/dd/yyyy)`

Canonical order for slash-joining: `EST → 6 MON → 9 MON → 12 MON → MAX`. Dedup happens AFTER days-to-exit filtering, so already-dropped rows don't participate.

Common in practice: deals announced ~6 months before the original deadline often have `est_date == max_date` because no extension is needed before the vote. Both rows would show identical yields; one slash-labeled row is sufficient.

### Formula per cell

Same as the main schedule, just with the column's price:

```
yield(price, D) = ((cit_today + cit_today × tbill_rate × days_to_exit/365) / price − 1) × 365 / days_to_exit
```

Format each cell as `#.##%`.

### Layout — Markdown table (Bloomberg-pasteable)

**Output the matrix as a GitHub-flavored markdown table** with pipes (`|`) and a `|---|` separator row. This is the format that copy-pastes cleanly into Bloomberg — it lands as separate cells. Do NOT use tab-separated text, fixed-width spacing, or a fenced code block for the matrix itself.

The table has TWO header rows above the data:

1. **Row 1: column labels** — `Yield`, then the 9 fixed column labels in this exact order: `−3c, −2c, −1c, VWAP` (or `Mid`), `+1c, +2c, +3c, Bid, Ask`.
2. **Row 2: actual dollar prices** — `Price`, then each column's price: `$10.21, $10.23, $10.25, $10.27, $10.29, $10.31, $10.33, $10.26, $10.28`. These are the prices plugged into the yield formula for that column.

Then the standard markdown `|---|---|...|` separator row, then the data rows (one per scenario date).

### Example output (VWAP-centered)

Header line (plain text, above the table):

`YIELD MATRIX — centered on VWAP = $10.27, Bid = $10.26, Ask = $10.28`

Then the markdown table:

| Yield | −3c | −2c | −1c | VWAP | +1c | +2c | +3c | Bid | Ask |
|---|---|---|---|---|---|---|---|---|---|
| Price | $10.24 | $10.25 | $10.26 | $10.27 | $10.28 | $10.29 | $10.30 | $10.26 | $10.28 |
| EST (06/01/2026) | 8.85% | 7.73% | 6.61% | 5.50% | 4.40% | 3.31% | 2.23% | 7.17% | 4.40% |
| 6 MON (10/24/2026) | 5.85% | 5.20% | 4.56% | 3.92% | 3.29% | 2.66% | 2.04% | 4.88% | 3.29% |
| 9 MON (01/23/2027) | 4.61% | 4.09% | 3.57% | 3.06% | 2.56% | 2.06% | 1.56% | 3.83% | 2.56% |
| 12 MON (04/24/2027) | 3.97% | 3.53% | 3.08% | 2.64% | 2.21% | 1.78% | 1.35% | 3.30% | 2.21% |
| MAX (07/29/2027) | 3.60% | 3.20% | 2.79% | 2.40% | 2.00% | 1.61% | 1.22% | 3.00% | 2.00% |

The header annotation line stays as plain text above the table, NOT inside it.

### If `vwap_5d` is invalid (centered on mid)

Header annotation changes, and the center column's label row reads `Mid` instead of `VWAP`. Everything else is identical.

Header line: `YIELD MATRIX — centered on mid = $10.26 (no valid 5d VWAP), Bid = $10.26, Ask = $10.26`

| Yield | −3c | −2c | −1c | Mid | +1c | +2c | +3c | Bid | Ask |
|---|---|---|---|---|---|---|---|---|---|
| Price | $10.23 | $10.24 | $10.25 | $10.26 | $10.27 | $10.28 | $10.29 | $10.26 | $10.26 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

If the book is locked at the mid (bid = mid = ask), those columns all show $10.26. That's accurate data — render them anyway.

### Cell edge cases

- If bid is missing from Bloomberg, OMIT the `Bid` column entirely. Same for ask. Don't leave a blank cell — drop the whole column. Note the omission in the header annotation: `Bid = --, Ask = $10.28`.
- If a stepped price would go ≤ $0, omit that step column (rare — would only hit for sub-$1 names).
- If a scenario date has days_to_exit ≤ 0, omit that data row.
- If the matrix ends up with fewer than 2 price columns, suppress the matrix and print `Yield matrix unavailable — insufficient price data`.

### Why no yields in the main note

The main note section (pre-deal / in-deal template) does **NOT** include the EST/6 MON/9 MON/12 MON/MAX yield lines. Those live exclusively in the matrix. This avoids duplication and keeps the top-of-note compact. The scenario dates appear as row labels in the matrix; readers get the date context there.

---

## Unit Structure Notation

Placed near the positions (see Output Templates below), not at the bottom.

Format: `U=S+W/n+R/m` where `n` = warrants-per-unit denominator, `m` = rights-per-unit denominator.

### Conversion from spac-details fields

- `warrants_in_unit = "1/2"` → `W/2`
- `warrants_in_unit = "1/3"` → `W/3`
- `warrants_in_unit = "1"` → `W/1` (one full warrant per unit — render as `+W` without denominator, e.g., `U=S+W`)
- `warrants_in_unit = "1 for 3/4"` → `W*3/4` (fractional; rare — render the fraction literally)
- `warrants_in_unit = "None"` or null → omit the W term

- `rights_in_unit = "1 for 1/10"` → `R/10`
- `rights_in_unit = "1 for 1/8"` → `R/8`
- `rights_in_unit = "1/5"` → `R/5`
- `rights_in_unit = "1/7 for 1"` → `R*7` (inverse form — 7 rights make 1 share; render literally)
- `rights_in_unit = "None"` or null → omit the R term

### Rendering rules

- Both present: `U=S+W/2+R/10`
- Only warrants: `U=S+W/2`
- Only rights: `U=S+R/10`
- Neither: `U=S`

---

## Thesis Block

A short summary of the current Meteora view on the name, pulled from the memory doc. Goes **inside the note code block**, on its own line(s), directly above the `---` that separates the note body from ORDERS.

### Core principle (the guardrail)

The thesis is sourced **EXCLUSIVELY** from the Executive Summary returned by `MeteoraMCP:read-memory-doc`. No other source is permitted, ever — not the sheet `notes` field, not the sheet `recommendation` field, not spac-details headers, not filings, not sponsor identity, not first principles. If there is no memory doc, the thesis is `Thesis: No memory doc exists for [TICKER].` — full stop. The bullets below are signposts for what to look for *when distilling an existing doc*, NOT a checklist to fill in from scratch.

The header, matrix, and ORDERS section already carry CIT, structure, sponsor, UW, deadlines, yields, and our active book. A "thesis" that just relabels header data is empty. A "thesis" that quotes or paraphrases the sheet `notes` or `recommendation` field is **worse than empty** — those fields are systematically stale and re-surfacing them as "current view" is actively misleading.

### Forbidden sources (never use these for the thesis)

The following are **NEVER** valid sources for any sentence in the thesis line, even partially, even paraphrased:

- `spac_details.notes` — sheet free-text field. Often months out of date; may reflect a view that's been reversed.
- `spac_details.recommendation` — sheet free-text field. Stale price levels, abandoned trade ideas, or instructions that no longer match the live book are common.
- `spac_details.s4_amendments` — already flagged as unreliable elsewhere in this skill.
- The header / matrix / ORDERS content itself (re-stating CIT, yields, position size, working orders).
- Web search, EDGAR filings, or first-principles reasoning about sponsor / structure / sector.
- The user's prior conversation context unless that context is specifically a memory doc read in this same session.

If the only thing that would let you write a substantive thesis is one of the above sources, you must instead render the "no memory doc" or "fetch failed" fallback. **Synthesizing from forbidden sources is the failure mode this section exists to prevent.**

### Source

`MeteoraMCP:read-memory-doc(name="[TICKER]", summary_only=true)` — pass the base common ticker (e.g. `IPCX`, `KDK`, not `IPCXR` or `KDKRW`). This returns the Executive Summary only, which is the living two-pager on the name. **This is the ONLY permitted source.**

### Stage selection

The framework bifurcates by stage. Use the `stage` field from `spac-details` (already determined in step 3 of the workflow):
- **Pre-deal** → use the Pre-Deal framework below
- **In-deal** → use the In-Deal framework below

### Three response cases

**Case 1 — Doc exists, summary returned.**
Read the Executive Summary. Distill into **3–4 sentences** using the framework for the current stage (below). Drop a bullet if the doc doesn't speak to it — never pad with generic structural commentary to fill four slots. The output is one line of text, all sentences run together (they wrap naturally in the client).

Render as:
```
Thesis: [Sentence 1.] [Sentence 2.] [Sentence 3.] [Sentence 4 if doc supports it.]
```

**Case 2 — No memory doc exists.**
If the tool returns `status: "not_found"` or an equivalent missing-doc error, render exactly:
```
Thesis: No memory doc exists for [TICKER].
```

Do not attempt to synthesize a thesis from any other source. Specifically, do NOT pull from `spac_details.notes`, do NOT pull from `spac_details.recommendation`, do NOT generate one from sponsor identity / UW / sector / extension cadence / position size / working orders / sheet flags. The whole point of the flag is to signal that the reader should build one. **This applies even when the spac-details payload looks "rich enough" to write something** — the absence of a doc IS the information. If you find yourself reaching for `notes` or `recommendation` to "fill in" a missing doc, stop and render the fallback.

**Case 3 — Tool error (network, timeout, MCP down).**
Render:
```
Thesis: Memory doc fetch failed — retry or check manually.
```

Don't silently drop the line. The reader needs to know the thesis is unverified.

---

### Pre-Deal Framework (3–4 sentences, distilled from memory doc)

When distilling a pre-deal memory doc, look for these dimensions in priority order. Drop a bullet if the doc doesn't speak to it.

1. **Sponsor franchise read.** What the prior vehicle's outcome and team-to-team changes tell us about deal-find probability and target quality. PIPE quality on the prior vehicle (the *names*, not just the size). What the UW choice signals about deal sourcing. First-time sponsors get an explicit "no track record" prior. *Example payload: "Repeat Alussa franchise — ALUS I closed FREYR with $600M PIPE from Koch / Glencore / Fidelity blue-chip names, demonstrating real institutional PIPE-raising capability."*
2. **Structural takeaway.** What the unit economics, fee load, and sponsor-side dollars committed *imply* — not "1/2 warrant + 1/10 rights." Rather: deferred UW economics constrain deal quality at close, sponsor cash committed implies they have a target lined up, fee load forces dilutive financing, etc.
3. **Mandate / pipeline credibility.** Whether the team has a real network in the stated focus (named industry advisors, prior deals in the space, recent banker movement, specialist hires) or it's boilerplate. Specialist franchises with active networks get a positive flag; generic mandates discount. *Example payload: "Slorer joined as CEO specifically to source through his sell-side energy network — UW upgraded BTIG → Santander signaling move upmarket for PIPE origination."*
4. **Current Meteora posture.** What we're doing and the price level driving it — building common at discount-to-trust for yield-floor, working warrants/rights at a level for cheap optionality, FPA-origination posture if PIPE looks shaky. Tied to a specific price or trigger from the doc. Use EXACT thresholds, not approximations ("warrants at 30–35c are cheap optionality if pipeline is real" not "cheap warrants").

### In-Deal Framework (3–4 sentences, distilled from memory doc)

1. **Closing probability read.** MCC status (met / has credible path / load-bearing risk), PIPE structure and quality of names (committed at trust = strong; structured convert at discount = couldn't raise clean; no PIPE = MCC is harder), CoC/debt overhang. The framing: *can this deal actually close, and what does the financing tell us about how the parties got it done.*
2. **Sponsor-incentive read.** What the sponsor's economic situation (deferred UW math, WCW draws, founder-share forfeit, dollars committed to extensions, prior shell-sale economics) tells us about the playbook they'll actually run. *Canonical examples: CCIX "Klein won't walk away from $1M WCW" or SIMA "$8mm shell purchase + 1.5% deferred fee = sponsor has a target lined up."*
3. **Process / timeline read.** S-4/F-4 cadence, SEC posture, deadline gap (real runway vs. cornered), gating items (FPI complications, MAE-event termination risk, regulatory clearances). Compare to outside date. Flag extension or termination risk where load-bearing.
4. **Current Meteora posture.** Long commons for yield-to-vote / yield-to-close, working warrants/rights at a level, FPA participation, redeem-at-vote, sell-the-rights-into-pop. Tied to a specific price AND a specific trigger that would change sizing.

---

### Distillation rules (apply to both frameworks)

- **The bullets are signposts, not slots.** Use 3 sentences if the doc only speaks to 3 dimensions; use 4 if all are load-bearing. Never pad to hit 4.
- **Mirror exact thresholds from the doc.** "$10.75 × 200K GTC bid" not "build at a discount." "60c wake-up sell on warrants" not "trim on strength." Numbers are the contract between the reader and the doc.
- **Specificity test** — if the sentence could appear verbatim in another SPAC's note, it's too generic. If it requires the specific facts of *this* doc to write, it's right. "Banker-shopped first-timer with no track record" fails the test. "Dominari paid $8mm for the shell + committed 1.5% deferred UW fee" passes.
- **No verbatim copies** of large Executive Summary paragraphs. Distill into your own active-voice sentences.
- **Mirror the doc's calibration.** Don't strip out hedging ("likely", "we think", "base case", "could slip") to make the thesis sound more confident than the doc actually is.

### Tone

Walter-facing, voice of a colleague who read the doc this morning. Terse, concrete, directional. No headings, no bullets, no bold inside the rendered thesis line.

### What not to pull in

- **No raw header re-statement.** The matrix and header already carry CIT / structure / sponsor / UW / deadlines / yields. The thesis is about the *view*, not the data.
- **No verbatim Executive Summary paragraphs.** Distill.
- **No content from `spac_details.notes` or `spac_details.recommendation`.** These sheet fields are stale-prone and explicitly prohibited as thesis sources. Do not paraphrase them, do not "incorporate" them, do not use them to flesh out a thin doc. If the memory doc doesn't say it, the thesis doesn't say it.
- **No warrant arb or option detail** unless the position posture is primarily option-driven (rare for simple-note context).
- **Do not invent thresholds or triggers** not in the doc. If the doc has no explicit price or IRR threshold, state the directional view without fabricating numbers.

### Worked examples (sourced from real memory docs)

**Pre-deal (ALUB):**
> *Thesis: Repeat Alussa franchise — ALUS I closed FREYR with $600M PIPE from Koch / Glencore / Fidelity blue-chip names, demonstrating real deal-closing capability and institutional PIPE-raising; post-close target failure was execution risk, not sponsor capability. Team upgraded for ALUB II with Slorer (ex-Morgan Stanley energy MD, ex-BTIG energy IB head) joining as CEO specifically to source deals through his sell-side network, UW upgraded BTIG → Santander signaling move upmarket for PIPE origination. Long 646K commons at ~$10.03 (11c below $10.14 trust, ~4.4% YTM) plus 59K warrants for cheap pipeline optionality; warrants at 30–35c are cheap if pipeline is real, bleed to zero if sitting on trust income.*

(Three sentences — covers franchise read, mandate credibility/team upgrade, and posture. The structural-takeaway slot was dropped because the ALUB doc doesn't make it load-bearing.)

**In-deal (SIMA):**
> *Thesis: Dominari paid $8mm for the shell plus a committed 1.5% deferred UW fee — too expensive to be speculative, implying a target is already lined up. Sponsor is running a serial extension-postponement playbook (no trust contribution, no new redemption window) until announcement; base case June–July 2026 before the 7/11/26 hard liq forces a vote. Long 1,683 commons via $10.75 × 200K GTC bid for redemption-yield floor (~3.7%) plus deal-pop optionality; 200K SIMAW @ avg ~23c scaling to ~300K via $0.23 × 100K GTC for ~30c modal pop on announcement; do not pay above trust on commons or above 26c on warrants, wake-up sell at 60c.*

(Three sentences — sponsor-incentive read absorbs closing-probability read since the $8mm math IS the closing-probability evidence. Process/timeline lives in sentence 2. Posture in sentence 3 with exact bid, exact size, exact don't-pay levels.)

**In-deal (CCIX, terminated):**
> *Thesis: Deal with PlusAI terminated 4/20/26 "due to market conditions"; SPAC alive until 8/6/26 Combination Period deadline but governing docs prevent another viable extension (auto-extension already spent, re-extension requires 100% redemption opt-out which collapses trust). Klein runs the clock to capture the final 5/6/26 WCW draw ($1M) — Churchill playbook across CC-I through CC-VIII confirms sponsor will not walk away from interest entitlement. Base case: wind-down 8-K mid-July, trust distribution late Aug / early Sep at ~$10.91–10.95 vs. current $10.72, ~5.8% IRR. Long 925K commons; hold/add below $10.70 (6%+ annualized), no chase above $10.74; warrants are structurally dead paper at 66c, do not buy.*

(Four sentences — closing-probability inverted into "won't liquidate, won't re-extend," sponsor-incentive read on WCW math, timeline forecast with prices, posture with exact triggers.)

### Examples of bad thesis sentences

- "The company is a SPAC with a business combination agreement." (too generic)
- "[TICKER] presents an interesting opportunity." (empty filler)
- "Rights-only structure with no warrant coverage means dilution-on-close is direct." (re-states header; doesn't interpret it)
- "First-time sponsor with generic mandate suggests banker-shopped sourcing." (could appear verbatim in any first-time-sponsor note — fails the specificity test)
- "Rights at 22c look fairly priced as deal-probability lottery." (empty hedge with no anchor — what would change the view? at what price would we size up?)
- "Holding commons for sub-5% yield to '27 deadline." (the matrix already shows the yield by date)
- "Sheet flagged 'Bad deals, Cantor underwriter' with sheet rec C 10.41/10.50, ws 30c." (verbatim from `spac_details.notes` and `spac_details.recommendation` — explicitly forbidden sources, and these fields are systematically stale)
- "Treasury-yield play at trust; sheet rec is buy ws at 30c." (paraphrased from `recommendation` — same failure mode, hidden under different wording)
- "Real ongoing G&A burn ($175K Q2 / $383K H1 2025) so trust accrual partially offset over time." (synthesized from filings or first principles in the absence of a memory doc — even if true, this is a forbidden source for the thesis line)

If the only source available for any of these statements is the sheet `notes` / `recommendation` field or independent reasoning, render the "no memory doc" fallback instead. The reader needs to know there's no doc; manufacturing one defeats the entire signal.

---

## Data Field Mapping

Position, trust, and date fields come from `spac-details`. Prices come from `get-price` (Bloomberg). Yields are recomputed. Orders come from `emsx-blotter`. Thesis comes from `read-memory-doc`.

### Shared fields

| Field | Source | Note Usage |
|-------|--------|-----------|
| `spac_ticker` | spac-details | C Ticker |
| `warrant_ticker` | spac-details | W Ticker (suppress if 0, null, `#N/A`) |
| `rights_ticker` | spac-details | R Ticker (suppress if 0, null) |
| `common_position` | spac-details | C Position |
| `warrants_position` | spac-details | W Position |
| `rights_position` | spac-details | R Position |
| `price` (common mid) | **get-price** | C Price — fallback to sheet `common_price` if Bloomberg errors |
| `price` (warrant mid) | **get-price** | W Price — fallback to sheet, suppress if both unavailable |
| `price` (rights mid) | **get-price** | R Price — fallback to sheet, suppress if both unavailable |
| `bid` / `ask` (common) | **get-price** | Yield matrix anchor columns |
| `vwap_5d` | spac-details | Yield matrix center (fallback to mid if 0/null/invalid) |
| `warrants_in_unit` | spac-details | Unit notation (W term) |
| `rights_in_unit` | spac-details | Unit notation (R term) |
| `domicile` | spac-details | Dom / Domicile |
| `underwriter` | spac-details | UW |
| `bucket` | spac-details | Bucket |
| `category` | spac-details | Category |
| `cash_in_trust` | spac-details | CIT |
| **C-T** | **computed** | `mid − cash_in_trust`, signed |
| `common_outstanding` | spac-details | Common O/S line |
| `pct_9_outstanding` | spac-details | 9.9% value on Common O/S line |
| `est_date` / `six_month_date` / `nine_month_date` / `twelve_month_date` / `max_date` | spac-details | Yield matrix ROW LABELS (no longer rendered as 5-line schedule) |
| **All yields** | **COMPUTED** | Every cell of the yield matrix — see "Yield Formula" and "Yield Matrix" |
| `ipo_date` | spac-details | IPO Date |
| **Thesis (3–4 sentences)** | **`read-memory-doc`** | Inside the code block, above `---` / ORDERS — see "Thesis Block" |

### Pre-deal only

| Field | Note Usage |
|-------|-----------|
| `liquidation_deadline` | Liquidation Deadline |
| `ipo_proceeds` | IPO Proceeds ($mm, if available) |
| `unit_ticker` | U Ticker (if available) |
| `units_position` | U Position |

### In-deal only

| Field | Note Usage |
|-------|-----------|
| `trust_balance` | Trust balance ($mm) |
| `target` | In deal with (strip "Announced: " prefix) |
| `deal_announced` | Announced date |
| `deadline` | Deadline |
| `outside_date` | Outside Date |
| **`s/f-4s` (EDGAR-verified)** | **Replaces sheet `s4_amendments`** — computed via 3-pass EDGAR workflow |
| `pipe_size` | PIPE size ($mm) — see "PIPE line" formatting rule. Rollout field — always render with `(per spac-insider)` disclaimer |

**DO NOT use `s4_amendments` from the sheet.** That field is unreliable. The in-deal note uses only the EDGAR-verified count.

---

## Output Templates

### Pre-Deal Note

```
PRE DEAL
{TICKER US Equity} {TICKERW US Equity} {TICKERR US Equity}
C Position: #,##0; U Position: #,##0; W Position: #,##0; R Position: #,##0
Unit: U=S+W/2+R/10
[TICKER]: $#,##0.00, [TICKERR]: $#,##0.00, [TICKERW]: $#,##0.00
Domicile: XX; UW: XXXX; Bucket: X; Category: XXXX
CIT: $#,##0.00; C-T: +/-$#,##0.00
Common O/S: #,###,###; 9.9%: #,###,###
IPO Date: mm/dd/yyyy; IPO proceeds: $#,##0.00mm;
Liquidation Deadline: mm/dd/yyyy
Thesis: [sentence 1.] [sentence 2.] [sentence 3.] [optional sentence 4.]
---
ORDERS
(see ORDERS section)
```

(Then below the code block:)

Header line (plain text, above table):
`YIELD MATRIX — centered on VWAP = $X.XX, Bid = $X.XX, Ask = $X.XX`

Then the markdown table:

| Yield | −3c | −2c | −1c | VWAP | +1c | +2c | +3c | Bid | Ask |
|---|---|---|---|---|---|---|---|---|---|
| Price | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX |
| EST (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| 6 MON (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

`Yields computed @ Tbill = X.XX% (USGG3M), mid = $X.XX`

### In-Deal Note

```
IN DEAL
{TICKER US Equity} {TICKERW US Equity} {TICKERR US Equity}
C Position: #,##0; W Position: #,##0; R Position: #,##0
Unit: U=S+W/2+R/10
[TICKER]: $#,##0.00, [TICKERW]: $#,##0.00, [TICKERR]: $#,##0.00
Dom: XX; UW: XXXX; Bucket: X; Category: XXXX; s/f-4s: # (EDGAR)
Trust balance: $#,##0.00mm; CIT: $#,##0.00; C-T: +/-$#,##0.00
Common O/S: #,###,###; 9.9%: #,###,###
In deal with: TargetCo
PIPE: $#,##0[.#]mm (per spac-insider)
Announced: mm/dd/yyyy
Deadline: mm/dd/yyyy; Outside Date: mm/dd/yyyy
IPO Date: mm/dd/yyyy
Thesis: [sentence 1.] [sentence 2.] [sentence 3.] [optional sentence 4.]
---
ORDERS
(see ORDERS section)
```

(Then below the code block:)

Header line (plain text, above table):
`YIELD MATRIX — centered on VWAP = $X.XX, Bid = $X.XX, Ask = $X.XX`

Then the markdown table:

| Yield | −3c | −2c | −1c | VWAP | +1c | +2c | +3c | Bid | Ask |
|---|---|---|---|---|---|---|---|---|---|
| Price | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX |
| EST (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| 6 MON (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

`Yields computed @ Tbill = X.XX% (USGG3M), mid = $X.XX`

**CRITICAL**: The in-deal header's `s/f-4s` value comes from the EDGAR 3-pass workflow, NOT from `spac_details.s4_amendments`. Always suffix with `(EDGAR)`.

**CRITICAL**: The Unit line sits between Positions and Prices — near the positions, not at the bottom.

**CRITICAL**: The `PIPE:` line is a rollout field — sourced from `spac-details.pipe_size` and ALWAYS suffixed with `(per spac-insider)` for now (sheet field origin disclaimer). Render even when `pipe_size = 0` so the reader knows the data was checked. See "PIPE line" formatting rule.

**CRITICAL**: The `Thesis:` line sits inside the code block, on the last content line before the `---` that precedes ORDERS. If the memory doc is missing or the fetch fails, render the fallback string per the "Thesis Block" section — never drop the line entirely.

---

## Formatting Rules

### Ticker validity — the suppression rule (governs Tickers / Positions / Prices lines)

A ticker is **invalid** if its value is `0`, `null`, empty, blank, or starts with `#N/A`. Invalid means "this instrument doesn't exist for this SPAC" (e.g. ATII has no rights → `rights_ticker = 0`). When a ticker is invalid, **SUPPRESS the corresponding field on every line** — the Tickers line, the Position line, AND the Prices line. Do NOT render `N/A` for the suppressed field; just drop it. The reader infers absence from absence.

Worked example — ATII (no rights, valid warrant ticker, zero warrant position):
- Tickers: `{ATII US Equity} {ATIIW US Equity}` (no rights bracket)
- Positions: `C Position: 179,043; W Position: 0` (no R Position field)
- Prices: `[ATII]: $10.76, [ATIIW]: $1.96` (no [ATII_RIGHTS] entry)

The Position line shows `0` (not `N/A`) when the ticker is valid but the holding is zero. This is the only place `N/A`-vs-`0`-vs-suppress matters and the rule is: **invalid ticker → suppress; valid ticker + zero position → render `0`.**

### Tickers
- Wrap each valid ticker in `{TICKER US Equity}` for Bloomberg compatibility.
- See suppression rule above for invalid tickers.

### Positions
- Comma separators, no decimals: `135,532`.
- See suppression rule above. Valid-ticker / zero-position → `0`.
- Pre-deal includes U Position if a unit ticker exists; in-deal does not.

### Prices
- Source: live Bloomberg mid via `get-price`. Sheet prices are fallback.
- Format `$#,##0.00`. Standard half-up rounding for the 2-decimal display ($10.755 → $10.76). All downstream computations (yields, C-T) use the unrounded mid; only the displayed price gets rounded.
- On the price line, wrap tickers in `[TICKER]`.
- Only show entries where ticker is valid AND a price is available.

### CIT and C-T
- CIT: `$#,##0.00`.
- C-T: computed as `mid − cash_in_trust`. Prefix with `+` or `-` before the `$`: `+$0.01` or `-$0.13`. Computation uses unrounded mid; the displayed 2-decimal value is half-up rounded.

### Dom / UW / Bucket / Category line
- Render every field even if its value is null. **Null/missing → render `N/A`** for that field. Never suppress, never collapse the line. The reader needs to know the field was checked and not populated — silent suppression is indistinguishable from "the data is fine but the field was forgotten."
- Example with all four populated: `Dom: KY; UW: BTIG; Bucket: 2; Category: Quantum`
- Example with bucket/category null: `Dom: KY; UW: BTIG; Bucket: N/A; Category: N/A`

### Yield Matrix
- **Markdown table** with pipes and `|---|` separator row. NOT tab-separated, NOT fixed-width.
- Fixed column order: `Yield | −3c | −2c | −1c | VWAP` (or `Mid`) `| +1c | +2c | +3c | Bid | Ask`. No price-sorting.
- Two header rows above the data:
  1. Column labels (as above).
  2. `Price` row: actual dollar prices (`$10.27`) for each column.
- Row labels = scenario name + date: `EST (mm/dd/yyyy)`, `6 MON (...)`, etc.
- Cells formatted `#.##%`. Drop any row with days-to-exit ≤ 0 or missing date.
- See "Yield Matrix" section for full spec.

**The main note does NOT contain the 5-line EST/6MON/9MON/12MON/MAX yield schedule.** Yields live in the matrix only.

### Unit line
- Always render if either W or R has a value; `U=S` if both are None/null.
- Use slash notation `W/n`, `R/m` (see "Unit Structure Notation" above).

### Common O/S line
- Always render, on its own line directly below the CIT/C-T line.
- Format: `Common O/S: [common_outstanding]; 9.9%: [pct_9_outstanding]`
- Both values comma-separated, no decimals (e.g. `23,000,000` and `2,277,000`).
- Source: `common_outstanding` and `pct_9_outstanding` from `spac-details`.
- If either value is missing/null/zero in spac-details, render that side as `N/A` (e.g. `Common O/S: 23,000,000; 9.9%: N/A`). Do not suppress the line.

### s/f-4s field (in-deal only)
- Render from EDGAR count, suffixed `(EDGAR)`.
- If EDGAR returned zero after all 3 passes, render `0 (EDGAR — none filed)`.
- NEVER use `s4_amendments` from spac-details.

### PIPE line (in-deal only — rollout field)
- Always render on its own line, directly below `In deal with: TargetCo` and above `Announced:`.
- Source: `pipe_size` field from `spac-details` (units: $mm).
- **Always append the `(per spac-insider)` disclaimer.** This is a new line being rolled out — the disclaimer flags its provenance to the reader so they know the source for now. Do not drop the disclaimer even if the value looks correct.
- Format the dollar value compactly:
  - Whole-number millions → `$500mm`, `$100mm`, `$31mm`
  - Fractional millions ≥ 1 → one decimal, no trailing zero: `$11.5mm`, `$113.3mm`, `$20.1mm`
  - Sub-million (< 1) → two decimals: `$0.45mm`
- Render rules by value:
  - `pipe_size > 0` → `PIPE: $XXXmm (per spac-insider)`
  - `pipe_size == 0` → `PIPE: None disclosed (per spac-insider)` — render explicitly so the reader knows the field was checked, not skipped.
  - `pipe_size` null / missing → `PIPE: N/A (per spac-insider)` — never drop the line entirely.
- Pre-deal notes do NOT include this line — PIPE doesn't apply pre-announcement.

### Thesis line
- Always render, on the last content line inside the code block before the `---` that precedes ORDERS.
- 3–4 sentences distilled from `MeteoraMCP:read-memory-doc(name, summary_only=true)` using the stage-bifurcated framework (pre-deal or in-deal) — see "Thesis Block" section for full distillation rules, worked examples, and fallback cases.
- Missing doc: `Thesis: No memory doc exists for [TICKER].`
- Fetch error: `Thesis: Memory doc fetch failed — retry or check manually.`
- Never drop the line entirely — absence is information the reader needs.

### Trust Balance (In-Deal only)
- `$#,##0.00mm` (millions, two decimals).

### In-Deal Target
- Strip `"Announced: "` prefix. Show just the target name after `In deal with: `.

### Outside Date
- Use `spac_details.outside_date` ONLY. If null, render `N/A`. **Do not enrich** from memory doc, press releases, news, or the BCA — the line reflects the sheet state, not the world state. If the sheet has null but the BCA outside date is publicly known to be (e.g.) 9/1/2026, the sheet still wins. Surface the discrepancy elsewhere if it matters; never patch this line.

### Position line vs memory doc
- `spac_details.common_position` / `warrants_position` / `rights_position` are authoritative for the position lines — always quote the sheet. Memory docs can reference older snapshots; that's expected, not a conflict.
- The thesis line MAY reference the trajectory ("residual 472K, down from ~1.1M original") if the arc is load-bearing for the view. Otherwise skip it — the position line speaks for itself.

### Footer (below both code blocks)
Always include:

```
Yields computed @ Tbill = X.XX% (USGG3M), mid = $X.XX
```

If the T-bill fetch failed and we fell back:

```
Yields computed @ Tbill = 3.66% (DEFAULT — live rate fetch failed), mid = $X.XX
```

If the VWAP was invalid and we centered on mid, also append:

```
Matrix centered on mid — no valid 5d VWAP
```

If the VWAP center is materially stale relative to the live mid (|VWAP − mid| > $0.10), append one line so the reader knows the matrix anchor and the actionable spread are decoupled:

```
VWAP $X.XX vs mid $Y.YY — tape moved since 5d window; bid/ask cols anchor actionable levels
```

This is informational only — the matrix still centers on VWAP. Don't fall back to mid; the bid/ask columns already give the actionable view.

### Line suppression
- Suppress any line where ALL values are blank, zero, null, or error.
- Never show an empty line or label with no data.

---

## ORDERS Section Formatting

Appended after a `---` divider inside the main code block. Fixed-width monospace.

### The rendering algorithm — single deterministic recipe

Every row is built by string concatenation. There is no "outer padding" / "inner padding" / "centered header" ambiguity. Build each row by emitting these segments in order:

1. **Label prefix (6 chars):** `"SELL: "` (SELL header), `"BUY:  "` (BUY header), or `"      "` (6 spaces, every data row regardless of side).
2. **Contract field (20 chars):** left-justify the contract name, right-pad with spaces to exactly 20 chars. Python: `f"{name:<20}"`.
3. **For each subsequent column, in order:** emit the literal separator `" | "` (exactly 3 chars: space-pipe-space), then the cell content:
   - **Header row:** the column label, **left-justified, right-padded with spaces** to the column's character width. Python: `f"{label:<{width}}"`.
   - **Data row:** the data value, **right-justified, left-padded with spaces** to the column's character width. Python: `f"{value:>{width}}"`.

That's it. No outer padding around `" | "`, no centering, no per-column variation. The separator is always exactly 3 chars; the cell after it is exactly `width` chars. If you're tempted to add an extra space somewhere because the worked example "looks right," you are mis-reading the example — re-check by counting chars.

### Contract Name Formatting
- Derive from `ticker` field on the EMSX order.
- Strip leading stock symbol and space (`KDK US ` → `""`).
- Reformat: `"10/16/2026 C9"` → `"Oct 16/26 C9"`, `"01/21/2028 C12.5"` → `"Jan 21/28 C12.5"`.
- Equity orders: use the Bloomberg ticker directly (e.g., `KDK US Equity`).
- Column width: pad to 20 chars (right-pad with spaces). Names longer than 20 chars are not expected; if encountered, do NOT truncate — let the row run wide for that one line.

### Columns

Render share-count columns (`Ord`, `Fill`, `Rem`) differently based on whether the order is for an **option contract** or an **equity** (common/warrant/rights):

- **Option orders** (yellow_key implies option, or contract name has expiry like `Jun 18/26 C9`): render as raw integer contract count.
- **Equity orders** (Bloomberg ticker like `ATII US Equity`, `ATIIW US Equity`, etc.): render share counts in `k` notation. The `Ord` column is almost always a round multiple of 1000 (e.g., 25000 → `25k`, 10000 → `10k`); `Fill` and `Rem` may not be — render fractional thousands with one decimal (e.g., 22468 → `22.5k`, 4593 → `4.6k`). Render counts under 1000 as the raw integer (e.g., 300 → `300`, 0 → `0`). Round to 1 decimal place; do not show trailing zeros (e.g., `25k` not `25.0k`).

### Column widths — pick ONCE per block, no iteration

If **any order in the block** is an equity at $1+ (i.e., not a sub-dollar warrant and not an option), use **equity-mode widths** for the entire block. Otherwise, use **option-mode widths**. This avoids re-laying-out the table mid-render. ATIIW at $1.96 = equity-mode. PSQHW at $0.40 = treat as the option-block driver (sub-dollar warrant).

| Column | Option mode | Equity mode |
|---|---|---|
| Contract | 20 chars | 20 chars |
| Ord  | 4 (`9999`) | 5 (`55.4k` / `999k`) |
| Fill | 4 | 5 |
| Rem  | 4 | 5 |
| Avg  | 5 (`0.000`) | 6 (`10.723`) |
| Lmt  | 4 (`0.00`) | 5 (`10.95`) |

BUY block omits the Avg column entirely (header and data both).

### Worked examples — byte-accurate

**Equity-mode block (ATII):**

```
SELL: Contract             | Ord   | Fill  | Rem   | Avg    | Lmt  
      ATII US Equity       |   20k | 15.1k |  4.9k | 10.835 | 10.75
BUY:  Contract             | Ord   | Fill  | Rem   | Lmt  
      ATII US Equity       |   25k |   300 | 24.7k | 10.56
      ATIIW US Equity      |   25k |     0 |   25k |  0.50
```

Verify by char-count if needed. SELL header row decomposes as:
- `"SELL: "` (6) + `"Contract            "` (20) + `" | "` (3) + `"Ord  "` (5) + `" | "` (3) + `"Fill "` (5) + `" | "` (3) + `"Rem  "` (5) + `" | "` (3) + `"Avg   "` (6) + `" | "` (3) + `"Lmt  "` (5) = **67 chars**.

The trailing spaces in the last header cell (`"Lmt  "`) are real — keep them. They make every header row the same width as the longest data row, which preserves column alignment if the row is later re-rendered or copied.

**Option-mode block:**

```
SELL: Contract             | Ord  | Fill | Rem  | Avg   | Lmt 
      Jun 18/26 C9         |  200 |  107 |   93 | 0.529 | 0.55
      Jun 18/26 C10        |  100 |   26 |   74 | 0.512 | 0.40
BUY:  Contract             | Ord  | Fill | Rem  | Lmt 
      Jun 18/26 C10        |  100 |    0 |  100 | 0.05
```

Other column rules:
- **Avg**: `avg_price` formatted `0.000`; `--` (right-aligned, padded left) if zero. For equity-mode 6-char column, `--` renders as `"    --"`.
- **Lmt**: `limit_price` formatted `0.00` (option) or `0.00`/`#0.00` (equity) — right-aligned in the column width.

If a single equity order legitimately exceeds 999k shares (rare), expand Ord/Fill/Rem to 6 chars for that note. Don't truncate.

#### Examples — equity rendering

| Raw value | Rendered |
|---|---|
| 25000 | `25k` |
| 10000 | `10k` |
| 22468 | `22.5k` |
| 4593 | `4.6k` |
| 24700 | `24.7k` |
| 300 | `300` |
| 0 | `0` |

### Grouping
- Separate SELL from BUY into labeled blocks.
- Within each, sort by expiry ascending, then strike ascending.
- Omit a block entirely if no orders on that side.
- If emsx-blotter returns empty, omit the whole `---` / ORDERS section.

### Status filter
- Only `WORKING` orders.

---

## Batch Mode

For multiple tickers: one note per ticker separated by blank line and `---`. Call `spac-details` and `emsx-blotter` once per ticker, but make **one** batched `get-price` call containing all common/warrant/rights tickers across every SPAC **plus `"USGG3M Index"`**. The T-bill rate is fetched once and reused for every note. `read-memory-doc` is called once per ticker (not batchable) — this is cheap relative to `get-price` so it's fine.

Each note gets its own yield matrix, its own thesis block, and its own footer line (same T-bill rate across the batch).

---

## What This Skill Does NOT Do

- Does not model extension deposits. Use `trading-note-extended` for that.
- Does not model trust leakage (taxes, WC). Use `spac-yield-calc` for leakage-adjusted yields.
- Does not read or trust `s4_amendments` from the sheet. The EDGAR 3-pass count replaces it entirely.
- Does not prompt for Extensions, # Rights, # Public Shares, Notes, Recommendation, or Last s-4 (manual-entry fields in the VBA macro). PIPE is now pulled from `spac-details.pipe_size` (rollout field — see "PIPE line" formatting rule).
- Does not fetch unit prices from Bloomberg.
