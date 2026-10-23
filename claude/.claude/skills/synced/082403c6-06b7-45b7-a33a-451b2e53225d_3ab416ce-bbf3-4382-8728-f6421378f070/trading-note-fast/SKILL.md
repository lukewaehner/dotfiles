---
name: trading-note-fast
description: >
  Generate a SPAC trading note FAST — live Bloomberg prices, live-recomputed yields (mid + USGG3M), a VWAP-centered yield matrix (±1c/±2c/±3c plus bid/ask), live EMSX orders, a `Thesis:` line, a `Non-Managing Members:` line, and extension-adjusted yields — taking all research content (s/f-4 count, extension terms, non-managing economics, thesis) from the Meteora memory doc, not live research. A bundled script (scripts/render_note.py) does all math and formatting; the model only fetches the four Meteora MCP payloads and distills the thesis. Does NOT hit EDGAR, verify S-4/F-4 counts, or extract 8-Ks. Trigger on 'fast note', 'quick note', 'doc note', 'note from the doc', 'fast trading note', 'note for [ticker] fast', or any trading-note request where speed matters and the doc is trusted as current. Unit renders `U=S+W/2+R/10` or `U=S`. For an EDGAR-verified S-4/F-4 count use `trading-note-simple`; for 8-K-verified extension extraction use `trading-note-extended`.
---

# Trading Note — Fast Variant

Generate a formatted SPAC position note FAST. **All math and all formatting live in a bundled script** (`scripts/render_note.py`); the model's only job is to fetch four Meteora MCP payloads and distill the `Thesis:` / `Non-Managing Members:` / `s/f-4s` / extension fields from the memory doc, then run the script and print its output verbatim. This is what makes the variant fast — the model never computes a yield or pads a table cell by hand.

It trusts the memory doc as the system of record for everything that would otherwise need research (in-deal S-4/F-4 count, extension-deposit terms, deal/structure color, sponsor non-managing economics, thesis). It still pulls the live tape: prices (`get-price`), positions/trust/dates (`spac-details`), orders (`emsx-blotter`). It does **NOT** call EDGAR, run the 3-pass S-4/F-4 verification, or extract 8-Ks. Extension deposits ARE modeled into yields — but from doc-recorded terms (labeled `per memory doc`), never from 8-Ks.

- For an **EDGAR-verified** S-4/F-4 count → `trading-note-simple`.
- For **8-K-verified** extension extraction → `trading-note-extended`.

All MCP tools are the **Meteora MCP connector** tools: `spac-details`, `get-price`, `emsx-blotter`, `read-memory-doc`.

---

## Workflow (fast path — 4 calls + 1 script)

1. **`spac-details`** with the requested ticker → positions, trust, deadlines, scenario dates, `vwap_5d`, unit structure, warrant/rights tickers, `stage`.

2. **In ONE parallel batch** (do not serialize these):
   - **`get-price`** with `tickers` = every valid security ticker (common, warrant, rights) **plus `"USGG3M Index"`**. One batched call. (Ticker format: slash-warrants like `ALUB/WS` → pass `ALUB/WS US Equity`; plain warrants/rights `KDKRW`/`IPCXR` → as-is; skip any ticker that is `0`/null/`#N/A`.)
   - **`emsx-blotter`** with `ticker` = base ticker.
   - **`read-memory-doc`** with `name` = base ticker, `summary_only=true`. **This single fetch feeds the thesis, the Non-Managing Members line, the in-deal s/f-4 count, and the extension terms.** Call it once; never twice, never go to EDGAR.

3. **Distill from the memory doc summary** (the ONLY judgment step — see `references/thesis.md` for full frameworks, rules, and worked examples):
   - `thesis` — 3–4 sentences, stage-bifurcated (pre-deal vs in-deal), sourced EXCLUSIVELY from the Executive Summary. If no doc → `No memory doc exists for [TICKER].`; if fetch errors → `Memory doc fetch failed — retry or check manually.`
   - `non_managing_members` — one tight clause on the sponsor LLC's managing/non-managing economics; `""` if the doc is silent, `none — wholly principal-funded` if the doc confirms no pass-through.
   - `sf4_count` (in-deal only) — the registration-statement count the doc records, as a string like `2 (per memory doc)`; `null` if the doc has no count (script renders `not in doc`).
   - `ext_per_share_per_month` — the per-share monthly deposit the doc records (`0` if none). Convert a flat monthly cap with `monthly_cap / public_shares`. Set `ext_silent=true` only when the name is in-deal/post-anniversary AND the doc is silent on extensions (script prints the deferral flag). See `references/thesis.md` → "Extension terms".

4. **Build the input JSON and run the script** (see "Running the script" below). The script does price selection, C-T, the yield matrix, the ORDERS table, all suppression, and the footer.

5. **Print the script's stdout verbatim.** That is the complete note (note block + yield matrix + footer). Do not reformat or recompute anything.

**Batch requests:** one `spac-details`, `emsx-blotter`, `read-memory-doc` per ticker, but a **single** `get-price` covering every ticker across all names plus `"USGG3M Index"`. Run the script once per ticker; separate notes with a blank line and `---`. There is no EDGAR step — that is why this variant is fast on batches.

---

## Running the script

Assemble one JSON bundle and pass it to the script. Stdlib only — no installs.

```bash
python3 scripts/render_note.py input.json      # or: cat input.json | python3 scripts/render_note.py
```

`input.json` shape (full spec in `references/input_schema.md`):

```json
{
  "ticker": "IPCX",
  "today": "2026-06-26",
  "thesis": "….",
  "non_managing_members": "….",
  "sf4_count": "2 (per memory doc)",
  "ext_per_share_per_month": 0,
  "ext_active_since": null,
  "ext_deposits_to_date": null,
  "ext_lump_period_days": null,
  "ext_silent": false,
  "spac_details": { <raw spac-details payload> },
  "prices":  { <raw get-price payload, incl. results[] and market_status> },
  "orders":  { <raw emsx-blotter payload, incl. orders[]> }
}
```

Pass the **raw** MCP payloads through untouched — the script matches price rows by ticker, reads `market_status`, and ignores nested route data. For batch, you may pass the one shared `get-price` payload to every ticker's bundle; the script picks the right rows.

---

## What the script handles (so you don't have to)

Everything deterministic, exactly per the locked Meteora spec (audit detail in `references/spec.md`):

- **Price selection ladder** — mid when reliable, `last_trade` when mid fails the reliability tests (wide spread / stub size / off-hours drift / stale), sheet price last resort. Relaxed thresholds for sub-dollar warrants/rights. Footer flags any `last_trade` substitution.
- **C-T** = selected common price − CIT (signed), off the unrounded selected price.
- **Unit notation** — `U=S+W/n+R/m` from `warrants_in_unit` / `rights_in_unit`.
- **VWAP-centered yield matrix** — center on `vwap_5d` (fallback to selected common price, label `Px`); fixed `−3c…+3c, Bid, Ask` columns; rows = scenario dates with days-to-exit > 0; coincident-date dedup (`EST/MAX`); extension-adjusted, simple-annualized yields; markdown table (Bloomberg-pasteable).
- **ORDERS** — `WORKING` only, SELL/BUY blocks, fixed-width columns, equity k-notation vs option raw counts, contract-name reformat, BUY omits Avg.
- **Suppression** — invalid ticker (`0`/null/`#N/A`) drops that instrument from the Tickers / Positions / Prices lines; `N/A` vs `0` rules; null Dom/UW/Bucket/Category → `N/A`.
- **Footer** — Tbill line (with default-rate flag), Extensions line (per memory doc), VWAP-stale flag.

You provide only the four payloads and the four distilled fields. If you find yourself reasoning about padding, yields, or which price to use, stop — that is the script's job.

---

## Output shape (produced by the script)

A fenced note block (header → unit → prices → CIT/C-T → O/S → in-deal/pre-deal lines → `Non-Managing Members:` → `Thesis:` → `---` → `ORDERS`), then the `YIELD MATRIX` header line + markdown table, then a fenced footer block. Pre-deal uses `Domicile:` and includes `IPO proceeds` / `Liquidation Deadline` / optional `U Position`; in-deal uses `Dom:` and includes `Trust balance` / `In deal with` / `PIPE: … (per spac-insider)` / `Announced` / `Deadline` + `Outside Date` / `s/f-4s: … (per memory doc)`.

---

## What this skill does NOT do

- No EDGAR, no S-4/F-4 verification (count comes from the doc, labeled `(per memory doc)`; `not in doc` if absent).
- No 8-K extension extraction (deposit terms come from the doc; yields are still extension-adjusted, labeled `(per memory doc)`; `ext_silent=true` prints a deferral flag).
- No web search, no filings reads, no first-principles reconstruction. Everything that isn't live tape comes from the memory doc.
- No trust-leakage modeling (use `spac-yield-calc`). Never reads `s4_amendments`, `notes`, or `recommendation` from the sheet.
