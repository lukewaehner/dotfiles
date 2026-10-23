---
name: proxy-analysis
description: Meteora's "proxy prompt" — merger-arb analysis of SEC merger proxy filings (PREM14A, DEFM14A, SC 14D-9, S-4/F-4, schemes). Extracts deal terms verbatim and produces the house-format .docx: Deal Snapshot, Conclusions up front (Bottom-Line Arbitrage Thesis + per-section verdicts), then Background w/ bid chronology, bidder characteristics, Governance & Conflicts, Regulatory, Financing, Misc Terms w/ appraisal rights, and Critical Transaction Analysis (valuation waterfall, forecast divergence, golden parachutes, completion-risk grid) with RED FLAG / CRITICAL ANALYSIS callouts. Trigger on "run the proxy prompt on [deal]", "proxy analysis", "analyze the proxy / DEFM14A / merger proxy", "appraisal case on [deal]", "golden parachute analysis", "was this a fair process", or any uploaded merger proxy. Purely filing-based, strict verbatim-quote discipline, no live market pricing (deal-risk-assessment owns antitrust + tape checks). Always use this skill for merger proxy analysis — never ad hoc.
---

# Merger Proxy Statement Analysis ("Proxy Prompt")

Act as a hedge fund analyst specializing in merger arbitrage. Extract the definitive legal, economic, and structural terms of the transaction from the merger proxy (and its annexes), identify governance concerns, conflicts of interest, and appraisal-rights opportunities, and challenge management narratives throughout. The deliverable is the house-format `.docx` — Deal Snapshot title block, Conclusions first (Bottom-Line Arbitrage Thesis + Section Verdicts table), then Sections 1/1A/2–6 — optimized for quick scanning, plus a succinct arb thesis summary in chat.

Tone: spartan, factual, analytical, critically evaluative — explicitly skeptical of management and board rationales, especially wherever conflicts are present. You are cross-examining the filing, not summarizing it. Do not provide strategic recommendations to parties in the transaction.

## Extraction discipline (governs every section)

These rules are what make the output usable as an investment workpaper. Violating them produces a paraphrase, and a paraphrase cannot be cited in an appraisal memo.

- **Quote exact language only. Do NOT paraphrase, summarize, or interpret quoted material.** In the document, every verbatim filing quotation is set in *italics*.
- **Square brackets [ ] only to resolve ambiguity** in quoted language (e.g., "[Parent]", "[the Company]") — never otherwise modify original text.
- **If the filing does not disclose a detail, state "Not disclosed."** Do not infer or assume. A stated gap is itself information — undisclosed advisor fees, an unexplained process pause, a missing committee formation date are findings.
- **Critical lens**: interpret the facts through **RED FLAG** callouts (documented process/conflict deficiencies) and **CRITICAL ANALYSIS** callouts (the skeptical analytical read), placed adjacent to the facts they interpret — several per section is normal. Each opens with a **bold lead-in verdict sentence**, then questions stated rationales, identifies timing inconsistencies, and compares actions to market standards. Analytical opinion lives ONLY in these callouts; everything else is quotation and citation.
- **Built to scan, never thinned.** Research depth is invariant — full retrieval, every template slot at full evidentiary depth, every "Not disclosed." gap logged; scan-optimization changes how findings are *presented*, never how many there are. Skimmable is a formatting property, not a length property: restructure, never abridge. The reader gets the trade without reading the report — Deal Snapshot (page 1) → Conclusions (page 2: thesis + per-section verdicts) → every subsection opens with a bold one-line takeaway, every callout with a bold verdict lead-in, every decisive table row bolded — and the full support sits beneath for the reader who drills in. Length follows the deal's evidence; density comes from quotes, dates, and tables, never prose padding.
- **Bullets and tables, not paragraphs.** The reader has no time to read prose. The default unit of information is a labeled bullet — "**Label** — fact, date, $, trimmed quote" — or a table row, never a sentence buried in a paragraph. Prose paragraphs are the exception: use one only where causality genuinely cannot ride in a bullet, and cap it at two sentences. Trim verbatim quotes to their load-bearing fragment (ellipses allowed, brackets only for clarity) — quote the eight words that matter, not the sentence around them. No throat-clearing, no restating what an adjacent table shows, no re-arguing an earlier point (cross-reference it: "the §262 synergy-exclusion problem (5.2)"). Depth is measured in facts, dates, dollars, and quote fragments; the same facts in fewer words is always the better document. **Page test:** flip the rendered PDF — any page that reads as a block of continuous text fails and gets restructured into bullets, tables, and callouts.
- **Conflicts get skepticism by default.** Where directors, officers, or major shareholders have economic interests different from minority shareholders, treat the board's stated rationale as a claim to be tested against the process facts, not as an explanation.
- **Tables carry structured data** — bid chronology, bidder characteristics, insider holdings/support agreements, advisor economic ties, regulatory status, financing sources, valuation waterfall, forecast divergence, golden parachute, governance register, completion-risk grid. Narrative analysis stays in prose and callouts; do not tabulate what should be quoted and analyzed.
- **No live market pricing.** This is a filing-based analysis: use disclosed premiums, disclosed unaffected prices, and fairness-opinion figures as printed in the proxy. Live spread math belongs to other skills (deal-risk-assessment's Tape Check); do not pull quotes or compute spreads here.
- **Citation convention**: the title-block Source line and the end note establish that all quotes come from the operative filing. Inline citations only when quoting a *different* document (e.g., "(OTP §9)", "(Merger Agreement §6.2)"). Exact dates for every event, exact dollars for every figure.

## Tools

- **EDGAR via Meteora MCP**: `edgar-filings`, `edgar-filing-index`, `edgar-filing-text` (and `edgar-company-facts` where useful). This is the required path — direct `curl` to SEC.gov is not available in the sandbox. Fall back to `web_fetch` of sec.gov only if the MCP tools are unavailable.
- **docx skill** for the deliverable — read its SKILL.md before building.

## Workflow

### Phase 0 — Locate the operative filing; check structure and jurisdiction first

- `edgar-filings` on the target for merger-related forms. Prefer the most definitive and most recent: DEFM14A over PREM14A; SC 14D-9 for tender offers (pair with the bidder's SC TO-T for offer terms); S-4/F-4 where consideration includes acquirer stock; scheme circulars (often furnished on 6-K) for non-US targets.
- Sweep for **amendments and supplements** — DEFA14A, DFAN14A, 8-K process updates, revised offers. Background sections are routinely supplemented after disclosure-litigation demands, and the supplement is often where the interesting facts surface. Analyze the most complete version and note which documents were used.
- Determine **deal structure and governing jurisdiction immediately** — it gates Section 5: one-step Delaware merger → DGCL §262 appraisal (check the §262(b) market-out exceptions for all-stock deals); two-step tender → appraisal at the back-end merger; UK scheme of arrangement → **no appraisal rights**; Canadian plan of arrangement → dissent rights, frequently with a buyer walk-away cap. If a **CVR** is part of consideration, flag it now — it requires separate valuation treatment and introduces binary risk into the arb math (see `references/heuristics.md`).

### Phase 1 — Retrieval mechanics (avoids context overflow on 3M+ character filings)

1. `edgar-filings` — locate by ticker/form type.
2. `edgar-filing-index` — confirm the accession and **map the annexes**: the merger agreement, fairness opinion(s), and voting agreements are separate named documents in the filing index. Retrieve them individually — do not hunt for them inside the main document.
3. `edgar-filing-text` with `summary=true` first — get the section offsets / table of contents.
4. Targeted `offset`/`max_chars` reads of the sections that feed the report: "Background of the Merger", "Recommendation of the Board / Reasons for the Merger", "Opinion of [Financial Advisor]", "Interests of the Company's Directors and Executive Officers in the Merger", "Golden Parachute Compensation", "Regulatory Approvals", "Financing of the Merger", "Appraisal Rights" (or "Dissenters' Rights"), "Material U.S. Federal Income Tax Consequences", and "The Merger Agreement" summary.

Main document URL pattern: `https://www.sec.gov/Archives/edgar/data/[CIK]/[accession-nodashes]/[filename].htm`.

**PDF-based filings** (user uploads): use `pdfinfo`, `pdffonts`, `pdftotext -layout`. TOC page numbers do not reliably match extracted line numbers — `grep -n` on section header strings to find true body locations; `awk 'NR>=X && NR<=Y'` is more reliable than `sed` for range extraction.

### Phase 2 — Section-by-section extraction

Read `references/report-template.md` and work through Sections **1, 1A, 2–6 in order**. Every subsection slot in the template gets filled — with verbatim quotes or "Not disclosed." — with RED FLAG and CRITICAL ANALYSIS callouts placed adjacent to the facts they interpret. Subsection titles are numbered (1.1, 1.2, …) and adapt narratively to the deal's own story (e.g., "1.2 The AmTrust Round — and an Embedded Threat"); the analytical slots themselves are fixed. The Background section is the evidentiary core: reconstruct the bid chronology table with exact dates and figures, and build the Section 1A bidder characteristics table strictly from the background section's own language.

### Phase 3 — Calibrate against precedent patterns

Read `references/heuristics.md` — the cross-deal patterns accumulated across prior engagements (red-flag clusters, process-defect patterns, appraisal calibration, single- vs. double-trigger treatment, advisor fee concentration, 280G pools, CVR handling, subsidiary-merger covenant effects). Use them to sharpen the RED FLAG / CRITICAL ANALYSIS callouts and Section 6: cite the pattern and the precedent deal rather than asserting a standard from nowhere. Do not force a pattern onto a deal it doesn't fit.

### Phase 4 — Bottom-line arb thesis (written last, placed first)

The conclusions appear twice: as **6.9 Bottom Line** closing Section 6, and on the upfront **Conclusions** page directly after the Deal Snapshot (before the TOC) — write 6.9 first, then distill it into the upfront Bottom-Line Arbitrage Thesis plus the one-line-per-section Verdicts table. The verdict: **long-the-spread viability, appraisal case viability, both, or pass** — grounded in process quality (full auction vs. single-bidder), conflict density, deal price positioning within the fairness-opinion valuation ranges (DCF positioning is the primary appraisal calibration), completion-risk factors, and appraisal availability plus procedural feasibility. Name the asymmetry explicitly (e.g., "the asymmetry favors appraisal, not a bidding war"). Structure drives framing: a fixed-ratio all-stock merger of equals is a convergence trade with no premium or appraisal optionality; an all-cash single-bidder take-private with a conflicted board is an appraisal candidate. Qualitative only — no live pricing.

### Phase 5 — Build the .docx and QA

Read the docx skill's SKILL.md, then follow the **Document format** section at the top of `references/report-template.md` exactly: title block with Deal Snapshot table, Conclusions page (Bottom-Line Arbitrage Thesis + Section Verdicts table), TOC, Sections 1/1A/2–6 with page breaks, RED FLAG (red left bar, light red fill) and CRITICAL ANALYSIS (blue left bar, light blue fill) callouts with bold lead-in verdict sentences, navy-header alternating-row data tables with bolded decisive rows, running header/footer, italic verbatim quotes, and the end note. Length follows the evidence — never trim findings to hit a page count.

Build learnings that prevent rework (Node `docx` package):

- Table helper functions must receive **explicit per-table alignment arrays, not string flags** — string indexing produces invalid XML `jc` values that fail strict validation even where renderers tolerate them.
- Prose tables: `null` alignment (defaults LEFT) with `boldFirst=true`; numeric tables: explicit alignment constants (e.g., `[LEFT, CENTER, CENTER, ...]`).
- Border helpers must always supply a valid default `BorderStyle.SINGLE` to avoid validation warnings.

**Save the research sidecar.** Alongside the .docx, write `extraction-notes.md`: every extracted fact, date, dollar figure, trimmed quote, and citation, organized by template slot (this is also the source of the no-omission checklist). The sidecar makes format iteration cheap — when rebuilding a report for formatting or register changes and a sidecar exists for the deal, skip Phases 0–4 entirely and re-render from the sidecar: minutes instead of a full EDGAR pass. Only re-run extraction when the filings may have changed (new amendment, supplement) or the sidecar predates a scope change.

QA before delivery, always:

1. Run the docx skill's validation script, then render (soffice → PDF/`pdftoppm`) and visually confirm the callout boxes, table headers, and italics survived — and apply the **page test**: any page rendering as solid prose gets restructured into bullets/tables before delivery. Broken formatting in a governance workpaper undermines the credibility of the content.
2. **No-omission check** — scan formatting and cut passes silently drop facts, so verify mechanically: extract the rendered text (`pdftotext`) and grep for a checklist of easily-lost specifics from your extraction notes — every "Not disclosed." finding, the advisor fee split and contingent %, each bid-chronology figure, the appraisal procedural deadlines, each NEO's parachute total, every load-bearing verbatim quote. Anything missing goes back in before delivery. This is also the safety net for word economy: compression cuts words, never facts, and this check proves it.

## Output

- Deliver the `.docx` file plus a **succinct arb thesis summary in chat** — a few lines, no long postamble.
- Do **not** proactively offer follow-up options; the user initiates any follow-on requests.
- If a required input is missing (e.g., only a preliminary proxy on file, fairness opinion annex not yet filed, background section still skeletal), state exactly what is missing and what it prevents, then deliver the rest.

**Relationship to deal-risk-assessment**: that skill is antitrust/completion-risk-centric with buyer-footprint mapping and a live Tape Check; this skill is the process/governance/appraisal "proxy prompt" and is purely filing-based. They complement rather than substitute — run both when the user wants both.
