# Deal Risk Flash — Report Template

This is deal-risk-assessment's report at lower resolution, not a different document. Section
numbers and names match `deal-risk-assessment/references/report-template.md` exactly, so a Flash
Read and a later full assessment on the same deal line up section for section. Sections Flash
cannot honestly populate stay present as one-line stubs — the reader needs to see the shape of
what has not been looked at.

Keep it to roughly two pages. If it is longer, the analysis drifted into the full assessment.

## Document format (when producing the .docx)

- **Verdict callout first** (shaded, left accent bar): the call — Lean in / Watch / Pass on first
  look — in one sentence, plus the single fact most likely to change it. A reader who stops here
  has the answer.
- **Each populated section opens with a bold one-line takeaway** before any detail.
- **Detail goes in tables, and every table carries its source** — in the caption or a per-row
  source column. A number that lives only in a table with no visible source is unauditable, and
  the reader shouldn't have to hunt the body for it. This is the same discipline as the full
  report; it is not relaxed because the read is fast.
- **Confidence labels are part of the content, not a disclaimer** — "confirmed" / "likely,
  unconfirmed" on the buyer classification, "evidenced, unverified" / "plausible, unverified" /
  "no signal, not screened" on the overlap screen. Never the word "clean".
- **Deferred sections render as a single italic line each**, not as empty headers.
- **Sources block in small type** at the end, grouped by channel (EDGAR / company deal materials /
  vector database), with accession numbers and, for vector hits, the metadata citation.

---

# Deal Risk Flash: [Acquirer] / [Target] ([TICKER])

*As of [date, time if known]. Preliminary triage read composed without reference to market
pricing. Sections 4, 5 and 6 not attempted; Section 8 not run. Run deal-risk-assessment for the
complete report.*

> **CALL: [Lean in / Watch / Pass on first look]** — one sentence on why, naming the single fact
> most likely to change it.

## 1. Deal Summary

**Takeaway:** one bold line.

**Table 1 — Key Deal Terms** (term | detail | source)

Rows, each sourced to the 8-K, the press release, or the anchored EX-2.1 lookup:

- Consideration and structure (merger sub mechanics, what happens to the listing)
- Deal value; disclosed premium **with its stated basis** (close vs. VWAP) — and the gap between
  the two where both are known
- Financing: committed amounts, sources, whether financing is a closing condition
- Termination fees both directions, including any reduced go-shop / Excluded-Party fee, and any
  guarantee standing behind the parent fee
- Efforts / regulatory covenant — the operative phrase quoted, and whether divestiture is required
  and how it is capped *(from the EX-2.1 anchored read; "not yet filed" if the exhibit is absent)*
- Outside date; marketing-period length
- Required approvals, split into **conditions to closing** vs. **covenants to file**
- Go-shop: headline expiry and the real Excluded-Party deadline
- Stated expected close timing
- Pre-announced divestitures or planned post-close separations
- Advisors, both sides, where the release names them

## 2. Buyer Classification and Competitive Footprint

**Takeaway:** one bold line naming the buyer type and the confidence flag.

Classification (financial sponsor / strategic / hybrid-consortium) with the entity-level evidence —
acquisition vehicle, ultimate parent, guarantor, commitment-letter parties — and **confirmed** or
**likely, unconfirmed**. For hybrids, state which entity carries the competitive footprint and
which carries the capital. One line on the buyer's own business lines; where the buyer is private
and does not file, say so explicitly, because that asymmetry is the main limit on Section 3.

## 3. Overlap Screen (preliminary)

**Takeaway:** one bold line carrying the overall grade.

**Table 3 — Preliminary Overlap Screen** (target business line | revenue share | buyer presence in
that line | overlap type | evidence + source)

Overlap type is horizontal / vertical / adjacent / no signal. Evidence comes from the target's
10-K Competition section (quoted verbatim, filing cited), the deck's own market-positioning
language, or a named portfolio-company match.

Below the table, in prose:

- The target's Competition section **quoted verbatim** with the filing cited — including when it
  names no specific competitors, which is itself a finding about market fragmentation.
- Segment and geographic revenue mix, sourced.
- The overall grade — **overlap evidenced, unverified** / **overlap plausible, unverified** /
  **no overlap signal found, but not screened**. Never "clean".
- One line on what would settle it, so the full assessment starts from a question rather than a
  blank page.

## 4. Market Definition and Competitive Effects

*Deferred to deal-risk-assessment — no market definition, share, or HHI work attempted at flash
speed, and estimating any of it unsourced would be worse than the gap.*

## 5. Financial Health

*Deferred to deal-risk-assessment — target capital structure, leverage, and liquidity not
reviewed.*

## 6. Litigation and Fraud Screen

*Deferred to deal-risk-assessment — neither party screened for proceedings, investigations, or
public allegations.*

## 7. Completion Assessment (preliminary, blind)

**Takeaway:** one bold line.

**Table 8 — Precedent Transactions** (deal | year | buyer type | review track | announce→close
days | outcome | source)

One deal per row; a specific day count and actual outcome in every row; cite each from vector hit
metadata (institution, title, date). Precedents matched on buyer type and structure where the
corpus allows — and where it doesn't, say so above the table and label the rows **structure-only
analogs, not sector comparables** rather than implying a match that isn't there. If the index
returned nothing on-point, write that plainly and leave the table out; note whether the emptiness
looks like a genuine absence or a coverage gap in the index.

Then, in prose:

- The completion view in two or three sentences, grounded in the covenant, the fee structure, the
  approvals list, and the precedents — labeled **Assessment:** so it is never mistaken for
  sourced fact.
- **What Flash did not look at**, as a short list: buyer footprint verification and full overlap
  screen, market definition and shares, target financials, litigation and fraud, the full
  sell-side sweep (Outlook + uploaded research + complete vector passes), and market pricing
  (blind by design).
- **What would move the call**, in one line — the specific unknown whose resolution flips it.

## 8. Tape Check

*Not run. Flash is blind by design; the tape check belongs to deal-risk-assessment, or to a
separate explicit price request.*

## Sources

Grouped by channel — EDGAR (form, date, accession number), company deal materials (8-K exhibit or
IR URL; slide numbers for deck-sourced facts), vector database (report title, institution,
analysts, publication date).

---

*This is a triage read, not the blind fundamental assessment. Run deal-risk-assessment for the
complete report — antitrust analysis, financials, litigation, and the tape check — when you're
ready to go deeper.*
