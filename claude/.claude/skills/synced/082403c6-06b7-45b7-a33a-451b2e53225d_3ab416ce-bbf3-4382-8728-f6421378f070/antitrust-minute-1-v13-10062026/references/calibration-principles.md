# Calibration principles — keep the verdict honest in both directions

Read this file in full during the gather window, and again just before locking Section A's verdict.

**Why this file exists.** A T+0 memo on Nielsen/DoubleVerify rated HSR clearance AMBER/MODERATE. The
deal then cleared HSR with no issues. Reading the memo back, the reservation did not come from bad
facts. It came from four reasoning habits that any deal can trigger:

1. A competitor named in the target's 10-K was treated as a real overlap. The target's own management,
   on earnings calls and at conferences, named a different company as its direct competitor and called
   the buyer complementary. That language was never checked.
2. One vivid unfavorable precedent (the buyer's 2012 Second Request on a direct-overlap deal) anchored
   the read. The buyer's full record was mixed: one clean HSR expiry in 70 days, one clean close in 137
   days, one Second Request in 286 days. Only the direct-overlap deal was troublesome.
3. A sell-side view that disagreed with the memo ("could clear without a second request, perhaps not
   even a pull-and-refile") was noted but not tested against the verdict.
4. "Is there overlap on paper," "will the regulator object," and "will the review be slow" were blended
   into one rating.

These principles fix the habits. They are **not** a lean toward clearing. A real horizontal overlap,
a high combined share, a prior Second Request on the same product line, or a merger agreement with a
large antitrust reverse fee must still push the verdict up. Every principle below runs both ways, and
the test for each one is "would this have moved the verdict on a deal that really does overlap?" If it
would not have, the principle is decoration and should be cut.

## 1. Overlap must be shown, not assumed

A name in a Competition section is a **candidate** overlap, not a finding. Before a candidate raises
the horizontal-overlap row above LOW, run four tests and write the result next to it:

- **Management's own words.** Search the *target's* and the *acquirer's* recent earnings-call
  transcripts, investor-day remarks and conference appearances for how each describes its direct
  competitors and the other party. A 10-K is drafted by counsel to be broad; a CEO on a call says who
  actually takes customers. Quote the language with the call date. If management names different
  rivals, or calls the other party a partner, supplier or complement, that outweighs a bare 10-K listing.
  If management names the other party as a head-to-head rival, that is strong overlap evidence, and the
  memo must say so.
- **Substitute or complement.** Would a customer buy one party's product instead of the other's
  (substitutes), or alongside it (complements)? Write the answer in one sentence.
- **Same customers, same purchase decision.** Do both sell to the same buyer inside that buyer's
  organization, for the same budget? Two products sold to different departments are not usually rivals.
- **Direction of the naming.** Who names whom? Only the target naming the buyer, with no rival naming
  either party and no management language to match, is thin. Both naming each other, or third-party
  rivals naming both, is strong. (See the two-direction check already in SKILL.md.)

Outcome of the four tests: **shown** (raise the row), **not shown** (keep at LOW, state what was
checked), or **unresolved** (say what would resolve it; a second research pass is required if the row
would otherwise be MODERATE or higher, per `gate-led-structure.md`).

## 2. Use the buyer's whole record, not its most memorable deal

For any repeat acquirer, list **every** prior acquisition that went through HSR review in the last
ten years (older ones only if in the same product line), each with: deal, year, overlap type (direct
horizontal / adjacent / complementary), outcome (cleared at expiry / pull-and-refile / Second Request /
consent decree / abandoned) and announce-to-close days. Then write the **outcome mix** in one sentence
("of N deals, X cleared at first expiry, Y drew a Second Request; both Second Requests were direct
overlaps"). Two rules follow:

- A precedent is read for what was combined. A Second Request on a direct-overlap deal says little about
  a complementary deal by the same buyer, and the memo has to say so. The reverse also holds: a clean
  history says little about a deal that really is a direct overlap.
- The single most memorable precedent never sets the verdict by itself. It is one row in the mix.

This adds to, and does not replace, the existing product-market-first ranking rule in SKILL.md.

## 3. Rate three different questions separately

Blending these is how a memo ends up saying "AMBER" when the honest answer is "probably clears, but
slowly." In Section A's matrix, keep three separate reads and label them in plain language:

- **Will the parties get through first review?** (No Second Request; possibly a pull-and-refile.)
  This is the "second-request risk" row.
- **Will the review run long?** Second Request, foreign or investment-screening filings, sector
  approvals, or a sequenced filing calendar. This is the existing OVERALL TIMING RISK row. Foreign
  filings that run in parallel and are likely to clear belong here, not in the challenge row.
- **Will a regulator sue or force a remedy?** This is the "challenge / remedy" read, and it stays LOW
  unless a real overlap (principle 1) exists. The existing Remedy / divestiture exposure row covers it.

The OVERALL ANTITRUST RISK TO COMPLETION row is then built from the first and third reads, not from the
second. Never let a timing concern lift the challenge rating, and never let a clean challenge rating
hide a genuine timing problem.

## 4. Steelman both neighbours before locking the verdict

Before Section A is final, write two short paragraphs into your working notes (they do not need to
appear in the memo unless the memo's verdict is not the middle case):

- The best honest case for **one level lower** risk than your draft verdict, using only sourced facts.
- The best honest case for **one level higher**.

Then say what specific evidence would move you to either neighbour, and which of those pieces of
evidence you actually looked for. If you find you never searched for the evidence that would have moved
you lower (or higher), search for it now. The memo's "what would have to be true for the view to be
wrong" sentence must come from this exercise, not be generic.

## 5. Test every disagreeing view; reconcile by trust tier

Whenever a sell-side note, desk comment, ArbJournal note, AlphaSense output or IB chat is present in
the conversation or in the pulls, and its read of overlap or clearance differs from your draft verdict,
do this before delivering:

1. Attribute it (firm, analyst, date) and place it in the trust tiers from the desk's sell-side
   priority list if one is available in this workspace (the `hour-1` skill keeps it in
   `references/sellside-priority.md`). If no tier list is available, say so and do not invent a ranking.
2. State the mechanism behind the disagreement: what fact or test does the other view rely on that
   this memo did not use? (For example: "relies on the target's earnings-call language naming a
   different direct competitor.")
3. Check that mechanism against a primary source yourself. Then say plainly whether the memo agrees,
   disagrees, or moves, and why.

A disagreeing view is a hypothesis to test, not a tie to break by tier alone. Tier decides how much
weight an unverified claim gets; a claim you have verified carries its own evidence.

**Where it shows up in the memo:** the "Other views" block in Section A (see `memo-template.md`). It is
required on every run: one line per view, or "No sell-side or desk view located." A view that agrees with
the draft verdict but gives no mechanism ("low likelihood of a second request given the buyer's history")
is noted and does not carry weight by itself; the memo names what would make it wrong.

At T+0 most notes do not yet exist (see "What exists on day one"). This principle applies whenever the
memo is re-run or refreshed after notes appear, and whenever the user pastes commentary into the chat.

## 6. Calibration is sourced or absent

Where an agency or law-firm tracker publishes a base rate that fits this deal's shape (for example the
share of HSR filings that draw a Second Request, or the share that receive early termination), cite it
with its source and date, and use it only to sanity-check the verdict, never to produce a point
probability. If no fitting published figure exists, write nothing. The existing rule against invented
market shares, HHI values and probability percentages stands unchanged.

## 7. Write the self-check into the deliverable

Add one sentence at the end of Section A, after the watch-list: **"Verdict stress-test:"**, naming (a)
the single fact that most supports the verdict, (b) the single fact that most cuts against it, and (c)
which one the memo weighted more and why. This costs two lines and lets a reader see the reasoning
that a bare RAG cell hides.

## Guardrails — what these principles must not do

- Do not lower a rating because a principle "could" support a lower rating. Lower it only when a
  sourced fact from a test above supports it, and say which test.
- Do not skip a principle because the deal looks clean. A clean deal passes the tests quickly and the
  memo says so in one sentence per test; that sentence is the evidence.
- Do not turn these principles into extra sections. They live inside Sections A, C and F.
- Keep the plain-language layer. Write "the target's own CEO named a different company as the main rival
  on its earnings call" rather than "management disclosure rebuts the mutual-listing inference."
