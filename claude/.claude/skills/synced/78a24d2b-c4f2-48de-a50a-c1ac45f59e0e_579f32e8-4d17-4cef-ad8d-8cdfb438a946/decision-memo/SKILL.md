---
name: decision-memo
description: >
  Produce a structured trade-off memo for a decision — options, constraints, trade-offs, and a clear recommendation — instead of a freeform chat answer. Use ONLY when explicitly invoked — the user names this skill directly, types "/decision-memo", or says something like "use the decision-memo skill." Do NOT trigger on plain "help me decide" or "what do you think" requests — those get a normal answer. Good fit for technical decisions (migrations, architecture choices, tool/vendor picks) and non-technical ones (financial, strategic) alike — the format doesn't assume a domain.
---

# Decision Memo

Turns a decision into a structured, comparable memo: what's actually being decided, the real options, their trade-offs, and a clear recommendation — instead of a meandering chat answer that's hard to refer back to or compare against a future decision.

Output format depends on length/context: a short, low-stakes decision can stay a well-structured chat response; a decision with several options, real stakes, or something the user will want to reference or share later is a better fit for a saved markdown file. Use judgment — if in doubt, ask which they'd prefer rather than guessing wrong on a decision that matters.

## Step 1: Pin down the actual decision

State in one or two sentences exactly what's being decided. If the user's framing bundles multiple decisions together (e.g. "should we migrate the DB and also switch ORMs"), separate them — a memo that conflates two decisions produces a recommendation that doesn't actually answer either one cleanly.

## Step 2: Gather the real constraints

Before comparing options, get the constraints that actually bound the decision — don't let the memo float in the abstract:
- Hard constraints (budget, timeline, team size/skillset, existing stack, compliance/regulatory, backward compatibility needs)
- What "good" looks like here — the actual criteria this decision will be judged against (cost, latency, risk, reversibility, time-to-ship, whatever applies)
- Who else is affected or needs to sign off, if relevant

If this context already exists in the conversation or uploaded material, use it — don't re-ask for what's already been said. Only ask for what's missing and would actually change the recommendation; state a reasonable assumption and proceed rather than blocking on minor unknowns.

## Step 3: Lay out the real options

List the options actually worth comparing — usually 2-4. Don't pad with a strawman option included only to be dismissed; every option listed should be one a reasonable person in this position might actually pick. If the user only gave one option ("should I do X"), the honest second option is usually "don't" (status quo / do nothing) — include it unless it's clearly not viable, since that comparison is often what makes the recommendation legible.

For each option, cover:
- What it actually involves (concretely, not just a label)
- What it optimizes for / its real advantage
- What it costs or risks — the honest trade-off, not a token downside

## Step 4: Compare against the constraints from Step 2

Explicitly connect each option back to the criteria established in Step 2 — this is what makes the options comparable rather than just a list of pros/cons in isolation. A table or clearly parallel structure across options works well here since it makes the comparison scannable.

## Step 5: Recommend

Give one clear recommendation, not a hedge. State it plainly, then give the actual reasoning — which constraint or criterion tipped it, and what would have to change for the recommendation to flip. If it's genuinely close between two options, say so and say what the tiebreaker was, rather than manufacturing false confidence.

Note any risk or condition attached to the recommendation (e.g. "recommended assuming timeline stays flexible — if it's fixed, option B is safer") so the recommendation is falsifiable, not just asserted.

## Style rules

- One clear recommendation per memo — no "it depends" without actually resolving what it depends on.
- Every stated trade-off must be a real one — don't inflate a minor consideration to make the comparison look more rigorous than it is.
- Keep options and comparisons parallel in structure so they're actually comparable side by side, not described in inconsistent terms.
- Domain-agnostic: the same structure should work for a database migration decision and a financial allocation decision — don't bake in technical-only or finance-only assumptions.
