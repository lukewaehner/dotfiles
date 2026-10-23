---
name: tear-sheet-fill-v2-10032026
description: "V2 of tear-sheet-fill: fills the Deal Notes text box on a Meteora merger-arb tearsheet (PRE DMA / POST DMA / Conditions). New in V2: Closing Guidance always carries the merging parties' own guidance (with source/date), a CHANGE note if that guidance has moved, and a one-sentence summary of the DMA's closing mechanic."
---

# Tearsheet Deal Notes fill — V2 (10/03/2026)

Fill the "Deal Notes" floating text box on a Meteora merger-arb tearsheet (.xlsx). Supersedes `tear-sheet-fill` (V1). Use whenever the user attaches/opens a tearsheet and asks to fill, update, or refresh the Deal Notes box, PRE DMA / POST DMA / Conditions, or does an "initial fill" — even if they only name the company.

**Standalone task.** Never gate on, chain after, or invoke antitrust-minute-1, dma-minute-1, hour-1, or other heavy deal-analysis modules. The research below is everything needed.

## What changed in V2
**Closing Guidance is mandatory and has three parts.** It was previously dropped or thin. Every has-DMA fill must include, in this order, in the single "Closing Guidance:" line:
1. **Parties' guidance** — the closing guidance that came directly from the merging parties (press release, 8-Ks, joint proxy, earnings calls/10-Q). Quote their wording, with source + date. Never use a desk or analyst estimate here.
2. **CHANGE note** — if the parties' guidance has changed at any time since announcement (e.g., "second half of 2026" -> "Q4 2026"), state the change: `CHANGE: narrowed/extended/delayed from '<old>' (<source, date>) to '<new>' (<source, date>)`. Re-check the 8-K / DEFA14A / 10-Q history on every run and every refresh; if unchanged, say "unchanged since announcement".
3. **DMA closing mechanic, one sentence** — summarize when the agreement requires closing, read from the agreement text (not the 8-K summary), with section ref. Example: "DMA timing: closing occurs no later than the 2nd business day after the last closing condition is satisfied/waived (Sec. 2.4)." Search the agreement for the Closing / Effective Time section. If no fixed timing, say so.

Example line: `- Closing Guidance: Parties' guidance: 'Q4 2026' (joint 8-K 09/30/26, after DOJ closed HSR). CHANGE: narrowed from 'second half of 2026' (02/09/26 PR; reaffirmed in 07/01/26 8-K). DMA timing: closing occurs no later than the 2nd business day after the last closing condition is satisfied/waived (Sec. 2.4), once Sanction Order is filed in Bermuda.`
If a guidance statement was not verified in a specific filing, do not cite that filing.

Done when: the Closing Guidance line contains all three parts and every date/source in it traces to a document you read.

## Step 1: Has a DMA been signed? Do not assume.
A tearsheet is often opened on rumor, activist, or strategic-alternatives situations. Check EDGAR/press for an 8-K (Item 1.01, or 2.01/5.01/8.01) announcing a definitive agreement with an Ex-2.1. If found: `has_dma = true`, fill everything. If only rumors, activist 13D, strategic review, LOI: `has_dma = false`; put everything in PRE DMA and write POST DMA / Conditions as "N/A - No DMA/merger agreement signed as of the date of this tearsheet." Never invent terms.
Done when: has_dma decided from a primary filing.

## Step 2: Research order
1. Identify target/acquirer from the user message and the tearsheet (ticker cells, deal-terms cells).
2. Pull the merger agreement text (Ex-2.1). **Agreement text controls over any 8-K narrative** on fees, triggers, efforts, specific performance, closing mechanics. Don't write a discrepancy memo; just use the agreement.
3. Read the 8-K / press release / deck for narrative, board-approval language, advisors, premium, and the parties' closing guidance.
4. Pull prior 8-Ks, proxy "Background of the Merger", and news across the run-up for PRE DMA: prior approaches, activists, strategic reviews, management changes, financing. Oldest first.
5. Check ArbJournal (semantic-search, namespace arbjournal) if available; if there is no coverage, say so — never claim it. Check recent 8-Ks/DEFA14A/proxy for regulatory filing/clearance updates and for any change in closing guidance.
Done when: each POST DMA/Conditions field traces to a document you read.

## Step 3: Content and voice (terse trading-desk style)
- **PRE DMA:** `-MM/DD/YY: short sentence`; combine same-day/related facts with semicolons.
- **POST DMA** fields, in order, each `- Label: text`: Date (announcement date + parties/tickers/consideration/structure/board approval); Closing Guidance (see V2 rules above); Transaction Value ($, premium with date+price, multiple); Go-Shop; Excluded Party; Target Dividends; Acquirer Dividends; Dividend Coordination; Confidentiality Agreement (date); Financing (lead Yes/No); Marketing Period; Company Termination Fee ($mm, % equity value, trigger, expense reimbursement); Reverse Termination Fee (same; note any regulatory reverse fee or lack); Walk Date (initial + automatic extensions); DMA Best Efforts; Specific Performance. Use "N/A" where it doesn't apply; omit a field you can't source rather than guess. Cite section numbers and exact figures.
- **Conditions:** Target Sh Approval (required vote; sub-bullets: voting agreements, prelim proxy status); Acquirer Sh Approval ("N/A" if none; same sub-bullets); Regulatory Approvals — one line per regulator `Regulator: detail` with filed/expected/cleared dates. Always include HSR (even "not applicable"). Cross-check recent 8-Ks for updates after signing.
- **Red flag (bold red line):** only if the acquirer is a strategic public operating company and neither party's docs mention unanimous board approval; flag text `NO MENTION OF UNANIMOUS BOARD APPROVAL BY [NAME]`. Never flag a private/PE acquirer's silence.
- **Green (hell-or-high-water):** only if the efforts covenant truly has no cap on divestitures/conduct remedies (read the Burdensome Condition-type definition). Most deals are not.

## Step 4: Write to the workbook
The Deal Notes box is a floating shape (e.g. "TextBox 1" on the "Tearsheet Template" sheet), not a cell. In the Excel add-in: use execute_office_js, set `sheet.shapes.getItem(<name>).textFrame.textRange.text`, then set font size (default 8pt for a full has-DMA fill; larger for no-DMA), and bold the section headings (PRE DMA, POST DMA, Conditions) and every field label via `getSubstring(start,len).font.bold`. Find label offsets from the read-back text (labels containing hyphens, e.g. "Go-Shop:", need explicit handling). Use green (#00B050) only for the HoHW flag and red (#FF0000) only for the board-approval flag; if rich-text colors are not possible, use plain markers `[HELL-OR-HIGH-WATER]` / `[FLAG: ...]`. The template prints a typo "Targer Sh Approval" — write "Target Sh Approval". With shell/Python access and the V1 script, that path is also valid.
If the user asks for a targeted edit (one line), read the live text, replace only that line, and re-apply bold to its label.

## Step 5: Verify
Read back the text, and render the sheet range (`getRange(...).getImage()`) to confirm nothing runs into the chart anchored below the box (the box does not auto-grow). Underlines in the render are a renderer artifact if font.underline reads null. Confirm the Closing Guidance line has all three parts. State what you verified and what you did not (e.g., items not re-confirmed such as foreign antitrust clearances).

## Step 6: Report
One short note: has-DMA or no-DMA branch, any flags applied or not, closing guidance and any CHANGE noted, and anything unverified.
