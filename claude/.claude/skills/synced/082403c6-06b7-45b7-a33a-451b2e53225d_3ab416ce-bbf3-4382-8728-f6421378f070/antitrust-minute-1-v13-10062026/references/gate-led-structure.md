# Gate-led structure — reordering, the irrelevance budget, and the mandatory second pass

This file governs three related changes to how the memo is composed once Section A's classification
(antitrust-gated / sector-gated / dual-gated — internal labels, never written into the memo) is
resolved. All three exist for the same reason: on a large fraction of real deals, the thing that
actually sets the closing date is not antitrust, and a memo that gives antitrust top billing by default
because that is the section this module knows how to write best has allocated its length exactly
backwards. This is not a new judgment — SKILL.md's "Regulatory intensity" and "Threshold framing"
sections already establish that Sections C and D *compress* on a sector-gated deal — but compression
alone is not enough. Live desk feedback on an earlier version of this module made the failure mode
concrete: a reader scrolling a memo that led with a thorough, well-sourced, but ultimately low-stakes
antitrust workup stopped reading before reaching the regulatory-timeline section that actually mattered,
because nothing in the memo's own structure told them to skip ahead.

Read this file during the gather window, alongside `references/memo-template.md`, once Agent E's
returns make the classification callable — which is usually before composition starts, since the
classification is meant to be resolved early (see SKILL.md's "Regulatory intensity" section).

## 1. Reorder around the gating classification, not just compress around it

**Once Section A's classification is resolved, restructure the memo's actual read order so the gating
item leads.** The six-section letter scheme (A through F, plus Section G) stays as the underlying
content model and the house-report mapping table in SKILL.md still applies unchanged — every fact still
has a home — but the *order in which a reader encounters them*, and the space each gets, follows the
gate, not the fixed letter sequence.

Concretely:

- **On an antitrust-gated deal**, the existing order (A → B → C → D → E → F → G) is already correct
  and needs no change — antitrust *is* the gating item, so leading with the verdict and the overlap
  analysis is leading with the thing that matters.
- **On a sector-gated deal**, after Section A's verdict (which still opens the memo — see the triage
  statement requirement below), the memo's weight and immediate next content should be the regulatory
  architecture and Approval Clock Build (Section E's material), not the overlap screen. In practice
  this means: state the verdict (A), state the triage explicitly (below), then go straight into the
  regulatory pathway and timeline build, with the compressed antitrust sections (C, D) following after
  — read as confirmatory detail for a reader who wants it, not as the main event. The section
  *numbering* in the delivered memo can still follow A/B/C/D/E/F/G for continuity with the house-report
  mapping table (so downstream consolidation isn't broken), but the *prose emphasis and space
  allocation* — which section is longest, which one the verdict paragraph points the reader toward next
  — follows the gate. Where it materially helps readability, it is also acceptable to physically reorder
  the delivered sections (e.g., present E before C/D) as long as the section labels stay attached to
  their content so a reader or a downstream consolidation step (`hour-1`) can still find "Section E" by
  that name; use judgment on which serves the reader better for a given deal, and default to reordering
  when the sector item is doing most of the work.
- **On a dual-gated deal**, both get full weight per the existing rule (SKILL.md's regulatory-intensity
  table); this file's reordering guidance does not apply the same way, since there is no single gating
  item to lead with — sequence by which clock is more likely to bind first, and say so.

## 2. The irrelevance budget — a hard cap, not a soft preference

**Any topic that RAG-scores LOW and is not the gating item is capped at roughly 15% of the memo's total
length, and does not get its own full table.** This sharpens SKILL.md's existing compression guidance
("Sections C and D compress to the overlap gate and its evidence... a two-page section D on a
market-extension deal is padding") into an enforceable ceiling rather than a stylistic preference,
because "compress" without a number is too easy to satisfy with a slightly-shorter version of the same
thorough treatment.

Apply it like this:

- **Estimate the budget before writing, not after.** Once the classification is resolved, a LOW-scored,
  non-gating topic (most commonly the antitrust analysis itself, on a sector-gated deal with a clean
  overlap screen) gets a length budget of roughly one-seventh of the memo — a short paragraph or two,
  not a section. Write to that budget rather than writing the full treatment and cutting it down
  afterward; the second approach tends to leave structural residue (a table stub, a half-argued
  narrow-vs-broad call) that reads as unfinished rather than as a deliberate compression.
- **No full table for a LOW, non-gating topic.** The Overlap Screen table, the Peer Set & Scale table,
  and similar required tables elsewhere in this module are still required *where the topic is the
  gating item or scores MODERATE+* — this budget does not waive them there. Where the topic is LOW and
  not gating, replace what would have been a table with a tight paragraph stating the finding, its
  source, and the one-line reasoning connecting them ("we looked and found nothing" is still a complete
  finding, per SKILL.md's existing rule — it just doesn't need a table to say it in).
- **The budget is a cap, not a target.** A LOW, non-gating topic that can be fully and honestly stated
  in three sentences should be three sentences — do not pad up to 15% to look proportionate. The number
  exists to stop over-investment, not to mandate a minimum.
- **This budget does not apply to Section G**, which has its own required shape (see
  `references/entry-price-target-irr.md`) regardless of how the classification comes back, and does not
  apply to the gating item itself, however long that legitimately needs to run.

## 3. Mandatory second research pass on anything MODERATE+ or still open

**Any item that scores MODERATE or higher, or that remains genuinely open or unresolved after the first
research pass, gets a second, targeted pass before the memo is delivered — it does not ride on a single
pass the way a LOW-scored item can.** This is stricter than SKILL.md's existing "Open questions and the
autonomous deep-dive pass," which screens the *finished* memo for items worth a follow-up; this rule
applies earlier, during composition itself, to stop a MODERATE+ finding from ever reaching the delivered
memo under-researched in the first place.

- **What triggers a second pass:** any risk-matrix row, overlap line, or regulatory-approval row rated
  MODERATE or HIGH; any item where the first pass's search came back with a hedge ("could not confirm,"
  "not determinable from public sources," "no disposition found") rather than a settled answer; and any
  item flagged as a candidate for the deep-dive pass under `references/open-questions-deep-dive.md`'s
  Step 1 screen — for those, this rule says do the second pass *before* delivery where it's feasible
  inside the gather window, rather than only as a post-delivery follow-up.
- **What the second pass looks like:** a targeted follow-up search or read specifically aimed at
  resolving the hedge or corroborating the MODERATE+ rating — not a repeat of the first pass's query.
  If the first pass searched the deal shape, the second pass searches the specific named entity, regime,
  or precedent that the first pass's results pointed toward. This is the same discipline SKILL.md
  already requires for market-share gap-filling (retarget to the closest analogous transaction) and for
  litigation-status checks (an affirmative disposition check, not a single search) — this rule
  generalizes that pattern to every MODERATE+ or open item, not just those two specific cases.
- **What "done" looks like:** either the second pass resolves the item to a settled, flatly-stated
  finding (apply the "hedge only what is actually uncertain" rule from SKILL.md once it's actually
  settled), or it doesn't — in which case the item remains open, is stated as open with the reasoning
  for why two passes couldn't close it, and becomes a candidate for the open-questions deep-dive pass
  per that reference file. A second pass that doesn't change the answer is still worth running — "we
  looked again and it holds" is a different, more confident state than "we looked once."

## Cross-reference: named-state granularity is part of the gating item, not a separate budget item

Where the gating item itself is a state-by-state licensing, change-of-control or **threshold-triggered notice-and-review** regime (state health care transaction laws are the v13 case; see `references/state-healthcare-regimes.md`; see
`references/gather-prompts.md`'s Agent E instructions for the specific fields to return — named states,
consent type, speed tier, must-have list, NMLS verification status), that granularity is part of what
"the gating item gets full weight" means under rule 1 above — it is not optional detail that could be
trimmed under rule 2's budget, because the budget only caps LOW, non-gating topics and a state-by-state
regime that is the gating item is by definition neither. An aggregate figure ("licensed in 46 states")
in place of the named-state breakdown is under-delivering the gating item's own required detail, not a
legitimate compression.
