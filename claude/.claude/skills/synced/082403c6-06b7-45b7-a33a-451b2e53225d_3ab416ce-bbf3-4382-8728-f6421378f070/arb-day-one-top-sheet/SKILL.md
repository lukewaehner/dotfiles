---
name: "arb-day-one-top-sheet"
description: "One-page verbatim terms sheet for a newly announced merger — parties, consideration, premium, financing, break fees, outside date, efforts standard, approvals, vote threshold, expected closing — every line a direct quote with its source cite. Trigger on \"top sheet on [TICKER]\", \"terms sheet\", \"what are the terms\", \"run day one on [TICKER]\", or a just-announced deal. Ticker-only input; reads the 8-K, press release, and merger agreement directly. EXTRACTION ONLY — produces no view, no call, no completion probability, and never characterizes a term as favorable, tight, or unusual."
---

# Day-One Top Sheet — Verbatim Terms

One of three independent day-of skills that run on a merger announcement. This skill has
exactly one job: put the announced terms in front of the trader, verbatim, with every line
traceable to its source.

**This is a terms sheet, not a summary.** It replaces the trader's own skim of the 8-K.
It does not replace the trader's judgment, and it must not attempt to.

**Independence rule — critical.** This skill does NOT read the output of
`arb-dma-extraction` or `arb-deal-antitrust-initial`, and they do not read this one. It
goes to the source filings itself. All three run in parallel with no dependencies.

---

## Prohibited output — read this before anything else

This skill produces **no view**. The following never appear in its output, in any form,
however hedged:

- Completion probability, odds, or likelihood of closing
- A lean-in / watch / pass call, or any recommendation
- Risk ranking, or a list of "what could break this"
- Characterization of any term as favorable, unfavorable, tight, loose, weak, strong,
  generous, standard, market, off-market, unusual, or aggressive
- Comparison to precedent transactions or to what is typical
- Spread, price, or anything about where the target trades
- Words like "suggests", "indicates", "notably", "importantly", "signals", or "which
  means" attached to a term

If a sentence would not survive being read aloud in a deposition as a quotation from a
filing, it does not belong in this document. The trader supplies every interpretation.

---

## Input

The trader supplies a **ticker only**.

### Retrieval sequence

1. Resolve the ticker to the target and acquirer.
2. `edgar-filings` → the merger 8-K (Item 1.01) and its press release exhibit (EX-99.1).
   `extract-8k` where available.
3. `edgar-filing-index` → check for the merger agreement exhibit (normally EX-2.1). If
   present, `edgar-filing-text` it and prefer it as the source for every term it covers.

**Source precedence.** Where the agreement and the press release both address a term, quote
the **agreement** and cite it. Where only the press release covers it, quote the press
release and mark the line `[per press release — agreement not yet filed]`. If the agreement
is filed later and its language differs from the release, that discrepancy is itself a
fact worth surfacing on a re-run — show both, cite both, say nothing further about it.

---

## Output

A single one-page `.docx` in the deal folder, named
`[TICKER] Top Sheet [YYYY.MM.DD].docx`. Use the `docx` skill.

### Header stub (shared across all three day-of skills)

```
Ticker:      [TICKER]
Deal:        [Acquirer] / [Target]
Skill:       arb-day-one-top-sheet
Run:         [YYYY-MM-DD HH:MM ET]
Sources:     [filing type, accession number, exhibit] for each document read
Key Findings:
  · [five bullets — the five highest-value quoted terms, each with its cite]
```

### The fields

Every field renders as: **quoted language** — then its source cite in the form
`8-K Item 1.01` / `DMA §5.4 p.62` / `PR ¶3`.

| # | Field |
|---|---|
| 1 | Parties — exact legal entities, target and acquirer |
| 2 | Transaction structure (one-step merger, two-step tender, stock-for-stock, etc.) |
| 3 | Consideration per share |
| 4 | Total equity value / enterprise value **as stated** |
| 5 | Premium **as stated in the release**, including the reference price and date it is measured against |
| 6 | Financing sources and amounts as stated |
| 7 | Company termination fee — amount, and as % of deal value with the work shown |
| 8 | Reverse / parent termination fee — amount, and as % of deal value with the work shown |
| 9 | Regulatory termination fee, if any |
| 10 | Outside date, and any extension rights |
| 11 | Efforts covenant standard — quoted exactly |
| 12 | Required approvals as listed (antitrust, CFIUS, sector regulators, foreign) |
| 13 | Shareholder vote threshold |
| 14 | Support / voting agreements — parties and % committed |
| 15 | Go-shop / no-shop — existence and stated window |
| 16 | Marketing period — existence and stated duration |
| 17 | Expected closing **as stated by the parties** |
| 18 | Interim dividend treatment |
| 19 | MAE definition location and carve-out count (pointer only — full text is the DMA extraction's job) |

**Not disclosed.** Where a field is not addressed in any source read, the line reads
exactly `Not disclosed.` and nothing more. Do not speculate why. Do not note that it is
unusual to omit.

### Permitted computation — the only two

1. **Date arithmetic** on quoted dates: *"Outside date 3/25/2027; 12 months from signing
   3/25/2026."* Also flag any quoted deadline that has already passed as of the run date.
2. **Fee as a percentage of deal value**, with the arithmetic shown: *"$142,000,000 ÷
   $4,100,000,000 = 3.46%."*

Both operate purely on quoted inputs. Nothing else is computed. In particular, do not
re-derive the premium — quote the premium the parties stated, along with their reference
price.

---

## Operating notes

**Length.** One page. If the terms genuinely overflow, let it run to two rather than
dropping fields — but never pad, and never add narrative to fill.

**Bold the answer inside the quote**, as in the DMA extraction convention: quote the full
responsive sentence, bold the operative number or phrase within it. The trader's eye
should land on the figure without losing the language around it.

**No agreement on file.** This skill still runs — the press release and 8-K carry most of
these fields. Mark each affected line `[per press release — agreement not yet filed]` and
note at the foot of the document that the agreement had not been filed as of the run time.
This is the one day-of skill that always produces something useful.

**Speed is the point.** This should be the fastest of the three. Do not open the target's
10-K, do not search for precedents, do not look at the tape. Read the announcement
documents, quote them, stop.

