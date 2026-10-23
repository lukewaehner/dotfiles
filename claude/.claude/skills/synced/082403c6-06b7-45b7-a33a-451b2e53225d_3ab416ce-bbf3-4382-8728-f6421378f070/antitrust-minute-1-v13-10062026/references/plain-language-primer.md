# Plain-Language Layer — "Regulatory Considerations" for a reader new to the industry

Read this file in full during the gather window, alongside `memo-template.md`. It adds a layer the
earlier versions of this module lacked: a memo that a reader who has never worked in the target's
industry can follow from the first paragraph, with the numbers laid out in fixed tables. It exists
because a memo can be analytically correct and still leave the reader assembling the business
picture from scattered sentences — on a live deal the reader asks "what do these two companies
actually do and how do they make money?" before any theory of harm means anything to them.

This layer **adds subsections inside B, C and D. It does not add sections, does not reorder A–G,
and does not override the gate-led length budget** (`gate-led-structure.md`). Where the gating item
is a sector regulator, the primer stays compact and the Approval Clock Build keeps its weight.

## Writing register for this layer

Write for a smart reader from another field. Simple, self-explanatory sentences. The first time a
term appears (PBX, SIP trunking, HHI, second request, plan of arrangement), say what it means in
the same sentence. No buzzwords: say "monthly subscription per user", not "recurring-revenue SaaS
platform". Take baby steps — market first, then where each party sits, then overlap, then harm. Every
table is followed by a short paragraph saying what it means. This layer is the one place in the
memo where a definition inside a sentence is required, not optional.

## B.0 — The companies in plain English (required, every deal)

Five items, in this order, for **both** the target and the acquirer. On a financial-sponsor buyer the
"acquirer" here is the sponsor's relevant platform or portfolio company, never the fund (the
sponsor invariant in SKILL.md still governs) — one line on what the fund is, then the platform.

1. **What they do and how they make money.** Two to four sentences each, then the revenue mix in
   words (for example "about 92% is monthly subscriptions and usage fees"). Name the customer
   (small business, consumer, bank) and the way they are reached (direct, resellers).
2. **Business segments.** Name each reportable segment and what it sells in one clause. Where the
   company reports a single segment, say so, and describe its product groups while stating that
   revenue for each group is not disclosed.
3. **Revenue by segment table — most recent fiscal year.** Columns: Segment | Revenue | % of total.
   **Formatting rule (the user's standing instruction): dollar figures in millions written as a bare
   dollar amount, for example `$164.1`. Do not append "mm" or "M" and do not write the word
   "millions" anywhere in the table, its header or its caption.** The % column sits immediately to the
   right of the revenue column, to one decimal place, and must sum to 100.0% (say so if rounding
   leaves 99.9% or 100.1%). Include a Total row that ties to the filing's own total. Where the
   company reports one segment, use revenue by type (for example products vs. services) and say so.
   Source (form, note number, filing date) goes in the caption — with a link. Because the table itself
   carries no unit word, put one plain sentence directly **below** each table: "Dollar figures are in
   millions of US dollars." (The ban covers the table, header and caption, not the sentence after.)
4. **Revenue by geography table — most recent fiscal year.** Same format and same formatting rule.
   Keep the filing's own region labels. If a filing does not split the way the reader expects
   (for example "North America" combined, no U.S.-only figure), say that in the caption and do not
   split it yourself.
5. **History and past mergers and acquisitions.** Two or three sentences on founding and listing,
   then a table: Deal | Date | Price or terms | Source. Include divestitures. Mark anything sourced to a
   single secondary source (an encyclopedia page, a trade-press article) as such and never mix it into
   the filing-sourced rows without the label. Where two sources conflict on a fact (for example
   headquarters), prefer the company's own most recent filing, state the conflict in one sentence,
   and do not silently pick.

Then the **bad-actor check** (B.4 in the template; see below).

## B.4 — Bad-actor check (required, every deal)

The question the reader is asking: does either party have a record that could change how a
regulator, a court, or the other side's lawyers treat this deal? Answer for the **target** first, in
one direct sentence ("No — ..."/"Yes — ..."), then support it:

- Legal proceedings and regulatory actions as the company itself discloses them (quote the sentence).
- Internal-control weaknesses, restatements or revisions, auditor changes — with amounts where given.
  Distinguish a **revision** (prior-period numbers corrected in the next filing, no formal restatement)
  from a **restatement**, and say which one the filing uses.
- Short-seller reports, class actions, agency enforcement (FCC, FTC, SEC, state AGs), data breaches —
  each as an explicit positive or negative finding naming where you searched. A search that ran and
  found nothing is a finding; say so with the search named.
- Then the **same check on the acquirer**, because that is often where the deal-relevant record sits
  (for example a consent decree at a subsidiary that the sector regulator will read). Say which
  regulator or approval each item bears on, and whether it belongs to the competition analysis or the
  sector-regulator rows. Conduct problems almost never change the competition verdict; they change
  the substance and duration rows of the sector approvals. Say that explicitly rather than leaving the
  reader to guess.

Label your conclusion `Assessment:`. An accounting weakness at the target is a diligence and
closing-condition point (bring-down of representations), not an antitrust factor — say so.

## C.0 — Antitrust in baby steps (required, every deal)

Open Section C with a short numbered walk, not a table. Five steps:

1. **How the market works.** What the customer used to buy, what they buy now, and who sells it, in
   three tiers if that is the true structure (very large, mid-size, small/resellers). Name the rivals
   the parties' own filings name.
2. **Where each party fits.** Scale in dollars from B.0, the customer each sells to, the geography.
3. **Is there an overlap?** A yes/no answer first, then a table: BRC or buyer-side unit | target line |
   overlap type | evidence. Most of the buyer's units will read "none" — that is the finding, and it
   is what stops the reader from assuming the whole buyer competes with the target.
4. **If there is an overlap, explain it simply but in detail.** Who the customers are, why they
   would or would not switch, what the other choices are. Then the market-share statement.
5. **Market shares by jurisdiction.** Give sourced shares for each jurisdiction where a citable
   source exists, each with a link. Where none exists, write one sentence saying so and naming the
   sources tried, and do not compute an estimate from stale or adjacent figures — the "never estimate
   shares" rule in SKILL.md is unchanged and outranks this layer. A stale or adjacent-market figure
   may appear only in the Market Structure table, labelled as such with its date.

**Every jurisdiction in E.1 gets a row in the antitrust analysis, not only the U.S.** Build a
Jurisdiction table: Jurisdiction | Filing required? (with the test and the figures) | Overlap in that
jurisdiction | Market-share data (or "none located"). Use the six screens in
`foreign-merger-thresholds.md` (EU, UK, China, Australia, Canada's Competition Act, Investment Canada
Act) so the table and E.1 cannot disagree. A regime that is not notifiable still gets its row and one
sentence on whether the agency could review anyway; if you have not verified that, say so.

## D.0 — HSR merger-guidelines table (required wherever HSR applies)

Complete the full 11-guideline table below. Do not omit rows that are clearly "No" — a full table is
what shows the reader nothing was skipped. Columns: **Guideline # | Guideline | Analysis | Triggered?
(Yes / No / Maybe)**. The wording of each guideline is the current U.S. Merger Guidelines' own
heading; reproduce it exactly:

1. Mergers raise a presumption of illegality when they significantly increase concentration in a
   highly concentrated market. — followed by sub-row **1a**: Agencies use the Herfindahl-Hirschman
   Index (HHI) and consider a post-merger HHI greater than 1,800 to be a highly-concentrated market;
   the threshold used to be greater than 2,500. (Also state, in the analysis cell, the second prong:
   a combined share above 30% with a change above 100 points.) Explain HHI in one sentence — add up
   each seller's squared market share.
2. Mergers can violate the law when they eliminate substantial competition between firms.
3. Mergers can violate the law when they increase the risk of coordination.
4. Mergers can violate the law when they eliminate a potential entrant in a concentrated market.
5. Mergers can violate the law when they create a firm that may limit access to products or services
   that its rivals use to compete.
6. Mergers can violate the law when they entrench or extend a dominant position.
7. When an industry undergoes a trend toward consolidation, the agencies consider whether it
   increases the risk a merger may substantially lessen competition or tend to create a monopoly.
8. When a merger is part of a series of multiple acquisitions, the agencies may examine the whole
   series.
9. When a merger involves a multi-sided platform, the agencies examine competition between
   platforms, on a platform, or to displace a platform.
10. When a merger involves competing buyers, the agencies examine whether it may substantially
    lessen competition for workers, creators, suppliers, or other providers.
11. When an acquisition involves partial ownership or minority interests, the agencies examine its
    impact on competition.

Honesty rules for the table:

- **"Triggered?" means "is this guideline engaged on the facts", not "will the deal be blocked".**
  Row 8 is "Yes" for any buyer with a string of same-line deals even when no harm is shown; say in the
  Analysis cell that engaged is not the same as harmful.
- **Row 1 is "No (not measurable)" when no share or HHI data exists, and that is a weaker statement
  than a flat "No".** Say so in the cell. Never let a soft "No" read like a computed one. If a
  narrow market definition would make the answer "Maybe", say that in the cell.
- Ground each Analysis cell in a fact from this memo (a named rival list, a revenue figure, a quoted
  sentence from a filing) — not in a general statement about the guideline. Quote the parties'
  own filings where they speak to the guideline (for example a filing acknowledging an industry
  consolidation trend is direct evidence for row 7).
- Rows 5, 7 and 11 are where a deal with a small overlap most often earns a "Maybe" the first
  pass missed. Test them deliberately: who buys the target's inputs, does the target's own filing
  describe consolidation, and does the buyer hold any partial interest in a related business.
- If HSR does not apply, say so in one line, name the reason (threshold), and skip the table.

## Length discipline

This layer adds about a page and a half of tables and short paragraphs. A test run on SANG/RILY came
back about 80% longer than the prior version, so these caps are hard: B.0 items 1–2 at most 4
sentences per company; history table at most 8 rows (largest and most recent deals; say "others
omitted"); B.4 at most one short paragraph per party plus a findings list; C.0 steps 1–4 at most 3
sentences each; every D.0 Analysis cell at most 2 sentences. Do not repeat a fact already stated in B.0
inside C.0 or D.0 — point back to it. Target: the memo grows by no more than about 25% over a memo
without this layer. Do not let it push the
gating regulator's analysis down or shorten the Approval Clock Build. If the memo is running long,
compress the history table and the D.0 Analysis cells before cutting anything from Section E.
