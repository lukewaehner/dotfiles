---
name: "arb-deal-antitrust-v2"
description: "Day-of merger arb antitrust and overlap screen on a newly announced deal — acquirer portfolio/overlap mapping, market definition and concentration, competitive effects, target capital structure, litigation and fraud risk, valuation and precedents, stakeholder analysis, all EDGAR-cited. Produces Meteora's full gold-standard 12-section report (front-matter Risk Matrix, closing Deal Completion Probability Decomposition with a directional HIGH/MODERATE/LOW read) in the same house format as the CBZ/Grant Thornton and ZYME/TBPH reports. Trigger on \"run the antitrust screen v2 on [TICKER]\", \"run the v2 deal screen\", \"overlap screen on [TICKER]\", \"run day one on [TICKER]\", or a newly announced merger. Ticker-only input — pulls the 8-K, press release, and EDGAR filings itself. Produces one .docx. Never estimates market shares, HHI, or probabilities without sourced data — the directional read is always qualitative and precedent-grounded, never a fabricated percentage."
---

# Initial Deal & Antitrust Screen — Day-Of (v2)

One of three independent day-of skills that run on a merger announcement. This skill has
exactly one job: the overlap, market-structure, and deal-risk screen off the announcement
and EDGAR.

**Independence rule — critical.** This skill does NOT read the output of
`arb-dma-extraction` or `arb-day-one-top-sheet`, and they do not read this one. All three
go to the source filings directly and run in parallel. Never wait on, reference, or
reconcile against a sibling skill's output.

**Boundary with `arb-dma-extraction`.** That skill owns every merger-agreement term
verbatim. This skill's "Deal Structure and Terms" section reads terms from the 8-K and
press release for context and does not attempt a clause-level extraction of the agreement.
This skill's territory is the market, the portfolio, the competitors, the target's
financial condition, and the litigation picture.

---

## Input

The trader supplies a **ticker only**. Everything else is retrieved.

### Retrieval sequence

1. Resolve the ticker to the target company and CIK. Identify the acquirer and classify it:
   **PE sponsor / strategic / hybrid-consortium.** The portfolio-context sections below are
   built for sponsors; for a strategic acquirer, apply the same overlap logic to the
   acquirer's own business segments and disclosed competitors. State the classification
   plainly (e.g. "Buyer classification: HYBRID") — Section 4 of the report leads with it.
2. `edgar-filings` → the merger 8-K and its press release exhibit (EX-99.1).
3. `extract-8k` where available for a fast structured read of the announcement.
4. Target's latest **10-K and 10-Q** — Competition section, segment reporting (product,
   geographic, customer type), MD&A, legal proceedings, capital structure and debt notes.
5. Acquirer's EDGAR filings where it is a public filer; for a sponsor, its portfolio
   companies' filings.
6. `semantic-search` against the **ArbJournal / Chain Bridge Research** vector index for
   precedent transactions with comparable structure, sector, and regulatory posture. Cite
   from hit metadata — institution, author, date. Pull this in the same pass as the EDGAR
   reads, not after — it feeds both the market-structure read (Section 5) and the precedent
   table (Section 9), and serializing it behind the filing reads is what blows the clock.

Run retrieval concurrently where possible; the clock matters.

### Missing-data rule

The framework below is explicit and it governs: where market size, share, or concentration
data is not available from a reliable source, **state the limitation explicitly**. Never
estimate, never back into a number, never produce an HHI or a probability percentage
without sourced inputs. This applies equally to the directional completion read in Section
11 — HIGH/MODERATE/LOW is a qualitative synthesis grounded in named precedent and the
sourced facts above it, never a number pulled from intuition.

---

## Output — Meteora's house report format

This skill's output is a single `.docx`, named
`[TICKER] Initial Deal & Antitrust [YYYY.MM.DD].docx`, built with the `docx` skill. It
follows the same 12-section house format as Meteora's other gold-standard deal reports
(the CBZ/Grant Thornton and ZYME/TBPH reports are the reference examples — see the
worked example below). Every section below is a formatting and organization layer over
the analytical framework in the next section — it does not add analysis the framework
doesn't already call for, it just locks down where each finding goes and how it reads on
the page.

**Note on the header stub used by this skill's siblings.** `arb-day-one-top-sheet` and
`arb-dma-extraction` open with a short shared stub (Ticker/Deal/Skill/Run/Sources/Key
Findings) because they're single-purpose extraction notes. This skill produces a full
narrative report instead, so its front matter is the richer parameter table below, not
that stub — the three skills no longer share identical front matter, and that's
intentional: this one is a different kind of document.

### Front matter (before Section 1)

A centered title block — "**METEORA CAPITAL**" / "Deal Completion Risk Assessment —
[Acquirer] / [Target]" / "METEORA CAPITAL" / "Event-Driven Research | Deal Completion Risk
Assessment" / target and acquirer names / "proposed acquisition of" — then a parameter
table:

| Parameter | Detail |
| --- | --- |
| Transaction | [structure: all-cash, cash+CVR, stock, etc.] |
| Consideration | [price per share; equity value / enterprise value] |
| Announced | [date; merger agreement date if different] |
| Target structure | [entity type, jurisdiction] |
| Expected close | [stated timeframe] |
| **Overall completion assessment** | **[HIGH / MODERATE / LOW] probability of completion** (bolded) |

Below the table, one italic disclaimer line ("Prepared as internal investment research to
inform arbitrage positioning. Not investment, legal, or tax advice. All figures sourced
from primary filings; see Section 12, Sources, Citations & Limitations.") and the report
date.

### Section order — lock this exactly

1. **Executive Summary & Deal Completion Risk Matrix** — 2–3 paragraphs of narrative
   synthesis (what the deal is, what kind of transaction it is — horizontal consolidation,
   market extension, roll-up add-on — and what the completion question actually turns on),
   then a Risk Matrix table: Risk Factor | Assessment (LOW / LOW-MODERATE / MODERATE / HIGH)
   | Rationale, one row per factor drawn from the framework below (antitrust/HSR clearance,
   financing certainty, MAE, deal litigation, shareholder approval, any common-ownership or
   structural flag surfaced in the portfolio analysis, any mechanical timing risk), ending
   in an **OVERALL COMPLETION PROBABILITY** row. Source line beneath the table.
2. **Deal Structure and Terms** — a Term|Detail table covering the framework's "Deal
   Structure and Terms Analysis" elements (price, premium, structure, financing, dividend
   policy, termination fees, timeline, MAE provisions), then an **Advisors** list, then a
   **Process & governance signals** subsection (board/committee approval unanimity, go-shop
   mechanics, retention/change-in-control programs — these bear on completion, not just
   deal mechanics).
3. **Target Financial Analysis** — the framework's "Target Financial Analysis" section:
   capital structure & liquidity table, most recent quarter results if released alongside
   the deal, segment and geographic revenue tables, one labeled **"Meteora read:"** line
   connecting the financial picture to the completion question.
4. **Acquirer Profile & Financing Capacity** — open with **"Buyer classification:
   [TYPE]."** stated plainly, then the entity/platform background, the portfolio_context
   analysis (sponsor portfolio table for a PE buyer; segment/business-line table for a
   strategic; both, attributed, for a hybrid), and a financing-structure paragraph ending
   in a labeled **"Structural read (Meteora):"** paragraph.
5. **Market Definition & Concentration Analysis** — the framework's "Market Definition and
   Concentration Analysis" section: product/practice-area mapping table, market definition
   paragraph with the target's verbatim Competition-section quote, a market-size/share
   table where sourced data supports one, and an explicit "No HHI is computed" line where
   it doesn't — never a fabricated figure.
6. **Competitive Effects Analysis** — Theory of Harm | Assessment | Basis table covering
   the framework's competitive-effects subsections, then the "Portfolio Context
   Integration" paragraph, then a remedy-likelihood and divestiture-candidate paragraph.
7. **Regulatory Pathway & Timeline** — Approval/gate | Risk | Notes table (HSR, foreign
   regimes, CFIUS, shareholder vote threshold), then an indicative dated-bullet timeline
   from signing through the outside date.
8. **Litigation & Fraud Risk Analysis** — Item | Assessment | Detail table covering the
   framework's "Litigation and Fraud Risk Analysis" elements, ending in an explicit
   MAC/fraud-as-closing-impediment assessment row.
9. **Valuation & Precedent Analysis** — a Reference|Observation table (equity/enterprise
   value, premium, any deal-characterization quote), then the precedent-transactions table
   sourced from the ArbJournal/Chain Bridge Research vector passes (each row: deal, buyer
   type, day count, outcome, sourcing institution/date — never a vague "months"), then an
   **Assessment:** paragraph naming the single closest, most probative precedent and why.
10. **Strategic Stakeholder Analysis** — Stakeholder | Position table (board, shareholders,
    activists, target/acquirer management, sponsor, key commercial counterparties,
    competing bidders).
11. **Deal Completion Probability Decomposition** — this is where the framework's
    "Probability Modeling" instruction becomes visible: a Component | Likelihood | Driver
    table (antitrust/regulatory clearance, financing availability, no-MAE/target
    stability, shareholder approval, absence of deal-blocking litigation), ending in a
    **COMPOSITE COMPLETION ASSESSMENT** row (HIGH / MODERATE / LOW, matching the front-matter
    line — never a bare percentage), then a **Key monitorables** bullet list naming the
    specific open items (a common-ownership overlap left contractually unaddressed, a
    marketing-period timing mechanic, an unresolved compliance matter, an unfiled proxy).
12. **Sources, Citations & Limitations** — a Primary sources list (every EDGAR filing by
    form/date/accession, vector-DB hits by report title/institution/date, any other named
    source) and a Limitations list stating explicitly what wasn't verified this pass
    (private non-filer entities with no Competition section, unconfirmed ownership
    percentages, market-size figures not independently re-verified, documents not yet
    filed).

### Docx build recipe

- Do scratch/intermediate build work under `/tmp`, not in the outputs-mounted folder —
  files written into the outputs folder can't be deleted or renamed afterward, so dumping
  chunked build scripts there leaves permanent clutter. Copy only the finished `.docx` into
  outputs, and only once built and verified.
- If using the `docx` npm package in the sandbox, set `NODE_PATH` to wherever it's
  installed so it resolves from any cwd.
- Chunk the build into part files when the report is long (it usually is — 12 sections
  plus this many tables routinely exceeds a single comfortable script): a first part
  defining shared helpers (heading paragraphs, body paragraph, bullet, a labeled-lead-in
  helper for "Assessment:"/"Meteora read:" lines, a table builder, a section-break rule)
  plus the front matter and Section 1; subsequent parts each requiring the prior part,
  appending one or two sections, and re-exporting the running document tree; a final
  `main.js` that wraps everything in a `Document` with US Letter page size, standard
  margins, and a footer with `[TICKER] Deal Risk - Page N`.
- Verify before presenting: convert to PDF, rasterize a few pages, and read back the front
  matter/Risk Matrix, a middle table-heavy section, and the final Sources page to confirm
  tables rendered correctly and nothing got truncated by a part-file wiring mistake.
- Only then copy the finished `.docx` into the outputs folder — this step is final, so do
  it last.

---

## Reference output — study before writing

Below is a full worked example in Meteora's house format (Zymeworks Inc. / Theravance
Biopharma). It is not a template to fill in mechanically — the actual section content
always comes from this deal's own filings — but it is the exact bar for tone, table
density, section discipline, and how sourced fact is separated from labeled analytical
opinion ("Assessment:", "Meteora read:", "Structural read (Meteora):"). Match its register:
terse, EDGAR-cited, no editorializing outside a labeled analysis line, tables over prose
wherever a table is possible, and a directional (never numeric) completion read.

```
**METEORA CAPITAL** Deal Completion Risk Assessment — ZYME / TBPH

**METEORA CAPITAL**

Event-Driven Research | Deal Completion Risk Assessment

**Zymeworks Inc. (NASDAQ: ZYME)**

proposed acquisition of

**Theravance Biopharma, Inc. (NASDAQ: TBPH)**

| **Parameter** | **Detail** |
| --- | --- |
| Transaction | All-cash merger + non-tradeable Contingent Value Right (CVR) |
| Consideration | $17.00 per share in cash; equity value ~$929 million |
| CVR | 80% of net proceeds from any future ampreloxetine monetization (10-yr); add'l milestone/royalty components per CVR Agreement |
| Announced | June 29, 2026 (Merger Agreement dated June 28, 2026) |
| Target structure | Theravance Biopharma, Inc. — Cayman Islands exempted company |
| Expected close | Second half of 2026 |
| **Overall completion assessment** | **HIGH probability of completion** |

*Prepared as internal investment research to inform arbitrage positioning. Not investment, legal, or tax advice. All figures sourced from primary filings; see Sources & Limitations.*

Report date: June 29, 2026

# 1. Executive Summary & Deal Completion Risk Matrix

On June 29, 2026, Theravance Biopharma, Inc. (TBPH) announced a definitive agreement under which Zymeworks Inc. (ZYME) will acquire all outstanding ordinary shares of TBPH for $17.00 per share in cash, an equity value of approximately $929 million, plus a non-tradeable CVR tied to the failed late-stage asset ampreloxetine. The Merger Agreement is dated June 28, 2026. The transaction is the culmination of a multi-year strategic review run by an independent committee and Lazard, and is expected to close in the second half of 2026.

From a deal-completion standpoint, this is a financially-engineered, market-extension acquisition rather than a horizontal industry consolidation. ZYME is an oncology-focused antibody company (HER2 bispecific zanidatamab / Ziihera) acquiring a single-product respiratory franchise (YUPELRI / revefenacin for COPD) plus a cash-rich balance sheet, near-term royalty/milestone streams, and ~$2.5 billion of Irish tax attributes. There is no overlap in any marketed or clinical-stage product market. The antitrust pathway is therefore a formality; the gating items are the shareholder vote and confirmatory regulatory clearance, both supported by favorable deal mechanics (committed, non-recourse-anchored financing with no financing condition; reciprocal break fees; a resolved major clinical binary).

## Deal Completion Risk Matrix

| **Risk Factor** | **Assessment** | **Rationale (sourced; see body sections)** |
| --- | --- | --- |
| Antitrust / HSR clearance | **LOW RISK** | No overlapping marketed or clinical product markets (oncology vs. respiratory/neurology). HSR is the only substantive filing; early termination or uneventful 30-day expiry expected. |
| Financing certainty | **LOW RISK** | No financing condition. $929M funded by $350M non-recourse OMERS note (secured solely by YUPELRI profit share) + ~$360M target closing cash + $219M ZYME cash; ZYME held $403.8M cash at 3/31/26. |
| Material Adverse Effect | **LOW RISK** | Principal binary (ampreloxetine CYPRESS Phase 3) already failed pre-signing and is ring-fenced in the CVR; target is a stable, cash-generative single-product company with no debt. |
| Deal / merger litigation | **LOW RISK** | Routine merger-objection demands/suits possible but historically immaterial to closing; comprehensive auction strengthens fiduciary record. |
| Shareholder approval (2/3 vote) | **MODERATE** | Primary swing factor. Thin premium to recent trading (~10% to post-CYPRESS VWAP) and $17 below most recent analyst PT ($19) invite holdout/undervaluation arguments, offset by unanimous board + independent-committee recommendation, full auction, and an easier 2/3-of-votes-cast threshold. |
| Tax-attribute / restructuring (economic) | **MONITOR** | Deal economics depend partly on preserving ~$2.5B Irish tax attributes via a financing reorganization; an economic risk to ZYME, not a closing condition. |
| **OVERALL COMPLETION PROBABILITY** | **HIGH** | No antitrust, financing, or MAC impediment identified; outcome turns on a shareholder vote that is well-supported by process and consideration mix. |

*Sources: TBPH Form 8-K & Exhibit 99.1 (Jun 29, 2026); ZYME Form 8-K (Jun 29, 2026); ZYME & TBPH Q1-2026 results (May 2026). Directional assessments per Meteora protocol — no fabricated probability percentages or HHI figures.*

# 2. Deal Structure and Terms

| **Term** | **Detail** |
| --- | --- |
| Acquirer (Parent) | Zymeworks Inc. (NASDAQ: ZYME), a Delaware corporation; HQ Vancouver, BC |
| Target (Company) | Theravance Biopharma, Inc. (NASDAQ: TBPH), a Cayman Islands exempted company; operations in South San Francisco, CA and Dublin, Ireland |
| Structure | Merger of Zymeworks Merger Sub 1 (Cayman) into TBPH; TBPH survives as a wholly owned subsidiary of ZYME |
| Cash consideration | $17.00 per ordinary share; ~$929 million equity value |
| CVR (per share) | Non-tradeable; 80% of net proceeds from any future license, divestiture or other monetization of ampreloxetine over the next 10 years (20% retained by ZYME). Per the ZYME 8-K/CVR Agreement, additional components include a $50M milestone on first commercial sale in defined markets and a 10% net-sales royalty for a defined period (confirm against full CVR Agreement). |
| Ampreloxetine process | If no monetization is executed by closing, a TBPH designee will pursue monetization on ZYME's behalf for 12 months post-close |
| Premium | 22% to TBPH's 3/3/26 close (day of ampreloxetine CYPRESS topline results); 10% to VWAP since that date |
| Financing | No financing condition. $350M non-recourse note from OMERS Life Sciences (secured solely by U.S. YUPELRI profit share) + ~$360M TBPH closing net cash + $219M ZYME cash |
| Termination fees | Reciprocal $32.5 million (payable by either party under specified circumstances) |
| Shareholder approval | Two-thirds of ordinary shares present and voting at an extraordinary general meeting ('Company Requisite Vote') |
| Regulatory condition | Expiration/termination of the HSR Act waiting period ('HSR Act Clearance') |
| Other conditions | No continuing Company Material Adverse Effect; absence of legal restraints; customary conditions |
| Expected closing | Second half of 2026 |

*Sources: TBPH Form 8-K, Ex. 99.1 (Jun 29, 2026); ZYME Form 8-K (d156494d8k.htm, Jun 29, 2026); Agreement and Plan of Merger dated Jun 28, 2026 (Ex. 2.1); deal-terms confirmation via TradingView/SEC 8-K summary for CVR sub-components and $32.5M reciprocal fee.*

## Advisors

- **Theravance Biopharma:** Lazard (lead financial advisor); Evercore (financial advisor); Skadden, Arps, Slate, Meagher & Flom LLP (legal).
- **Zymeworks:** Kirkland & Ellis LLP (legal); Matheson (Irish tax); TD Cowen (advisor on the OMERS royalty note); MTS Health Partners (financial advice).
- **OMERS Life Sciences:** Sidley Austin LLP (legal); Maples and Calder (Ireland) LLP and Davies Ward Phillips & Vineberg LLP (Irish legal / tax).

## Process & governance signals (favorable to completion)

- Strategic Review Committee formed 2024, composed solely of independent directors and chaired by independent Board Chair Susannah Gray; worked with Lazard across a multi-year value-maximization process (including the 2025 monetization of TRELEGY royalties for $225M).
- The Committee unanimously recommended the transaction; the full Board unanimously approved and recommends shareholders vote in favor.
- A broad strategic-alternatives review (effectively a market canvass) reduces competing-bidder risk and strengthens the fiduciary record against merger-objection claims.

*Source: TBPH Form 8-K, Ex. 99.1 (Jun 29, 2026).*

# 3. Target Financial Analysis — Theravance Biopharma (TBPH)

TBPH is a debt-free, cash-rich, single-commercial-product company. Following the March 2026 failure of ampreloxetine's Phase 3 CYPRESS study, it wound down R&D, cut headcount ~50%, and refocused on YUPELRI economics and residual TRELEGY milestones. There are no going-concern, covenant, or solvency concerns; the balance sheet is a net asset rather than a liability in this transaction.

## Capital structure & liquidity (Q1 2026)

| **Metric (as of / for Q1 2026)** | **Value** |
| --- | --- |
| Cash, equivalents & marketable securities (3/31/26) | ~$394.7 million |
| Total debt | None (zero long-term debt) |
| Leverage (Net Debt / EBITDA, Debt/Equity) | Not applicable — no debt; net cash position |
| Covenant compliance / waivers | Not applicable — no credit facility / covenants disclosed |
| Going-concern / audit qualification | None disclosed |
| Total revenue (Q1 2026) | $17.7 million (entirely Viatris collaboration revenue) |
| Net loss (Q1 2026) | $(4.9) million (vs. $(13.6)M prior-year quarter) |
| Non-GAAP net income from operations (Q1 2026) | $0.6 million |
| R&D expense (Q1 2026) | $5.8 million (vs. $11.5M prior-year quarter) |
| Shareholders' equity (12/31/25) | $296.7 million (up from $175.5M YoY) |
| Total assets (12/31/25) | $485.6 million |

*Sources: TBPH Q1-2026 results / Form 10-Q (May 7, 2026); TBPH FY2025 Form 10-K (Mar 2026).*

## Commercial & milestone profile

- **YUPELRI (revefenacin):** Nebulized, once-daily LAMA for COPD maintenance. Viatris leads U.S. commercialization under a 65% Viatris / 35% TBPH profit-share; Viatris-reported Q1-2026 U.S. net sales of $62.4M (+7% YoY), implying ~$21.9M to TBPH's share; FY2025 U.S. net sales $266.6M (+12%). Combined U.S. profit share + ex-U.S. royalties run-rate ~$60M annualized (per ZYME).
- **TRELEGY (royalty/milestone):** TBPH sold its remaining TRELEGY royalty to GSK for $225M (June 2025) and retains up to $150M of milestones tied to 2025-2026 net sales (via Royalty Pharma). Q1-2026 TRELEGY net sales $873M (+2%); management expressed high confidence in a $100M 2026 milestone (which ZYME expects to receive ~Q1 2027).
- **Ampreloxetine:** Phase 3 CYPRESS (MSA / nOH) failed its primary endpoint (announced 3/3/26); program wound down. Economic optionality is transferred to TBPH holders via the CVR (ZYME ascribes little base-case value).
- **Irish tax attributes:** ZYME cites ~$2.5 billion of Irish tax attributes as a core strategic rationale.

## Free cash flow & distribution policy

- Restructuring targets ~60% opex reduction / ~$70M annualized savings beginning Q3 2026, supporting a lean, cash-generative model; non-GAAP operations were near breakeven in Q1.
- No dividend; no debt service. Historical cash inflows were driven by milestone and royalty monetizations ($50M TRELEGY milestone Feb 2025; $225M TRELEGY royalty sale June 2025; $25M YUPELRI milestone).

*Sources: TBPH FY2025 10-K; TBPH Q1-2026 results (May 7, 2026); ZYME Form 8-K / press release (Jun 29, 2026).*

# 4. Acquirer Profile & Financing Capacity — Zymeworks (ZYME)

Buyer classification: STRATEGIC. Zymeworks is a biotechnology company centered on its partnered HER2 bispecific antibody zanidatamab (Ziihera), with an oncology ADC and immunology/inflammation (I&I) pipeline. It is not a private-equity sponsor; the standard PE-portfolio-overlap analysis is therefore reframed below as a product/pipeline overlap analysis (Sections 5–6). The relevant completion question for the acquirer is financing capacity, which is strong.

## Acquirer financial position

| **Metric** | **Value** |
| --- | --- |
| Cash, equivalents & marketable securities (3/31/26) | $403.8 million ($244.3M cash + $159.6M securities) |
| Non-dilutive financing (Mar 2026) | $250M non-recourse royalty-backed note from Royalty Pharma (secured by 30% of Ziihera royalties) |
| FY2025 total revenue | $106.0 million (+39% YoY) |
| FY2025 net loss | $(81.1) million (improved from $(122.7)M in 2024) |
| Stated cash runway | Beyond 2028 (incl. ~$440M anticipated Ziihera regulatory milestones) |
| Capital return | 2026 buyback up to $125M (~$95.8M used by early May); 2025 program repurchased 4.2M shares for $102.3M |
| Lead asset catalyst | Ziihera (1L HER2+ GEA) U.S. PDUFA date August 25, 2026 |

*Sources: ZYME Q1-2026 results / Form 8-K (May 7, 2026); ZYME FY2025 results (Mar 2, 2026); ZYME–Royalty Pharma note announcement (Mar 2, 2026).*

## Financing structure of the $929M purchase price (no financing condition)

| **Source** | **Amount** | **Nature / risk note** |
| --- | --- | --- |
| Non-recourse note — OMERS Life Sciences | $350M | Secured solely by U.S. YUPELRI profit share; non-recourse to ZYME (ring-fenced acquired cash flow) |
| Theravance Biopharma closing net cash | ~$360M | Target's own balance-sheet cash funds the largest share of consideration |
| Zymeworks cash at close | $219M | Modest vs. ZYME's $403.8M cash at 3/31/26 |
| **Total consideration** | **~$929M** | Plus expected $100M TRELEGY milestone (~Q1 2027) offsetting outlay; deal stated to be accretive to earnings and cash flow |

**Structural read (Meteora).** The financing is engineered to minimize ZYME's net capital at risk: the target's own cash and non-recourse leverage against the acquired YUPELRI stream together fund ~$710M of the ~$929M price, leaving ZYME a modest net cash contribution against near-term milestone inflows. Because there is no financing condition and the largest funding source is the target's own balance sheet, financing is not a credible impediment to closing.

*Sources: ZYME Form 8-K / press release (Jun 29, 2026); ZYME Q1-2026 8-K (May 7, 2026).*

# 5. Market Definition & Concentration Analysis

**Threshold framing (decisive).** Consistent with Meteora protocol, the vertical/market-extension vs. horizontal question is resolved before any concentration screen. This transaction joins two non-overlapping therapeutic franchises; there is no relevant antitrust product market in which both parties participate, so market-share and HHI computation is inapplicable. No HHI figures are estimated.

## Product/therapeutic-area mapping

| **Dimension** | **Zymeworks (Acquirer)** | **Theravance Biopharma (Target)** |
| --- | --- | --- |
| Primary therapeutic area | Oncology (HER2-positive cancers) | Respiratory (COPD) |
| Lead marketed/registrational asset | Ziihera / zanidatamab (HER2 bispecific antibody; 1L HER2+ GEA, U.S. PDUFA 8/25/26) | YUPELRI / revefenacin (nebulized LAMA; COPD maintenance) — co-promoted with Viatris |
| Modality | Biologics — bispecific antibodies, ADCs | Small-molecule inhalation therapeutic |
| Pipeline focus | Oncology ADCs (ZW191, ZW220, ZW251, pan-RAS ADCs); preclinical I&I / autoimmune (AIID) | Autonomic neurology (ampreloxetine — failed Ph3, now CVR); preclinical I&I |
| Customers / channel | Oncology specialists, partnered commercialization (Jazz, BeOne) | Pulmonology, COPD; Viatris-led U.S. commercialization |
| **Horizontal overlap in any marketed/clinical market?** | **None** | **None** |

*Sources: ZYME Q1-2026 results & corporate update (Jan/May 2026); ZYME–Royalty Pharma note (Mar 2026); TBPH FY2025 10-K & Q1-2026 results; deal press release (Jun 29, 2026).*

## Relevant markets & screening

- Relevant product markets do not intersect: HER2-targeted oncology biologics vs. nebulized LAMA bronchodilators for COPD are distinct on indication, mechanism, modality, prescriber, and channel. There is no demand- or supply-side substitution between them.
- The only nominal touchpoint is that each party lists a preclinical I&I / autoimmune effort. These are research-stage, with no disclosed shared target, no marketed product, and no near-term competition — below any cognizable horizontal-overlap or late-stage pipeline-overlap threshold.
- Market size, market share, and HHI: not computed — there is no shared market to measure. Per protocol, no figures are fabricated where overlap is absent.

# 6. Competitive Effects Analysis

| **Theory of harm** | **Assessment** | **Basis** |
| --- | --- | --- |
| Horizontal overlap | **None** | No common marketed or clinical product market (oncology biologics vs. respiratory small molecule). |
| Vertical / input foreclosure | **None** | No upstream/downstream supply relationship between the parties' products; no foreclosure of rivals' inputs or distribution. |
| Potential competition | **None** | Neither party is a likely or actual entrant into the other's market; ZYME has no respiratory/COPD program, TBPH no oncology program. |
| Conglomerate / bundling | **Negligible** | No plausible tying/bundling across COPD and HER2 oncology; distinct prescribers, payers, and channels. |
| Innovation / dynamic | **Negligible** | No overlapping late-stage R&D programs; preclinical I&I touchpoint is non-specific and research-stage. |
| Buyer / monopsony power | **None** | No common input markets or supplier base where combined purchasing would create monopsony effects. |

**Portfolio-context integration.** Reframing the PE-portfolio test for a strategic acquirer: the combination is platform-diversifying (adding a commercial respiratory cash-flow stream and tax attributes to an oncology platform) rather than an add-on to a concentrated franchise. There is no customer overlap to cross-sell, no combined data asset of competitive concern, and no R&D consolidation that removes a competing development path. Competitive-effects risk to deal completion is de minimis.

*Analytical assessment based on sourced product/pipeline profiles in Sections 4–5; no agency overlap concern is implied by the parties' disclosures.*

# 7. Regulatory Pathway & Timeline

| **Approval / gate** | **Risk** | **Notes** |
| --- | --- | --- |
| U.S. HSR Act clearance | **LOW** | Sole substantive antitrust filing. Given zero product overlap, expect early termination (if granted) or expiry of the initial 30-day waiting period without a second request. |
| Other foreign merger control | **LOW** | No horizontal overlap to trigger substantive review in any jurisdiction; filings, if any, should be clearance formalities. |
| CFIUS | **N/A / negligible** | Target is a COPD drug co-promotion (non-sensitive/non-TID); acquirer is Delaware-incorporated and Nasdaq-listed. No evident CFIUS nexus. |
| TBPH shareholder vote (2/3) | **MODERATE** | Extraordinary general meeting; see Sections 1 and 10. Definitive proxy (Schedule 14A) to be filed; vote is the binding-path long pole. |

## Indicative timeline

- Jun 28–29, 2026: Merger Agreement signed; transaction announced; preliminary 8-K/DEFA14A filed.
- Q3 2026: HSR filing and waiting period; preliminary then definitive proxy statement; setting of EGM record date and meeting date.
- H2 2026: TBPH extraordinary general meeting and shareholder vote; satisfaction of remaining conditions; expected closing.

*Sources: ZYME Form 8-K (closing conditions, Jun 29, 2026); TBPH Ex. 99.1 (Jun 29, 2026). Timeline is indicative based on customary U.S. single-target cash-merger sequencing.*

# 8. Litigation & Fraud Risk Analysis

| **Item** | **Assessment** | **Detail** |
| --- | --- | --- |
| Target material litigation | **LOW** | All Hatch-Waxman (ANDA) litigation relating to YUPELRI resolved following a March 2026 settlement with Mankind Pharma. No other material proceedings surfaced in filings reviewed. |
| Acquirer material litigation | **LOW** | No active material securities class action or government enforcement action surfaced in the searches and filings reviewed. |
| Restatements / internal investigations | **None identified** | No financial restatements, audit qualifications, or internal-investigation disclosures identified for either party. |
| Short-seller / fraud allegations | **None identified** | No publicly available short-seller report or public fraud allegation against either party was identified as of the report date. |
| Deal-specific litigation | **LOW** | Routine merger-objection demand letters / disclosure suits are typical for public-company mergers but historically immaterial to closing; the multi-year independent auction strengthens the fiduciary record. |
| MAC / fraud as closing impediment | **LOW** | No litigation or fraud exposure identified that would plausibly trigger the Company MAE condition. |

**Note on estimated exposure.** No quantified pending-litigation exposure was disclosed in the materials reviewed that is material to either party or to deal completion. This section reflects sources available on the announcement date; the definitive proxy and each party's next periodic report should be monitored for any newly disclosed proceedings.

*Sources: TBPH Q1-2026 results (Hatch-Waxman/Mankind settlement, May 7, 2026); TBPH FY2025 10-K legal proceedings; ZYME periodic filings; public search for short-seller/fraud allegations (no results as of Jun 29, 2026).*

# 9. Valuation & Precedent Analysis

This is an asset/cash-flow-and-tax-attribute acquisition rather than an EBITDA-multiple buyout, so conventional EV/EBITDA framing is of limited use. The headline cash value is dominated by the target's balance-sheet cash and discrete royalty/milestone/tax assets.

| **Valuation reference** | **Observation** |
| --- | --- |
| Equity value | ~$929 million ($17.00/share, cash) |
| Target closing net cash (approx.) | ~$360 million — a large share of equity value is the target's own cash |
| Implied value for operating/asset base | Residual after net cash ≈ ~$570M for YUPELRI economics (~$60M/yr run-rate cash flow), TRELEGY milestones (up to ~$100M near-term), ~$2.5B Irish tax attributes, and 20% retained ampreloxetine CVR economics |
| Premium | 22% to 3/3/26 close (post-CYPRESS); 10% to subsequent VWAP — modest vs. typical take-private premia, reflecting a cash-heavy target trading near intrinsic cash value |
| Most recent analyst price target | $19.00 (Buy) per the latest analyst rating cited post-announcement — i.e., $17.00 sits below the most recent published target |

**Completion-relevant read.** The thin premium to recent trading and a deal price below the most recent analyst target are the elements most likely to be invoked by a holdout or activist arguing for a bump. Counterweighing: the price was struck after a comprehensive multi-year auction with no superior proposal emerging, the consideration is all cash plus retained CVR upside on the failed asset, and a large portion of value is simply the target's own cash being returned at a premium.

*Sources: deal press releases (Jun 29, 2026); TBPH/ZYME financials; analyst PT per post-announcement summary (TipRanks). Precedent-multiple comps are not asserted given the asset/cash-flow nature of the transaction; no fabricated multiples included.*

# 10. Strategic Stakeholder Analysis

| **Stakeholder** | **Position / consideration** |
| --- | --- |
| TBPH Board & Strategic Review Committee | Independent committee (Chair: Susannah Gray) unanimously recommended; full Board unanimously approved and recommends a 'for' vote. Multi-year process with Lazard supports the record. |
| TBPH shareholders | Must approve by 2/3 of shares present and voting. All-cash certainty + CVR upside; principal friction is the thin premium / sub-PT price (Section 9). No disclosed controlling bloc opposed. |
| Activist / significant holders | No public objection identified at announcement. Undervaluation-of-net-cash arguments are the plausible vector if an activist emerges; monitor 13D/A activity and proxy advisory recommendations. |
| Viatris (YUPELRI partner) | Key commercial collaborator; U.S. profit-share counterparty. Continuity of the Viatris collaboration underpins the acquired cash-flow thesis; partner response is a monitorable but not a closing condition. |
| GSK / Royalty Pharma (TRELEGY) | Counterparties to TRELEGY milestone economics; the ~$100M 2026 milestone is part of deal financing math (expected ~Q1 2027). |
| OMERS Life Sciences | Provides the $350M non-recourse acquisition note; aligned financing partner, not a closing-risk vector. |
| Acquirer governance | ZYME led by Kenneth Galbraith (Chair, President & CEO; acting CFO). No ZYME shareholder vote required for the merger; ZYME approval already obtained at board level. |
| Competing bidders | None emerged from the comprehensive strategic review; an interloper at a meaningful premium appears unlikely given the cash-heavy valuation and prior canvass. |

*Sources: TBPH Ex. 99.1 (Jun 29, 2026); ZYME Form 8-K; ZYME Q4-2025/Q1-2026 disclosures.*

# 11. Deal Completion Probability Decomposition

Per Meteora protocol, the assessment is directional (HIGH / MODERATE / LOW) with a decomposed rationale; no point probability is asserted.

| **Component** | **Likelihood** | **Driver** |
| --- | --- | --- |
| Antitrust / HSR clearance | **HIGH** | No product-market overlap; confirmatory filing only. |
| Financing availability | **HIGH** | No financing condition; committed, target-cash-anchored, non-recourse-leveraged structure. |
| No MAC / target stability | **HIGH** | Major clinical binary already resolved and ring-fenced; debt-free, cash-generative target. |
| Shareholder approval (2/3 votes cast) | **MODERATE–HIGH** | Unanimous board/committee support and full auction vs. thin premium / sub-PT price. The binding swing factor. |
| Absence of deal-blocking litigation | **HIGH** | Only routine merger-objection activity expected. |
| **COMPOSITE COMPLETION ASSESSMENT** | **HIGH** | Closing turns almost entirely on an affirmative shareholder vote that is well-supported by process and consideration; no structural impediment identified. |

## Key monitorables

- Definitive proxy (Schedule 14A): background-of-the-merger, fairness opinion, projections, and any 'go-shop'/'no-shop' nuance; EGM date.
- Proxy advisory (ISS/Glass Lewis) recommendations and any activist 13D/A or public undervaluation campaign.
- HSR status (early termination grant or waiting-period expiry).
- YUPELRI/Viatris collaboration continuity and TRELEGY milestone confirmation; preservation of Irish tax attributes through the financing reorganization (economic, not closing).

# 12. Sources, Citations & Limitations

## Primary sources

- Theravance Biopharma, Inc. — Form 8-K and Exhibit 99.1 (press release), filed June 29, 2026 (event date June 28, 2026); DEFA14A; Agreement and Plan of Merger dated June 28, 2026 (Exhibit 2.1) and Form of CVR Agreement (Exhibit A).
- Zymeworks Inc. — Form 8-K (d156494d8k.htm) and Exhibit 99.1, June 29, 2026 (closing conditions: HSR Act Clearance; two-thirds Company Requisite Vote; no continuing Company MAE; no legal restraint).
- Theravance Biopharma — Q1-2026 results / Form 10-Q (May 7, 2026) and FY2025 Form 10-K (March 2026): cash $394.7M, no debt; YUPELRI economics; TRELEGY milestones; ampreloxetine CYPRESS failure; Mankind Hatch-Waxman settlement.
- Zymeworks — Q1-2026 results / Form 8-K (May 7, 2026): cash $403.8M; FY2025 results (March 2, 2026): revenue $106.0M, net loss $81.1M; ZYME–Royalty Pharma $250M note (March 2, 2026); Ziihera PDUFA date August 25, 2026.
- Deal-terms confirmation (reciprocal $32.5M termination fee; CVR sub-components — $50M first-commercial-sale milestone and 10% net-sales royalty) via SEC 8-K summary; to be confirmed verbatim against the full Merger Agreement and CVR Agreement.

## Limitations

- This assessment reflects information available on the announcement date (June 29, 2026). The definitive proxy statement, fairness opinion, and full Merger/CVR Agreement text were not yet available in full for verbatim extraction; certain terms (precise MAC carve-outs, no-shop/fiduciary-out mechanics, regulatory-efforts covenant, CVR sub-components) should be confirmed against those documents when filed.
- Per Meteora protocol: no market shares, HHI figures, or point probability percentages are estimated where source data is absent. Because the parties operate in non-overlapping product markets, concentration analysis is inapplicable and intentionally omitted rather than fabricated.
- Directional risk ratings are analytical opinions of Meteora Capital, distinct from the sourced facts presented; they are not a guarantee of any outcome.
- Litigation/fraud findings reflect filings reviewed and public search as of the report date; absence of identified short-seller or class-action activity is not a representation that none exists or could arise.

*Meteora Capital — Event-Driven Research. Internal investment research; not investment, legal, or tax advice. Not for distribution.*
```

---

## Analytical framework — reproduce exactly

Everything below this line is the trader's Initial Deal & Antitrust prompt. It is the
authoritative spec for this skill. **Do not paraphrase, compress, reorder, or drop items
from it.** Every section, deliverable, checklist step, and verification standard applies.
The report structure above is a formatting layer over this framework — every table and
section it calls for maps onto one of the elements below (the "Probability Modeling with
Portfolio Considerations" section, for instance, is what Section 11's Deal Completion
Probability Decomposition makes visible on the page).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<antitrust_risk_assessment_guide>
  <general_instructions>
    <perspective>Conduct analysis from the perspective of a prospective deal risk analyst evaluating transaction completion probability. Do not provide strategic recommendations for parties involved in the transaction, and do not focus on where the target stock is trading relative to deal consideration.</perspective>
    <critical_requirements>
      <requirement>All facts and figures must be cited with specific sources</requirement>
      <requirement>Never estimate, calculate, or hallucinate market shares, HHI calculations, or probability percentages without explicit source data</requirement>
      <requirement>If market size or concentration data is unavailable, explicitly state this limitation rather than making estimates</requirement>
      <requirement>Distinguish clearly between sourced facts and analytical opinions</requirement>
      <requirement>Competitor disclosures and geographic revenue breakdowns are required outputs, sourced directly from EDGAR filings (10-K, 10-Q, 8-K, merger filings)</requirement>
    </critical_requirements>
  </general_instructions>
  <portfolio_context_analysis>
    <section title="Critical Portfolio Company Due Diligence">
      <requirements>
        <requirement>Comprehensive listing of acquirer's portfolio (majority and minority stakes) to identify horizontal and adjacent overlaps</requirement>
        <requirement>Historical portfolio investigation including past exits to assess consolidation patterns</requirement>
        <requirement>Analysis of direct, adjacent, complementary, and potential future competitors</requirement>
        <requirement>Verification using acquirer website, EDGAR, specialized PE databases, and reputable news sources</requirement>
      </requirements>
    </section>
    <section title="PE-Specific Competitive Effects Framework">
      <deliverables>
        <deliverable>Portfolio Company Overlap Table aligning portfolio companies against target product/service lines</deliverable>
        <deliverable>Revenue segmentation comparison by product, geography, and customer type</deliverable>
        <deliverable>Geographic revenue breakdowns for target and overlapping portfolio companies from EDGAR</deliverable>
        <deliverable>Analysis of high-concentration regions and geographic expansion trends</deliverable>
        <deliverable>Vertical integration assessment for upstream/downstream relationships</deliverable>
        <deliverable>Review of whether acquisition represents part of a roll-up strategy</deliverable>
      </deliverables>
    </section>
    <section title="Enhanced Competitive Effects Evaluation">
      <considerations>
        <consideration>Platform vs. add-on characterization</consideration>
        <consideration>Customer overlap and potential cross-selling or bundling</consideration>
        <consideration>Data advantage risks from combined portfolio</consideration>
        <consideration>Innovation impact from combined R&D capabilities</consideration>
      </considerations>
    </section>
    <section title="Regulatory History Examination">
      <requirements>
        <requirement>Review prior antitrust reviews of the PE sponsor in related sectors</requirement>
        <requirement>Summarize remedies/divestitures previously required</requirement>
      </requirements>
    </section>
    <section title="Geographic Revenue Analysis Requirements">
      <mandatory_items>
        <item>Market-by-market assessment for each overlapping product/service line</item>
        <item>Target geographic revenue breakdown with EDGAR citation</item>
        <item>Portfolio companies' geographic revenue breakdown using same categories</item>
        <item>Combined entity's position by geography (text and table only)</item>
        <item>Geographic concentration flags where overlaps exceed screening thresholds</item>
        <item>Year-over-year geographic expansion trends</item>
      </mandatory_items>
    </section>
    <section title="Portfolio Company Competitor Documentation">
      <requirements>
        <requirement>Extract and cite competitors listed in each relevant portfolio company's latest 10-K/10-Q</requirement>
        <requirement>Cross-reference competitor lists across portfolio companies and target</requirement>
        <requirement>Identify common competitors</requirement>
        <requirement>Analyze likely responses from non-portfolio competitors</requirement>
      </requirements>
    </section>
    <section title="Probability Modeling with Portfolio Considerations">
      <constraints>
        <constraint>Base assessments solely on historical precedent of similar PE transactions with overlaps</constraint>
        <constraint>Include remedy likelihood qualitatively where overlaps exist</constraint>
        <constraint>Identify potential divestiture candidates in text or table form</constraint>
      </constraints>
    </section>
    <section title="Enhanced Documentation Requirements">
      <requirements>
        <requirement>Include relevant sections from portfolio companies' latest EDGAR filings</requirement>
        <requirement>Extract geographic segment tables verbatim with citations</requirement>
        <requirement>Provide verbatim competitor listings from EDGAR Competition sections</requirement>
        <requirement>Summarize PE investment thesis and how target fits within portfolio</requirement>
      </requirements>
    </section>
  </portfolio_context_analysis>
  <analysis_framework>
    <section title="Deal Structure and Terms Analysis">
      <required_elements>
        <element>Purchase price, premium calculation, and analyst comparison</element>
        <element>Deal structure and consideration details</element>
        <element>Financing structure including debt/equity amounts</element>
        <element>Sponsor background and ownership structure</element>
        <element>Dividend/distribution policy during pendency</element>
        <element>Termination fees and downside protections</element>
        <element>Expected closing timeline and milestones</element>
        <element>Material adverse change provisions</element>
      </required_elements>
    </section>
    <section title="Target Financial Analysis">
      <required_elements>
        <element>Capital structure overview including total debt, equity, and key debt instruments with EDGAR citations</element>
        <element>Leverage metrics (Net Debt/EBITDA, Debt/Equity, interest coverage) sourced from EDGAR filings</element>
        <element>Recent financing activity including equity offerings, debt issuances, and credit facility amendments</element>
        <element>Free cash flow profile including operating cash flow, capital expenditures, and unlevered free cash flow trends</element>
        <element>Liquidity position including cash on hand, revolver availability, and near-term debt maturities</element>
        <element>Covenant compliance disclosures and any waiver or amendment history from EDGAR filings</element>
        <element>Potential solvency concerns including going concern disclosures, audit qualifications, or financial distress indicators</element>
        <element>Dividend and share repurchase history and sustainability relative to free cash flow generation</element>
      </required_elements>
    </section>
    <section title="Valuation and Precedent Analysis">
      <required_elements>
        <element>Key valuation multiples (EV/Revenue, EV/EBITDA, P/E)</element>
        <element>Comparison to precedent transactions with multiples cited</element>
        <element>Peer group trading multiples</element>
        <element>Assessment relative to recent M&A activity</element>
        <element>Premium analysis versus historical averages</element>
        <element>Synergy expectations and disclosed targets</element>
      </required_elements>
    </section>
    <section title="Strategic Stakeholder Analysis">
      <required_elements>
        <element>Existing strategic investors and rights</element>
        <element>Board composition and approval processes</element>
        <element>Shareholder approval requirements</element>
        <element>Management retention and change-in-control terms</element>
        <element>Key customer/supplier/partner relationships</element>
        <element>Activist or significant shareholders with objections</element>
        <element>Potential competing bidders</element>
      </required_elements>
    </section>
    <section title="Litigation and Fraud Risk Analysis">
      <required_elements>
        <element>Overview of active material litigation involving the target and bidder sourced from EDGAR disclosures (10-K, 10-Q, 8-K legal proceedings sections)</element>
        <element>Historical litigation profile including past settlements, judgments, and financial impact with EDGAR citations</element>
        <element>Regulatory investigations or government enforcement actions disclosed in filings</element>
        <element>Any disclosed fraud allegations, financial restatements, or internal investigation disclosures</element>
        <element>Review of publicly available short-seller reports or public fraud allegations targeting either the target or the bidder</element>
        <element>Estimated financial exposure from pending litigation as disclosed in EDGAR filings</element>
        <element>Deal-specific litigation risks including merger objection lawsuits, fiduciary duty claims, and appraisal rights actions</element>
        <element>Assessment of material litigation or fraud allegations as a potential deal-closing impediment or MAC trigger</element>
      </required_elements>
    </section>
    <section title="Market Definition and Concentration Analysis">
      <steps>
        <step>Define relevant product and geographic markets</step>
        <step>Provide geographic and segment revenue breakdowns from EDGAR</step>
        <step>Apply hypothetical monopolist test</step>
        <step>Only quantify market shares and HHI with reliable data</step>
        <step>If data unavailable, state limitation explicitly</step>
        <step>Identify and analyze significant competitors</step>
        <step>Extract competitors from EDGAR Competition sections</step>
        <step>Assess adjacent markets and substitutes</step>
        <step>Evaluate barriers to entry</step>
      </steps>
    </section>
    <section title="Competitive Effects Analysis">
      <subsections>
        <subsection>Horizontal Overlap Assessment</subsection>
        <subsection>Vertical Relationship Assessment</subsection>
        <subsection>Potential Competition Assessment</subsection>
        <subsection>Conglomerate Effects</subsection>
        <subsection>Innovation and Dynamic Competition Concerns</subsection>
        <subsection>Buyer/Supplier Power and Monopsony Effects</subsection>
        <subsection>Portfolio Context Integration (platform vs. add-on, cross-selling, data advantages, innovation impacts)</subsection>
      </subsections>
    </section>
    <section title="Evidence Collection and Documentation">
      <required_sources>
        <source>10-K and 10-Q MD&A (EDGAR)</source>
        <source>Segment reporting by product, geography, and customer type (EDGAR)</source>
        <source>Competition sections of 10-Ks and 10-Qs (EDGAR)</source>
        <source>Merger agreements, proxy statements, S-4/F-4, and 8-Ks (EDGAR)</source>
        <source>Industry analyst reports and trade publications</source>
        <source>FTC/DOJ precedent cases and enforcement actions</source>
        <source>Trade association data and industry studies</source>
        <source>Customer and supplier contract disclosures</source>
        <source>Patent filings and R&D disclosures</source>
        <source>PE sponsor and portfolio company disclosures verified against EDGAR</source>
      </required_sources>
    </section>
  </analysis_framework>
  <implementation_checklist>
    <required_portfolio_steps>
      <step>List all PE acquirer portfolio companies</step>
      <step>Flag overlaps with target</step>
      <step>Extract geographic revenue breakdowns from EDGAR</step>
      <step>Compare product/service offerings in table form</step>
      <step>Document all competitors from filings with citations</step>
      <step>Analyze historical acquisition patterns</step>
      <step>Evaluate roll-up or platform strategy</step>
      <step>Assess cross-selling and data combination risks</step>
      <step>Review previous antitrust reviews</step>
    </required_portfolio_steps>
    <geographic_revenue_documentation>
      <step>Standardize geographic categories across companies</step>
      <step>Extract revenue percentages by region from filings</step>
      <step>Compare combined geographic presence in tables</step>
      <step>Document expansion trends</step>
      <step>Analyze regional regulatory considerations</step>
    </geographic_revenue_documentation>
    <financial_analysis_documentation>
      <step>Extract capital structure and leverage metrics from most recent EDGAR filings</step>
      <step>Document near-term debt maturities and liquidity position</step>
      <step>Identify any going concern disclosures, covenant waivers, or distress indicators</step>
      <step>Summarize recent financing activity and free cash flow trends</step>
    </financial_analysis_documentation>
    <litigation_and_fraud_documentation>
      <step>Extract legal proceedings disclosures from target and bidder EDGAR filings</step>
      <step>Search for publicly available short-seller reports or fraud allegations on either party</step>
      <step>Document estimated financial exposure from pending litigation with citations</step>
      <step>Assess deal-specific litigation risks including merger objection suits and appraisal actions</step>
    </litigation_and_fraud_documentation>
    <documentation_format_requirements>
      <requirement>Present all findings in text and tables only</requirement>
      <requirement>Include a dedicated "Portfolio Company Analysis" section</requirement>
      <requirement>Provide comparative tables for geographic revenue</requirement>
      <requirement>Document competitor lists with exact citations</requirement>
    </documentation_format_requirements>
  </implementation_checklist>
  <fact_verification_requirements>
    <market_data_standards>
      <standard type="market_size_figures">Must cite specific industry reports, government data, or trade association studies</standard>
      <standard type="market_share_calculations">Only if both revenue and total market size are from reliable sources</standard>
      <standard type="hhi_calculations">Only if sufficient market participant data is available</standard>
      <standard type="probability_estimates">Only if based on historical precedent data from similar transactions</standard>
      <standard type="valuation_multiples">Cite precedent transactions, filings, or analyst reports</standard>
      <standard type="competitor_lists">Required verbatim from EDGAR filings</standard>
      <standard type="geographic_revenue">Required verbatim from EDGAR segment tables</standard>
      <standard type="portfolio_mapping">Portfolio verified via EDGAR and sponsor disclosures; minority stakes noted</standard>
      <standard type="leverage_and_financial_metrics">Sourced from most recent EDGAR filings (10-K, 10-Q); do not estimate</standard>
      <standard type="litigation_exposure">Sourced from EDGAR legal proceedings disclosures; publicly available short reports cited by source and date</standard>
    </market_data_standards>
  </fact_verification_requirements>
</antitrust_risk_assessment_guide>
```

---

## Operating notes

**Buyer type drives the portfolio sections.** The `portfolio_context_analysis` block is
written for a PE sponsor. For a **strategic** acquirer, apply the identical logic to the
acquirer's own reported segments, product lines, geographic revenue, and 10-K Competition
disclosures — the overlap question is the same, the source is the acquirer's own filings
rather than a portfolio roster. For a **consortium**, run it for each member.

**Sourced facts vs. analytical opinion must be visibly separated**, per the framework's
critical requirements. Where the framework calls for assessment (competitive effects,
remedy likelihood, litigation as a MAC trigger, the Section 11 decomposition), label it
with a lead-in like "Assessment:", "Meteora read:", or "Structural read (Meteora):" and
ground it in the cited facts above it. Do not let opinion migrate into the factual
sections.

**Verdict language stays qualitative.** The framework's own "Probability Modeling with
Portfolio Considerations" section already calls for a completion-probability perspective
("evaluating transaction completion probability") grounded in historical precedent — the
Section 1 Risk Matrix and Section 11 Decomposition simply give that instruction a locked
place to live on the page. HIGH / MODERATE / LOW, always tied to named precedent and
sourced facts; never a percentage, never an unsourced number.

**Do not discuss the spread.** The framework is explicit: do not focus on where the target
trades relative to deal consideration. No price, no spread, no implied probability from
the tape.

**Tables and text only.** No charts, no graphics.

