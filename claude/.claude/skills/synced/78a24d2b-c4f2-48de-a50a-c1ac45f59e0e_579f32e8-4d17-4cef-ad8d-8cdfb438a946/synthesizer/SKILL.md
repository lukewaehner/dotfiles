---
name: synthesizer
description: >
  Condense text, documents, or large content dumps into a strictly factual, no-frills consolidation — every substantive point covered, nothing added. Use ONLY when explicitly invoked — the user names this skill directly, types "/synthesizer", or says something like "use the synthesizer skill" or "synthesize this." Do NOT trigger on plain "summarize this" or "tl;dr" requests — those get a normal answer. Purely a content organizer, with no commentary, no "consider this," no hypotheticals, and no emotional framing — just clear structure and a closing recap.
---

# Synthesizer

Condenses input text, documents, or large content dumps into a clean, factual consolidation. This is pure content organization — not analysis, not commentary, not "here's what you should think about this."

## Core constraints (non-negotiable)

- **Strictly factual.** Only what's actually in the source. No inference, no speculation, no filling gaps with plausible-sounding detail.
- **No hypotheticals.** Never "imagine if..." or "this could mean...". If the source doesn't state it, it doesn't appear.
- **No emotional or evaluative language.** No "impressively," "unfortunately," "it's worth noting that this is concerning," etc. State what the source says, not how to feel about it.
- **No directive framing.** Never "dive into this," "consider this," "you should look at X" — this skill organizes content, it doesn't recommend next actions or steer attention.
- **Complete coverage.** Every substantive point/aspect in the source should be represented somewhere in the output, even briefly. This is consolidation, not selective highlighting — don't quietly drop a section of the source because it seemed less important; condense it down instead.

## Process

### 1. Identify the natural structure

Before writing, work out how the source is actually organized — sections, chronological sequence, distinct topics, arguments and counterarguments, whatever it actually is. The output structure should mirror the source's real structure, not a generic template forced onto it. A meeting transcript, a research paper, and a sprawling email thread each organize very differently — match the output shape to the input, not the other way around.

### 2. Condense section by section

Work through the source's natural sections/topics and condense each into a tight, factual form using whichever of these fits that particular content best:
- **Bullet points** — for discrete facts, lists of items, decisions made, action items, data points.
- **Short prose** — for content that's inherently a flow of reasoning or narrative and would lose meaning chopped into bullets.

Mixing both within one output is fine and often correct — a section of prose followed by a bulleted list of decisions from that section, for instance. Pick per-section based on what actually preserves the information most clearly, not one style for the whole document.

Use clear section headers matching the source's real divisions so the output is scannable.

### 3. Close with a TL;DR / recap

End every output with a short recap section (label it clearly, e.g. "TL;DR" or "Recap") that compresses the entire piece down to its most essential points — a few bullets or a couple of sentences, not a re-summary of every section. This is the "if you only read one part" distillation.

## Scaling to input size

- **Short input** (a few paragraphs, a short email): a brief plain-response condensation is enough — section structure may not even be needed, just tight prose or a few bullets plus a one-line recap.
- **Long input** (a full document, a large transcript, multiple files): use full section structure with headers, condense each section, and close with a proper TL;DR. For genuinely long output, a saved markdown file may serve the user better than a wall of chat text — use judgment on when a file is more usable than an inline response, and check the general file-creation guidance for the threshold (length, whether they'll want to keep/reference it later) rather than defaulting to one or the other.
- **Multiple documents/sources at once**: condense each source's content into the structure, but also make clear (via headers or clear labeling) which points came from which source if the sources are meaningfully distinct — don't blur them into one undifferentiated mass unless the user's request suggests a single merged view is what's wanted.

## What this skill does not do

- Does not add opinions, evaluations, or recommendations.
- Does not flag what it thinks is "most important" beyond the natural TL;DR distillation — no editorializing about what deserves attention.
- Does not extrapolate beyond what the source states.
- Does not suggest follow-up actions or further reading unless the source itself explicitly contains those (e.g. an actual action-items list in a meeting transcript — that's a fact from the source, not commentary).
