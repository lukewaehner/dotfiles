---
name: trading-note-extended
description: >
  Generate a formatted SPAC trading note with live-recomputed yields (Bloomberg mid + USGG3M) modeling sponsor extension deposits from EDGAR 8-Ks, a VWAP-centered yield matrix (±1c/±2c/±3c plus bid/ask), an EDGAR-verified S-4/F-4 count (3-pass: SPAC CIK + PubCo CIK), and a `Thesis:` line pulled from the Meteora memory doc. Trigger on 'extended note', 'full note', 'note with extensions', 'trading note extended', or any trading-note request where extension deposits or a verified S-4/F-4 count matters (post-IPO-anniversary names, stale sheet counts). Unit renders as `U=S+W/2+R/10` or `U=S`. For the lightweight version, use `trading-note-simple`.
---

# Trading Note — Extended Variant

Generate formatted SPAC position notes with:
- Live Bloomberg prices and live-recomputed yields **incorporating sponsor extension deposits** (extracted from EDGAR 8-Ks / Articles)
- Inline unit-structure notation (`U=S+W/2+R/10` or `U=S`) placed near positions
- A VWAP-centered yield matrix showing yield at ±1c/±2c/±3c price steps plus live bid/ask, **with extension deposits modeled in each cell**
- An **EDGAR-verified S-4/F-4 amendment count** (3-pass workflow; sheet value ignored) for in-deal SPACs
- A 3–4 sentence thesis block distilled from the Meteora memory doc (bifurcated pre-deal vs in-deal framework, calibration preserved) or a "no memory doc" flag, placed inside the code block, directly above the `---` that precedes ORDERS
- Live EMSX orders appended

This is the deep variant. For the fast version without extension-deposit extraction or EDGAR verification, use `trading-note-simple`.

## Workflow

1. Call `MeteoraMCP:spac-details` with the requested ticker to get positions, trust data, deadlines, scenario dates, `vwap_5d`, `notes`, `ipo_date`, and the correct warrant/rights tickers.
2. In parallel with step 1 if possible:
   - `MeteoraMCP:emsx-blotter` with `ticker` set to the base ticker.
   - `MeteoraMCP:get-price` with `tickers` set to a batch of valid security tickers (common, warrant, rights) **plus `"USGG3M Index"`**. Single batched call.
   - `MeteoraMCP:read-memory-doc` with `name` set to the base ticker and `summary_only=true`. See "Thesis Block" below.
3. **EDGAR S-4/F-4 verification** (in-deal only — skip for pre-deal):
   - Run the 3-pass registration-statement workflow (see "S-4/F-4 Verification" below).
   - Produce an **amendment count** sourced from EDGAR. **Do NOT use `s4_amendments` from the sheet** — that field is unreliable.
4. **Extension deposit extraction** (in-deal AND pre-deal where IPO is >18 months ago):
   - Run the 8-K workflow around the IPO anniversary ±2 months (see "Extension Deposits" below).
   - Extract per-share deposit amount, frequency, cap, start date.
   - If the sheet `notes` field mentions extension terms, cross-reference and flag any discrepancy.
5. Determine `stage` from spac-details (`predeal` or `indeal`).
6. Extract live common bid/ask/mid, warrant mid, rights mid. Extract T-bill rate = `USGG3M Index.price / 100`.
7. Recompute `C-T = bbg_common_mid − cash_in_trust` (signed).
8. **Compute extension-adjusted yields** at each (price × scenario date) combination needed for the matrix — see "Yield Recalculation" and "Yield Matrix" below. The 5-line EST/6MON/9MON/12MON/MAX schedule is NOT rendered in the main note — yields live exclusively in the matrix.
9. **Build the VWAP-centered yield matrix** (extension deposits applied to each cell; see "Yield Matrix" below).
10. **Distill the thesis block** from the memory doc summary — see "Thesis Block" below.
11. Assemble the note using the appropriate template. In-deal notes include `s/f-4s: [EDGAR count]` — **explicitly labeled as EDGAR-verified, NOT from the sheet**. **Insert the thesis block directly above the `---` that precedes ORDERS.**
12. Append the ORDERS section.
13. Output note as fenced code block, then yield matrix as second fenced block, then footer lines, then a one-line Extensions summary (if extensions are active).
14. Batch mode: one note per ticker, separated by blank line and `---`. Single batched `get-price` covering all tickers. EDGAR, 8-K extraction, and memory-doc reads must still run per ticker.

## Live Price Fetch

Identical to `trading-note-simple`. Bloomberg mid is authoritative, sheet is fallback.

- **Common**: use `mid`; also extract `bid` and `ask` for the matrix. Fall back to `last_trade` only if mid unavailable AND recent.
- **Warrant**: slash tickers need ` US Equity` suffix (`FCRS/WS US Equity`, `LEGT/WS US Equity`); plain alphanumeric pass as-is.
- **Rights**: pass plain.
- Skip any ticker that is 0, null, empty, or `#N/A`.
- Always include `"USGG3M Index"` in the batch.

T-bill rate: `USGG3M Index.price / 100`. Fallback 3.66% with footer flag if fetch fails.

---

## S-4/F-4 Verification (EDGAR, 3-Pass — In-Deal Only)

The sheet's `s4_amendments` field is systematically unreliable. For in-deal SPACs, always re-derive the count from EDGAR using the full 3-pass workflow from the yield-calc skill. The goal is a **count of registration-statement filings on record** (public S-4/F-4 plus amendments; DRS counted separately when present).

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

**Step 3a — Extract the PubCo's exact legal name** from the deal-announcement 8-K's Exhibit 2.1 (BCA / Agreement and Plan of Merger), which Pass 1 already returned. The PubCo name lives in the BCA preamble. Free lookup — don't web-search for it.

**Step 3b — Search the web for the CIK, with fetchable URLs only:**

```
web_search: "[PubCo full legal name]" S-4 site:sec.gov
web_search: "[PubCo full legal name]" stocktitan OR spacresearch
```

What is fetchable from this environment (and what isn't):

| URL pattern | Fetchable? | Use for |
|---|---|---|
| `sec.gov/Archives/edgar/data/[CIK]/...` | ✓ | CIK is in the path — read it off the URL, no fetch needed |
| `stocktitan.net/sec-filings/[TICKER]/...` | ✓ | Aggregator mirrors of SEC filings; CIK in page content |
| `spacresearch.com`, `justia.com`, `prnewswire.com`, news sites | ✓ | Confirmatory only |
| `efts.sec.gov/LATEST/search-index?...` | ✗ | SEC full-text search backend — **not fetchable, don't try** |
| `sec.gov/cgi-bin/browse-edgar?...` | ✗ | EDGAR company browser — **not fetchable, don't try** |

The CIK is the digit string in any `sec.gov/Archives/edgar/data/[DIGITS]/` URL the search returns. Pull it directly from the URL, then call `edgar-filings(cik="[CIK]", limit=20)` and count normally.

**Step 3c — If no `/data/[CIK]/` URL surfaces** after two well-shaped searches, try one alternative name spelling (drop punctuation, vary "Inc."/"Corporation"). If still nothing, render:

```
... s/f-4s: unverified (EDGAR — PubCo CIK not located via web)
```

…and add a footer flag: `⚠ PubCo S-4 filing not confirmable via EDGAR — verify manually`. Do NOT guess `0` or `1` when you couldn't confirm.

**Anti-pattern — don't waste calls on:**
- Fetching `efts.sec.gov` or `sec.gov/cgi-bin` — return permission errors.
- Generic re-queries of the same phrase. Vary the *PubCo name spelling*, not the boilerplate around it.
- Fetching news stories that just quote the BCA boilerplate from an 8-K you already have.

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
... s/f-4s: 3 (EDGAR-verified);
```

If the EDGAR workflow returned zero registration statements after all 3 passes:
```
... s/f-4s: 0 (EDGAR — none filed);
```

If pass 3 was not attempted because pre-conditions weren't met but the count looks suspiciously low, flag in the footer rather than silently reporting low numbers.

---

## Extension Deposits (8-K Extraction)

The ONE reason this skill exists versus `trading-note-simple`. Many SPACs require sponsor deposits into trust for each extension period; these **increase CIT at exit** for extended scenarios and materially change yield.

### When to extract

- **In-deal SPAC**: always extract.
- **Pre-deal SPAC where IPO is >18 months ago**: always extract (likely in extension territory).
- **Pre-deal SPAC where IPO is <18 months ago**: skip — no extensions possible yet.

### Extraction workflow

Run a filtered 8-K search around the IPO anniversary:
```
edgar-filings(ticker="[TICKER]", form_type="8-K", filing_date="[IPO_ANNIVERSARY − 2 months]:[TODAY]")
```

Read each 8-K's Item headers. Focus on:
- **Item 1.01** (Material Definitive Agreement) — promissory notes, contribution agreements, sponsor deposit commitments
- **Item 5.03** (Amendments to Articles) — articles amendment approving extension
- **Item 2.03** (Creation of Direct Financial Obligation) — often cross-references the promissory note from Item 1.01
- **Item 8.01** (Other Events) — occasional extension deposit confirmations

For any 8-K with Item 1.01 or 2.03, read the full body. Extract:
- Per-share deposit amount per extension period
- Aggregate cap, if any (e.g., "$375,000 per month")
- Frequency (monthly vs. per-extension-period)
- Source of funds (sponsor, promissory note, target contribution)
- Start date of deposits (first extension date)
- Number of deposits already made (count months from first deposit to today)

**CRITICAL LESSON (HYAC case study)**: Extension deposits are frequently NOT in the Articles of Association at all. The Articles may grant the board discretion to extend with no deposit mention, while a separate 8-K promissory note establishes the deposit obligation. Always run the 8-K search. Articles-only extraction will miss the deposits.

If the user memory or spac-details `notes` field mentions "$Xk/mo extensions" or "paying $Y/mo," use it as a **hint**, but still verify via 8-K. Flag any mismatch between the sheet notes and EDGAR findings.

### If no extension 8-Ks found

- Pre-deal SPAC within 18 months of IPO: confirm no extensions expected; proceed with zero extension deposits.
- Pre-deal/in-deal >18 months post-IPO with no extension 8-Ks: this is a red flag — either the sponsor isn't funding extensions (rare), or we missed them. Flag in the footer: `⚠ No extension 8-Ks found despite post-anniversary window — verify manually`.

---

## Yield Recalculation (with extension deposits)

### Inputs

| Input | Source |
|-------|--------|
| `price` (common mid) | Bloomberg |
| `cit_today` | `cash_in_trust` |
| `tbill_rate` (decimal) | USGG3M / 100 |
| `ext_deposit_per_share_per_month` | Extracted from 8-K (or 0 if none) |
| `ext_cap_per_month` (optional) | Extracted from 8-K |
| `common_outstanding` | spac-details (for cap conversion) |
| `today` | current ET date |
| Scenario dates | est_date, six_month_date, nine_month_date, twelve_month_date, max_date |

### Effective per-share extension deposit

If the sheet/8-K states a flat dollar cap (e.g., "$375,000/month"), convert to per-share using public shares outstanding:
```
effective_per_share = min(stated_per_share_per_month, cap_per_month / public_shares_outstanding)
```
If only a per-share figure is stated (no cap), use it directly.

### Formula per scenario date D

```
days_to_exit        = (D − today).days
months_to_exit      = days_to_exit / 30.4375     # fractional months
trust_accrual       = cit_today × tbill_rate × days_to_exit / 365
extension_deposits  = effective_per_share × months_to_exit    # simple linear; see "Cadence" below
cit_at_exit         = cit_today + trust_accrual + extension_deposits
total_return        = cit_at_exit / price − 1
annualized          = total_return × 365 / days_to_exit
```

Format: `#.##%`.

### Cadence

If deposits are **monthly** (most common): use fractional months as above.

If deposits are **per-extension-period** (e.g., a lump sum per 3-month extension) — count how many discrete extension triggers fall within the scenario window:
```
num_extensions_in_window = floor(days_to_exit / extension_period_days)
extension_deposits       = effective_per_extension × num_extensions_in_window
```

If deposits **have already started** (past anniversary and running): CIT already includes prior deposits in the `cash_in_trust` value returned by spac-details. Only FUTURE deposits (between today and D) get modeled here.

### Edge cases

- `days_to_exit ≤ 0` → drop that scenario date from the matrix.
- Missing scenario date → drop that row.
- `price ≤ 0` or CIT missing → render `--` in affected cells (or omit the column/row).
- No extensions extracted → treat extension_deposits as 0 (behaves like simple variant on that dimension).

### Simplifications still applied

- **No trust leakage** (taxes, WC) — for leakage-adjusted yields, use `spac-yield-calc`.
- **Simple annualization** (×365/days), not compound.

---

## Yield Matrix (VWAP-centered, with extensions)

Same structure as `trading-note-simple`, but each cell uses the extension-adjusted yield formula.

### Center selection

- **Primary**: `vwap_5d` from spac-details.
- **Fallback**: if `vwap_5d` is 0, null, or obviously invalid (e.g., < $1 for a SPAC), center on live Bloomberg mid. Flag: `Matrix centered on mid — no valid 5d VWAP`.

### Cent step computation — locked

Round the center to 2 decimals BEFORE generating column offsets. Use the rounded prices for BOTH display AND the yield formula:

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

- Center column **label** is `VWAP` normally, or `Mid` when `vwap_5d` is invalid and we fell back.
- If bid or ask is unavailable from Bloomberg, omit that column. Note the omission in the header annotation: `Bid = --, Ask = $10.28`.

### Rows

One row per scenario date that passes edge-case filter (days_to_exit > 0, date not null).

### Coincident-date dedup

If two or more scenario rows resolve to the same exit date, collapse them into a single row with a slash-joined label. Yields would be identical anyway — duplicate rows are visual noise.

- `est_date == max_date` → label `EST/MAX (mm/dd/yyyy)`
- `est_date == six_month_date` (sponsor on a known short deadline) → `EST/6 MON (mm/dd/yyyy)`
- More than two collide → join with slashes in canonical order: `EST/6 MON/MAX (mm/dd/yyyy)`

Canonical order for slash-joining: `EST → 6 MON → 9 MON → 12 MON → MAX`. Dedup happens AFTER days-to-exit filtering, so already-dropped rows don't participate.

Common in practice: deals announced ~6 months before the original deadline often have `est_date == max_date` because no extension is needed before the vote. Both rows would show identical yields; one slash-labeled row is sufficient.

### Formula per cell

Use the full extension-adjusted formula:
```
yield(price, D) = ((cit_today + cit_today × tbill_rate × days_to_exit/365
                    + effective_per_share × (days_to_exit / 30.4375)) / price − 1)
                  × 365 / days_to_exit
```

(Or the per-extension-period variant if that's the cadence.)

### Layout — Markdown table (Bloomberg-pasteable)

**Output the matrix as a GitHub-flavored markdown table** with pipes (`|`) and a `|---|` separator row. This is the format that copy-pastes cleanly into Bloomberg — it lands as separate cells. Do NOT use tab-separated text, fixed-width spacing, or a fenced code block for the matrix itself.

The table has TWO header rows above the data:

1. **Row 1: column labels** — `Yield`, then the 9 fixed column labels in this exact order: `−3c, −2c, −1c, VWAP` (or `Mid`), `+1c, +2c, +3c, Bid, Ask`.
2. **Row 2: actual dollar prices** — `Price`, then each column's price in the same fixed order.

Then the standard markdown `|---|---|...|` separator row, then the data rows (one per scenario date).

### Example output (with extensions)

Header line (plain text above the table):

`YIELD MATRIX — centered on VWAP = $10.27, Bid = $10.26, Ask = $10.28; w/ extensions ($0.025/sh/mo)`

Then the markdown table:

| Yield | −3c | −2c | −1c | VWAP | +1c | +2c | +3c | Bid | Ask |
|---|---|---|---|---|---|---|---|---|---|
| Price | $10.21 | $10.23 | $10.25 | $10.27 | $10.29 | $10.31 | $10.33 | $10.26 | $10.28 |
| EST (06/01/2026) | 12.85% | 10.60% | 8.34% | 6.07% | 3.82% | 1.61% | -0.58% | 11.94% | 4.68% |
| 6 MON (10/24/2026) | 8.68% | 7.34% | 6.02% | 4.72% | 3.45% | 2.20% | 0.99% | 7.86% | 4.08% |
| 9 MON (01/23/2027) | 7.05% | 5.98% | 4.93% | 3.90% | 2.88% | 1.88% | 0.90% | 6.43% | 3.38% |
| 12 MON (04/24/2027) | 6.12% | 5.21% | 4.32% | 3.44% | 2.58% | 1.74% | 0.91% | 5.55% | 3.00% |
| MAX (07/29/2027) | 5.58% | 4.75% | 3.92% | 3.12% | 2.34% | 1.56% | 0.80% | 5.05% | 2.73% |

If extensions are zero, drop the `; w/ extensions ($X.XX/sh/mo)` clause from the header line.

If `vwap_5d` is invalid, the header annotation changes and the center column's label row reads `Mid` instead of `VWAP`. Everything else is identical.

### Cell edge cases
- Missing bid or ask → OMIT that column entirely. Don't leave a blank cell — drop the whole column. Note the omission in the header annotation: `Bid = --, Ask = $10.28`.
- Stepped price ≤ $0 → omit that step column.
- Row days_to_exit ≤ 0 → omit that data row.
- If the matrix ends up with fewer than 2 price columns, suppress it entirely and print `Yield matrix unavailable — insufficient price data`.

### Why no yields in the main note

The main note does NOT include EST/6MON/9MON/12MON/MAX yield lines. Those live exclusively in the matrix. Scenario dates appear as matrix row labels.

---

## Unit Structure Notation

Identical to `trading-note-simple`. Placed near the positions.

Format: `U=S+W/n+R/m`.

- `warrants_in_unit = "1/2"` → `W/2`
- `warrants_in_unit = "1/3"` → `W/3`
- `warrants_in_unit = "1"` → `W` (no denominator)
- `warrants_in_unit = "1 for 3/4"` → `W*3/4` (rare, render literally)
- `warrants_in_unit = "None"` / null → omit

- `rights_in_unit = "1 for 1/10"` → `R/10`
- `rights_in_unit = "1 for 1/8"` → `R/8`
- `rights_in_unit = "1/5"` → `R/5`
- `rights_in_unit = "1/7 for 1"` → `R*7` (inverse)
- `rights_in_unit = "None"` / null → omit

Rendering:
- Both present: `U=S+W/2+R/10`
- Only W: `U=S+W/2`
- Only R: `U=S+R/10`
- Neither: `U=S`

---

## Thesis Block

A short summary of the current Meteora view on the name, pulled from the memory doc. Goes **inside the note code block**, on its own line(s), directly above the `---` that separates the note body from ORDERS.

### Core principle (the guardrail)

The thesis is sourced **EXCLUSIVELY** from the Executive Summary returned by `MeteoraMCP:read-memory-doc`. No other source is permitted, ever — not the sheet `notes` field, not the sheet `recommendation` field, not spac-details headers, not filings, not EDGAR extension cadence, not 8-K extension data, not sponsor identity, not first principles. If there is no memory doc, the thesis is `Thesis: No memory doc exists for [TICKER].` — full stop. The bullets below are signposts for what to look for *when distilling an existing doc*, NOT a checklist to fill in from scratch.

The header, matrix, extension line, matrix footer, and ORDERS section already carry CIT, structure, sponsor, UW, deadlines, yields, per-share extension contributions, and our active book. A "thesis" that just relabels that information is empty. A "thesis" that quotes or paraphrases the sheet `notes` or `recommendation` field is **worse than empty** — those fields are systematically stale and re-surfacing them as "current view" is actively misleading.

### Forbidden sources (never use these for the thesis)

The following are **NEVER** valid sources for any sentence in the thesis line, even partially, even paraphrased:

- `spac_details.notes` — sheet free-text field. Often months out of date; may reflect a view that's been reversed.
- `spac_details.recommendation` — sheet free-text field. Stale price levels, abandoned trade ideas, or instructions that no longer match the live book are common.
- `spac_details.s4_amendments` — already flagged as unreliable elsewhere in this skill.
- The header / matrix / extension line / ORDERS content itself (re-stating CIT, yields, extension cadence, position size, working orders).
- EDGAR 8-K extension data extracted in this same workflow — that data drives the extension line, NOT the thesis.
- Web search, filings, or first-principles reasoning about sponsor / structure / sector.
- The user's prior conversation context unless that context is specifically a memory doc read in this same session.

If the only thing that would let you write a substantive thesis is one of the above sources, you must instead render the "no memory doc" or "fetch failed" fallback. **Synthesizing from forbidden sources is the failure mode this section exists to prevent.**

### Source

`MeteoraMCP:read-memory-doc(name="[TICKER]", summary_only=true)` — pass the base common ticker (e.g. `IPCX`, `KDK`, not `IPCXR` or `KDKRW`). This returns the Executive Summary only, which is the living two-pager on the name. **This is the ONLY permitted source.**

### Stage selection

The framework bifurcates by stage. Use the `stage` field from `spac-details` (already determined in the workflow):
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

Do not attempt to synthesize a thesis from any other source. Specifically, do NOT pull from `spac_details.notes`, do NOT pull from `spac_details.recommendation`, do NOT generate one from sponsor identity / UW / sector / EDGAR extension cadence / 8-K extension data / position size / working orders / sheet flags. The whole point of the flag is to signal that the reader should build one. **This applies even when the spac-details payload + extension data look "rich enough" to write something** — the absence of a doc IS the information. If you find yourself reaching for `notes`, `recommendation`, or extension cadence to "fill in" a missing doc, stop and render the fallback.

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
4. **Current Meteora posture with EXACT build triggers.** What we're doing and the price level driving it — building common at discount-to-trust for yield-floor, working warrants/rights at a level for cheap optionality, FPA-origination posture if PIPE looks shaky. **Use the EXACT thresholds from the doc, not approximations.** "6%+ IRR to est close, warrants below 10c as a flyer" not "decent yield, cheap warrants." If the doc has explicit IRR thresholds, price levels, yield levels, sizing caps, or "build-only-if" conditions, NAME them. If the public securities are not the trade, end with the next-best Meteora seat (FPA / structured paper / sponsorship). Pull dust-position context if relevant ("existing 1,000 [TICKER]W is residual IPO dust").

### In-Deal Framework (3–4 sentences, distilled from memory doc)

1. **Closing probability read with calibration.** MCC status (met / has credible path / load-bearing risk), PIPE structure and quality of names (committed at trust = strong; structured convert at discount = couldn't raise clean; no PIPE = MCC is harder), CoC/debt overhang. **Match the doc's calibration** — "mechanically closes" only if no MCC + no FPI risk + clean F-4 history; otherwise "likely closes" or "should close" with the friction noted. Preserve foreign-target nuance ("Polish better than Chinese", "less F-4 friction than China deal but not clean").
2. **Sponsor-incentive read.** What the sponsor's economic situation (deferred UW math, WCW draws, founder-share forfeit, dollars committed to extensions, prior shell-sale economics) tells us about the playbook they'll actually run. *Canonical examples: CCIX "Klein won't walk away from $1M WCW" or SIMA "$8mm shell purchase + 1.5% deferred fee = sponsor has a target lined up."* The thesis can reference extensions only when extensions are the load-bearing part of the trade view (e.g., "carry through 2 paid extensions then redeem", "extensions flip yield attractive post-anniversary"). Do NOT restate per-share contribution amounts ($0.025/sh/mo, $0.033/sh/mo) — those are matrix-footer data, not thesis payload.
3. **Process / timeline read.** S-4/F-4 cadence, SEC posture, deadline gap (real runway vs. cornered), gating items (FPI complications, MAE-event termination risk, regulatory clearances). Include the next concrete dated catalyst (S-4 filing, vote, outside date, hard deadline, anniversary extension date) and include the date. Flag extension or termination risk where load-bearing.
4. **Current Meteora posture with EXACT triggers.** Long commons for yield-to-vote, working warrants/rights at a level, FPA participation, redeem-at-vote, sell-the-rights-into-pop. Tied to a specific price AND a specific trigger that would change sizing. Use exact thresholds from the doc.

---

### Distillation rules (apply to both frameworks)

- **The bullets are signposts, not slots.** Use 3 sentences if the doc only speaks to 3 dimensions; use 4 if all are load-bearing. Never pad to hit 4.
- **Mirror exact thresholds from the doc.** "$10.75 × 200K GTC bid" not "build at a discount." "60c wake-up sell on warrants" not "trim on strength." "6%+ IRR to est close" not "decent IRR." Numbers are the contract between the reader and the doc.
- **Specificity test** — if the sentence could appear verbatim in another SPAC's note, it's too generic. If it requires the specific facts of *this* doc to write, it's right. "Banker-shopped first-timer with no track record" fails the test. "Dominari paid $8mm for the shell + committed 1.5% deferred UW fee" passes.
- **No verbatim copies** of large Executive Summary paragraphs. Distill into your own active-voice sentences.
- **Mirror the doc's calibration.** Don't strip out hedging ("likely", "we think", "base case", "could slip", "maybe") to make the thesis sound more confident than the doc actually is. Forecasts without confidence language read as overconfident assertions; the reader needs to know what's view vs what's fact.

### Calibration rules (in-deal-specific, preserved from prior framework)

- **Deal closure language:** "mechanically closes" only if the doc says no MCC + no FPI risk + sponsor has clean F-4 history. Otherwise use "likely closes" or "should close" with the friction noted (FPI, foreign-target F-4, sponsor extension history).
- **Foreign target nuance:** If the doc distinguishes Polish / European / Israeli targets from Chinese / PRC ones, preserve that distinction. Don't collapse it.
- **Post-close trading forecast:** Prepend with **"we think"** / **"best case"** / **"base case"** / **"likely"** unless the doc states the forecast as fact. Specific number ranges ($2–4, $1–3) are fine; the hedge belongs on the verb, not the number.
- **Build triggers:** Use the EXACT thresholds from the doc, not approximations.
- **Extension dynamics:** Reference extensions only when they're the load-bearing part of the current trade view. Per-share contribution amounts belong in the matrix footer, not the thesis.

### Tone

Walter-facing, voice of a colleague who read the doc this morning. Terse, concrete, directional. No headings, no bullets, no bold inside the rendered thesis line.

### What not to pull in

- **No raw header / matrix / extension-line re-statement.** The matrix and header already carry CIT / structure / sponsor / UW / deadlines / yields, and the matrix footer carries extension contribution amounts. The thesis is about the *view*, not the data.
- **No verbatim Executive Summary paragraphs.** Distill.
- **No content from `spac_details.notes` or `spac_details.recommendation`.** These sheet fields are stale-prone and explicitly prohibited as thesis sources. Do not paraphrase them, do not "incorporate" them, do not use them to flesh out a thin doc. If the memory doc doesn't say it, the thesis doesn't say it.
- **Extension-deposit mechanics belong in the matrix footer, not the thesis.** Reference extensions only when they're the load-bearing trade view (e.g., "carry through next two paid extensions then redeem"), never as a restatement of contribution amounts.
- **Do not invent thresholds or triggers** not in the doc. If the doc has no explicit IRR / price threshold, the posture sentence states the directional view without fabricating numbers.

### Worked examples (sourced from real memory docs)

**Pre-deal (ALUB):**
> *Thesis: Repeat Alussa franchise — ALUS I closed FREYR with $600M PIPE from Koch / Glencore / Fidelity blue-chip names, demonstrating real deal-closing capability and institutional PIPE-raising; post-close target failure was execution risk, not sponsor capability. Team upgraded for ALUB II with Slorer (ex-Morgan Stanley energy MD, ex-BTIG energy IB head) joining as CEO specifically to source deals through his sell-side network, UW upgraded BTIG → Santander signaling move upmarket for PIPE origination. Long 646K commons at ~$10.03 (11c below $10.14 trust, ~4.4% YTM) plus 59K warrants for cheap pipeline optionality; warrants at 30–35c are cheap if pipeline is real, bleed to zero if sitting on trust income.*

(Three sentences — covers franchise read, mandate credibility/team upgrade, and posture with exact threshold. Structural-takeaway slot dropped because the ALUB doc doesn't make it load-bearing.)

**In-deal (SIMA):**
> *Thesis: Dominari paid $8mm for the shell plus a committed 1.5% deferred UW fee — too expensive to be speculative, implying a target is already lined up. Sponsor is running a serial extension-postponement playbook (no trust contribution, no new redemption window) until announcement; base case June–July 2026 before the 7/11/26 hard liq forces a vote. Long 1,683 commons via $10.75 × 200K GTC bid for redemption-yield floor (~3.7%) plus deal-pop optionality; 200K SIMAW @ avg ~23c scaling to ~300K via $0.23 × 100K GTC for ~30c modal pop on announcement; do not pay above trust on commons or above 26c on warrants, wake-up sell at 60c.*

(Three sentences — sponsor-incentive read absorbs closing-probability since the $8mm math IS the closing-probability evidence. Process/timeline lives in sentence 2. Posture in sentence 3 with exact bid, exact size, exact don't-pay levels and wake-up offer.)

**In-deal (CCIX, terminated):**
> *Thesis: Deal with PlusAI terminated 4/20/26 "due to market conditions"; SPAC alive until 8/6/26 Combination Period deadline but governing docs prevent another viable extension (auto-extension already spent, re-extension requires 100% redemption opt-out which collapses trust). Klein runs the clock to capture the final 5/6/26 WCW draw ($1M) — Churchill playbook across CC-I through CC-VIII confirms sponsor will not walk away from interest entitlement. Base case: wind-down 8-K mid-July, trust distribution late Aug / early Sep at ~$10.91–10.95 vs. current $10.72, ~5.8% IRR. Long 925K commons; hold/add below $10.70 (6%+ annualized), no chase above $10.74; warrants are structurally dead paper at 66c, do not buy.*

(Four sentences — closing-probability inverted into "won't liquidate, won't re-extend," sponsor-incentive read on WCW math, timeline forecast with prices, posture with exact triggers. Note "base case" calibration preserved.)

### Examples of good thesis sentences (calibration preserved)

- "Build common at 6%+ IRR to est close, warrants below 10c as a flyer — existing 1,000 MMTXW is residual IPO dust, FPA / ELOC origination is the only real Meteora seat."
- "Deal announced 4/23/26 likely closes on no-MCC all-stock rollover; S-4 maybe expected ~June 2026 (FPI friction softer than China but real), 9-month outside 1/23/2027."
- "B4 Asian-shell template + low-quality UW + Class B 15-vote founder → PubCo we think trades $2–4 post-close, common holders redeem at vote."
- "Reducing commons toward zero on sub-5% yield, target full exit before est-date."
- "Selling rights into catalyst-driven volume spikes, target 38–40c."
- "Carry through the next two paid extensions on 6%+ trust accrual; flip view if sponsor signals third extension."

### Examples of bad thesis sentences

- "The company is a SPAC with a business combination agreement." (too generic)
- "[TICKER] presents an interesting opportunity." (empty filler)
- "Rights-only structure with no warrant coverage means dilution-on-close is direct." (re-states header; doesn't interpret it)
- "First-time sponsor with generic mandate suggests banker-shopped sourcing." (could appear verbatim in any first-time-sponsor note — fails specificity test)
- "Rights at 22c look fairly priced as deal-probability lottery." (empty hedge with no anchor — what would change the view? at what price would we size up?)
- "Deal mechanically closes and post-close trades $2–4." (strips hedging — overconfident vs underlying view)
- "No build on common or warrants." (bare directive — doesn't surface the build trigger or the next-best seat)
- "Sponsor depositing $0.033/sh/mo over 3 extensions." (data dump — extension mechanics belong in the matrix footer, not the thesis)
- "Sheet flagged 'Bad deals, Cantor underwriter' with sheet rec C 10.41/10.50, ws 30c." (verbatim from `spac_details.notes` and `spac_details.recommendation` — explicitly forbidden sources, and these fields are systematically stale)
- "Treasury-yield play at trust; sheet rec is buy ws at 30c." (paraphrased from `recommendation` — same failure mode, hidden under different wording)
- "Real ongoing G&A burn ($175K Q2 / $383K H1 2025) so trust accrual partially offset over time." (synthesized from filings or first principles in the absence of a memory doc — even if true, this is a forbidden source for the thesis line)

If the only source available for any of these statements is the sheet `notes` / `recommendation` field, EDGAR / 8-K extension data, or independent reasoning, render the "no memory doc" fallback instead. The reader needs to know there's no doc; manufacturing one defeats the entire signal.

---

## Data Field Mapping

### Shared fields

| Field | Source | Note Usage |
|-------|--------|-----------|
| `spac_ticker` / `warrant_ticker` / `rights_ticker` | spac-details | Tickers |
| `common_position` / `warrants_position` / `rights_position` | spac-details | Positions |
| `price` (common mid / warrant mid / rights mid) | **get-price** | Prices (fallback to sheet) |
| `bid` / `ask` (common) | **get-price** | Yield matrix anchor columns |
| `vwap_5d` | spac-details | Matrix center (fallback to mid) |
| `warrants_in_unit` / `rights_in_unit` | spac-details | Unit notation |
| `domicile` / `underwriter` / `bucket` / `category` | spac-details | Header |
| `cash_in_trust` | spac-details | CIT |
| **C-T** | **computed** | `mid − CIT`, signed |
| `common_outstanding` | spac-details | Common O/S line |
| `pct_9_outstanding` | spac-details | 9.9% value on Common O/S line |
| `est_date` / `six_month_date` / `nine_month_date` / `twelve_month_date` / `max_date` | spac-details | Yield matrix ROW LABELS (no longer rendered as a 5-line schedule) |
| **All yields** | **COMPUTED** | Every cell of the yield matrix, extension-adjusted — see "Yield Recalculation" and "Yield Matrix" |
| `ipo_date` | spac-details | IPO Date; anniversary for 8-K search |
| **Extension deposits** | **EDGAR 8-K** | Yield math; footer summary |
| **Thesis (3–4 sentences)** | **`read-memory-doc`** | Inside the code block, above `---` / ORDERS — see "Thesis Block" |

### Pre-deal only
| Field | Note Usage |
|-------|-----------|
| `liquidation_deadline` | Liquidation Deadline |
| `ipo_proceeds` | IPO proceeds ($mm) |
| `unit_ticker` / `units_position` | U Ticker / U Position |

### In-deal only
| Field | Note Usage |
|-------|-----------|
| `trust_balance` | Trust balance ($mm) |
| `target` | In deal with (strip "Announced: ") |
| `deal_announced` | Announced date |
| `deadline` / `outside_date` | Deadline / Outside Date |
| **`s/f-4s` (EDGAR-verified)** | **Replaces sheet `s4_amendments`** — computed via 3-pass EDGAR |
| `pipe_size` | PIPE size ($mm) — see "PIPE line" formatting rule. Rollout field — always render with `(per spac-insider)` disclaimer |
| `recommendation` / `notes` | Shown if present (cross-referenced with EDGAR findings) |

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

(Below the code block:)

Header line (plain text above the table):
`YIELD MATRIX — centered on VWAP = $X.XX, Bid = $X.XX, Ask = $X.XX; w/ extensions ($X.XX/sh/mo)`

Then the markdown table:

| Yield | −3c | −2c | −1c | VWAP | +1c | +2c | +3c | Bid | Ask |
|---|---|---|---|---|---|---|---|---|---|
| Price | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX |
| EST (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| 6 MON (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

```
Yields computed @ Tbill = X.XX% (USGG3M), mid = $X.XX
Extensions: $0.025/sh/mo (sponsor promissory note, active since mm/dd/yyyy)
```

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

(Below the code block:)

Header line (plain text above the table):
`YIELD MATRIX — centered on VWAP = $X.XX, Bid = $X.XX, Ask = $X.XX; w/ extensions ($X.XX/sh/mo)`

Then the markdown table:

| Yield | −3c | −2c | −1c | VWAP | +1c | +2c | +3c | Bid | Ask |
|---|---|---|---|---|---|---|---|---|---|
| Price | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX | $X.XX |
| EST (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| 6 MON (mm/dd/yyyy) | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% | #.##% |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

```
Yields computed @ Tbill = X.XX% (USGG3M), mid = $X.XX
Extensions: $X.XX/sh/mo (source), active since mm/dd/yyyy, N deposits to date
```

**CRITICAL**: The in-deal header's `s/f-4s` value comes from the EDGAR 3-pass workflow, NOT from `spac_details.s4_amendments`. Always suffix with `(EDGAR)`.

**CRITICAL**: The Unit line sits between Positions and Prices — near the positions.

**CRITICAL**: The Extensions footer line is included ONLY if extension deposits are non-zero. Omit entirely for pre-anniversary SPACs with no extensions.

**CRITICAL**: The `PIPE:` line is a rollout field — sourced from `spac-details.pipe_size` and ALWAYS suffixed with `(per spac-insider)` for now (sheet field origin disclaimer). Render even when `pipe_size = 0` so the reader knows the data was checked. See "PIPE line" formatting rule.

**CRITICAL**: The `Thesis:` line sits inside the code block, on the last content line before the `---` that precedes ORDERS. If the memory doc is missing or the fetch fails, render the fallback string per the "Thesis Block" section — never drop the line entirely.

---

## Formatting Rules

### Ticker validity — the suppression rule (governs Tickers / Positions / Prices lines)

A ticker is **invalid** if its value is `0`, `null`, empty, blank, or starts with `#N/A`. Invalid means "this instrument doesn't exist for this SPAC" (e.g. ATII has no rights → `rights_ticker = 0`). When a ticker is invalid, **SUPPRESS the corresponding field on every line** — the Tickers line, the Position line, AND the Prices line. Do NOT render `N/A` for the suppressed field; just drop it. The reader infers absence from absence.

Worked example — ATII (no rights, valid warrant ticker, zero warrant position):
- Tickers: `{ATII US Equity} {ATIIW US Equity}` (no rights bracket)
- Positions: `C Position: 179,043; W Position: 0` (no R Position field)
- Prices: `[ATII]: $10.76, [ATIIW]: $1.96` (no rights entry)

The Position line shows `0` (not `N/A`) when the ticker is valid but the holding is zero. **Invalid ticker → suppress; valid ticker + zero position → render `0`.**

### Tickers
- Wrap each valid ticker in `{TICKER US Equity}` for Bloomberg compatibility.
- See suppression rule above for invalid tickers.

### Positions
- Comma separators, no decimals: `135,532`.
- See suppression rule above. Valid-ticker / zero-position → `0`.
- Pre-deal includes U Position if a unit ticker exists; in-deal does not.

### Prices
- Source: live Bloomberg mid via `get-price`. Sheet prices are fallback.
- Format `$#,##0.00`. Standard half-up rounding for 2-decimal display ($10.755 → $10.76). All downstream computations (yields, C-T) use the unrounded mid; only the displayed price gets rounded.
- On the price line, wrap tickers in `[TICKER]`.
- Only show entries where ticker is valid AND a price is available.

### CIT and C-T
- CIT: `$#,##0.00`.
- C-T: computed as `mid − cash_in_trust`. Prefix with `+` or `-` before the `$`: `+$0.01` or `-$0.13`. Computation uses unrounded mid; the displayed 2-decimal value is half-up rounded.

### Trust Balance (in-deal only)
- `$#,##0.00mm` (millions, two decimals).

### In-Deal Target
- Strip `"Announced: "` prefix from `spac_details.target`. Show just the target name after `In deal with: `.

### Dom / UW / Bucket / Category line
- Render every field even if its value is null. **Null/missing → render `N/A`** for that field. Never suppress, never collapse the line. The reader needs to know the field was checked and not populated — silent suppression is indistinguishable from "the data is fine but the field was forgotten."
- Example with all four populated: `Dom: KY; UW: BTIG; Bucket: 2; Category: Quantum`
- Example with bucket/category null: `Dom: KY; UW: BTIG; Bucket: N/A; Category: N/A`

### Outside Date
- Use `spac_details.outside_date` ONLY. If null, render `N/A`. **Do not enrich** from memory doc, press releases, news, or the BCA — the line reflects the sheet state, not the world state.

### Position line vs memory doc
- `spac_details.*_position` fields are authoritative — always quote the sheet on the position line. Memory docs can reference older snapshots; that's expected, not a conflict.
- The thesis line MAY reference trajectory ("residual 472K, down from ~1.1M original") if the arc is load-bearing for the view. Otherwise skip it.

### Yield Matrix
- **Markdown table** with pipes and `|---|` separator row. NOT tab-separated, NOT fixed-width.
- Fixed column order: `Yield | −3c | −2c | −1c | VWAP` (or `Mid`) `| +1c | +2c | +3c | Bid | Ask`. No price-sorting.
- Two header rows above the data:
  1. Column labels (as above).
  2. `Price` row: actual dollar prices (`$10.27`) for each column.
- Row labels = scenario name + date: `EST (mm/dd/yyyy)`, `6 MON (...)`, etc.
- Cells formatted `#.##%`, extension-deposit-adjusted. Drop any row with days-to-exit ≤ 0 or missing date.
- See "Yield Matrix" section for full spec.

**The main note does NOT contain the 5-line EST/6MON/9MON/12MON/MAX yield schedule.** Yields live in the matrix only.

### Unit line
- Always render; `U=S` when no W or R.
- Slash notation per "Unit Structure Notation."

### Common O/S line
- Always render, on its own line directly below the CIT/C-T (pre-deal) or Trust balance/CIT/C-T (in-deal) line.
- Format: `Common O/S: [common_outstanding]; 9.9%: [pct_9_outstanding]`
- Both values comma-separated, no decimals (e.g. `23,000,000` and `2,277,000`).
- Source: `common_outstanding` and `pct_9_outstanding` from `spac-details`.
- If either value is missing/null/zero, render that side as `N/A`. Do not suppress the line.

### Thesis line
- Always render, on the last content line inside the code block before the `---` that precedes ORDERS.
- 3–4 sentences distilled from `MeteoraMCP:read-memory-doc(name, summary_only=true)` using the stage-bifurcated framework (pre-deal or in-deal) with calibration preserved — see "Thesis Block" section for full distillation rules, calibration rules, worked examples, and fallback cases.
- Missing doc: `Thesis: No memory doc exists for [TICKER].`
- Fetch error: `Thesis: Memory doc fetch failed — retry or check manually.`
- Never drop the line entirely — absence is information the reader needs.

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

### Footer (below both code blocks)

Always include the yield line:
```
Yields computed @ Tbill = X.XX% (USGG3M), mid = $X.XX
```

If T-bill fetch failed:
```
Yields computed @ Tbill = 3.66% (DEFAULT — live rate fetch failed), mid = $X.XX
```

If VWAP was invalid:
```
Matrix centered on mid — no valid 5d VWAP
```

If the VWAP center is materially stale relative to the live mid (|VWAP − mid| > $0.10), append one informational line so the reader knows the matrix anchor and the actionable spread are decoupled:
```
VWAP $X.XX vs mid $Y.YY — tape moved since 5d window; bid/ask cols anchor actionable levels
```
The matrix still centers on VWAP — don't fall back to mid. The bid/ask columns already give the actionable view.

If extensions are non-zero, add a second line:
```
Extensions: $X.XX/sh/mo (source), active since mm/dd/yyyy, N deposits to date
```

If extensions weren't found but should have been (post-anniversary, no 8-Ks):
```
⚠ No extension 8-Ks found despite post-anniversary window — verify manually
```

### Line suppression
Suppress any line where all values are blank, zero, null, or error. Never an empty line.

---

## ORDERS Section Formatting

Appended after a `---` divider inside the main code block. Fixed-width monospace. `WORKING` status filter only; if emsx-blotter is empty, omit the whole `---` / ORDERS block.

### The rendering algorithm — single deterministic recipe

Every row is built by string concatenation. There is no "outer padding" / "inner padding" / "centered header" ambiguity. Build each row by emitting these segments in order:

1. **Label prefix (6 chars):** `"SELL: "` (SELL header), `"BUY:  "` (BUY header), or `"      "` (6 spaces, every data row regardless of side).
2. **Contract field (20 chars):** left-justify the contract name, right-pad with spaces to exactly 20 chars. Python: `f"{name:<20}"`.
3. **For each subsequent column, in order:** emit the literal separator `" | "` (exactly 3 chars: space-pipe-space), then the cell content:
   - **Header row:** the column label, **left-justified, right-padded with spaces** to the column's character width. Python: `f"{label:<{width}}"`.
   - **Data row:** the data value, **right-justified, left-padded with spaces** to the column's character width. Python: `f"{value:>{width}}"`.

That's it. No outer padding around `" | "`, no centering, no per-column variation. The separator is always exactly 3 chars; the cell after it is exactly `width` chars. If you're tempted to add an extra space somewhere because the worked example "looks right," you are mis-reading the example — re-check by counting chars.

### Contract name
Strip stock symbol prefix, reformat date/strike (`10/16/2026 C9` → `Oct 16/26 C9`, `01/21/2028 C12.5` → `Jan 21/28 C12.5`). Pad to 20 chars (right-pad with spaces). Equity orders use the Bloomberg ticker directly (`KDK US Equity`, `ATII US Equity`). Names longer than 20 chars are not expected; if encountered, don't truncate — let the row run wide for that one line.

### Equity vs option share counts
Option orders show raw integer contract counts (`200`, `100`); equity orders use `k` notation. Round multiples drop the decimal (`25000 → 25k`); fractional thousands get one decimal (`22468 → 22.5k`, `4593 → 4.6k`); sub-1000 stays raw (`300 → 300`, `0 → 0`).

### Column widths — pick ONCE per block, no iteration
If any order in the block is an equity at $1+, use equity-mode widths for the entire block. Otherwise, use option-mode widths. ATIIW at $1.96 → equity-mode. PSQHW at $0.40 → treat as the option-block driver (sub-dollar warrant).

| Column | Option mode | Equity mode |
|---|---|---|
| Contract | 20 chars | 20 chars |
| Ord  | 4 (`9999`) | 5 (`55.4k` / `999k`) |
| Fill | 4 | 5 |
| Rem  | 4 | 5 |
| Avg  | 5 (`0.000`) | 6 (`10.723`) |
| Lmt  | 4 (`0.00`) | 5 (`10.95`) |

BUY block omits the Avg column entirely (header and data both). `--` in Avg if `avg_price` is zero — right-aligned within the column width (in equity-mode, `--` renders as `"    --"` in a 6-char column). If a single equity order exceeds 999k shares (rare), expand Ord/Fill/Rem to 6 chars.

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

The trailing spaces in the last header cell (`"Lmt  "`) are real — keep them.

**Option-mode block:**

```
SELL: Contract             | Ord  | Fill | Rem  | Avg   | Lmt 
      Jun 18/26 C9         |  200 |  107 |   93 | 0.529 | 0.55
      Jun 18/26 C10        |  100 |   26 |   74 | 0.512 | 0.40
BUY:  Contract             | Ord  | Fill | Rem  | Lmt 
      Jun 18/26 C10        |  100 |    0 |  100 | 0.05
```

Within each block, sort by expiry ascending then strike ascending (options) or limit price ascending (equity).

---

## Batch Mode

One note per ticker, separated by blank line and `---`. Single batched `get-price` call containing all common/warrant/rights tickers across every SPAC plus `"USGG3M Index"`. The T-bill rate is fetched once.

**EDGAR, 8-K extraction, and memory-doc reads must run per ticker.** Don't batch these. For a batch of N in-deal SPACs, that's N separate edgar-filings workflows, N separate 8-K extension searches, and N `read-memory-doc` calls. The EDGAR and 8-K calls are the bulk of the latency — this is the cost of the extended variant, and it's slower than the simple one. If the user needs fast output on a batch, steer them to `trading-note-simple`.

Each note gets its own yield matrix, its own s/f-4s (EDGAR), its own thesis block, its own extensions line, and the shared T-bill footer.

---

## What This Skill Does NOT Do

- Does not model trust leakage (taxes, WC). For leakage-adjusted yields, use `spac-yield-calc`.
- Does not read or trust `s4_amendments` from the sheet. The EDGAR 3-pass count replaces it entirely.
- Does not verify MCC, PIPE terms, or outside dates beyond what's in spac-details (for deeper in-deal diligence, use `spac-deal-review`).
- Does not prompt for Extensions, # Rights, # Public Shares, Notes, Recommendation, or Last s-4 (manual-entry fields in the VBA macro). The Extensions line is derived from EDGAR, not from user input. PIPE is now pulled from `spac-details.pipe_size` (rollout field — see "PIPE line" formatting rule).
- Does not fetch unit prices from Bloomberg.
- Does not replace the standard `trading-note-simple` for routine use — use simple when speed matters and extensions aren't material.
