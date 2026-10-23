# Open questions and the autonomous deep-dive pass

**The T+0 memo is not necessarily the end of the run.** The gather window is optimized for speed —
six agents, one block, ~3 minutes — and that optimization means a genuine idiosyncratic wrinkle gets a
one-line flag in the delivered memo (a Limitations entry, a risk-matrix row) rather than the
primary-source statute-and-rule read it actually needs. That is correct behaviour for the T+0 memo
itself — never slow the initial delivery down to chase it — but it is not correct behaviour for the run
as a whole. **Do not wait for the user to ask "can you dig into X" before doing it. Deliver the memo,
then keep going, in the same turn, without further prompting.**

**Step 1 — screen the finished memo for open questions before declaring the run done.** An open
question, for this purpose, is any item where (a) the memo's answer rests on a general rule, an
assumption, or a stated gap rather than a primary-source read specific to the actual entity or
jurisdiction involved, and (b) a wrong answer would move the base-case close date or the verdict by
more than a rounding error. Typical sources, drawn from how this has actually come up in practice:

- An ancillary licensed entity (a captive, a reciprocal, a small MGA-owned underwriter) whose specific
  state regime is not already built out in `references/regulatory-clocks.md` — Section E's build had to
  fall back on a general regime entry for that entity type by default, and the general entry is
  frequently wrong for it (see that file's captive-carve-out entry, added after exactly this gap
  surfaced on a real deal — check whether the same kind of gap exists for the entity in front of you).
- A buyer-archetype question the precedent set can't cleanly answer — e.g. "how does this regulator
  treat a first-time owner of this specific asset type" where the available precedents split into
  buckets that don't quite match this acquirer (a specialist-sponsor bucket and a different-asset-type
  bucket, with nothing in the exact cell). Report the mismatch itself as the finding (see SKILL.md's
  "Precedents" section), and treat closing that specific gap as an open question for the deep-dive pass
  rather than force-fitting an answer from the mismatched buckets.
- A regulator's discretionary posture that the statute leaves genuinely open (a waiver provision, a
  "facts and circumstances" standard) where only that regulator's own recent precedent order, not the
  statute text alone, can narrow the range.
- Anything the user's own reply in the same thread specifically asked about, even in passing — a
  question asked once should not require being asked twice.

**Step 2 — do the primary-source work immediately, without asking permission first.** For each open
question: read the actual statute or rule (not a secondary summary), pull the specific regulator's own
recent precedent order where one exists, and reason to a real band — not a shrug — the way Agent E's
brief already requires for the initial build. This is the same primary-source discipline as the rest of
this module; the only thing that changes is that it is now targeted at a small number of specific,
consequential questions instead of the full approval perimeter, so it should take a fraction of the
gather window's time, not repeat it.

**Step 3 — write the deep dive as a follow-up, not a silent revision.** Do not go back and quietly edit
the delivered T+0 memo. Deliver the deep dive as its own follow-up communication — a reply in the same
email thread the memo went out on, or a continuation message in chat, matching however the T+0 memo was
delivered — reasoning to a revised or sharpened view the way the rest of this module argues to a
conclusion (fact → why it matters → conclusion, `Assessment:` for opinion), rather than restating the
open question back to the reader. State plainly whether the deep dive changes the base case, narrows a
range, or confirms the T+0 read — a deep dive that confirms the original number is still worth sending,
because "researched further, unchanged" is a different and more useful state than "not yet checked."

**Step 4 — rank surviving open questions by materiality, and cut the ones that don't clear the bar
entirely.** Do not deliver a flat, unranked list. For every item that survived Step 1's screen and
Step 2's research, ask explicitly: **if this came back the other way, would the base-case close date or
the verdict actually move — not just move a sub-clause of the reasoning, the delivered date or verdict
itself?** Rank what remains from most to least consequential and state the ranking in the block itself
(highest first). Anything that would not move the date or verdict does not get a demoted or "minor" entry
— it is dropped from the delivered Open Questions block entirely, not listed at lower priority. This is a
change from treating every flagged item as worth reporting once it clears Step 1: Step 1 sets the bar for
what's worth *researching*, and materiality-ranking at Step 4 is a second, stricter filter on what's worth
*delivering* — an item can survive the first and still fail the second, and it should be cut rather than
padded into the section as a minor closer. A memo's Open Questions block is a target list for where a
reader's attention should go next, and a list padded with immaterial items trains the reader to skim past
all of it, including the entries that matter.

**Step 5 — close every surviving, materiality-ranked open question with a standalone, portable entry,
formatted per `references/memo-template.md`'s Open Questions — Cross-Model Verification format, even for
questions the deep dive fully answered.** This block is not just a to-do list for this module — it is
meant to be pasted, as-is, into another model (ChatGPT, Gemini, Perplexity) for an independent second
read, and it is the required input to `hour-1`'s Perplexity-council reconciliation step. Format each
entry so it stands alone: enough deal context in the question itself that a model with no memory of this
conversation could attempt it, this run's own working answer stated plainly (never withheld to make the
question look "neutral"), why it matters to the timeline or verdict, and — new — where it sits in the
materiality ranking from Step 4. A question the deep dive resolved outright still gets an entry — mark it
resolved, state the answer and its confidence, and say what would have to be true to change it; that is
what lets a later run, or another model, spend its effort on what is still genuinely open instead of
re-deriving what this run already nailed down.

**This does not apply to every run.** A clean antitrust-gated deal with no sector regulator on the
critical path and no buyer-archetype wrinkle will often close out with zero open questions — say so in
one line rather than manufacturing a question to fill the section. The bar is "would a wrong answer here
move the date or the verdict," not "is there anything left to look up" — and after Step 4's materiality
ranking, the delivered list should contain only items that clear that bar, ordered by how much they
clear it.
