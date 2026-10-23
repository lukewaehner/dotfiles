---
name: red-team
description: >
  Adversarially attack an argument, plan, pitch, thesis, or piece of writing — take the strongest opposing position and find its weakest points, without requiring code or any specific input type. Use ONLY when explicitly invoked — the user names this skill directly, types "/red-team", or says something like "use the red-team skill" or "red-team this." Do NOT trigger on plain "what do you think of this" or "any feedback" requests — those get a normal answer. Domain-agnostic: works on a memo, a trade thesis, a proposal, a piece of writing, a plan, or a claim.
---

# Red Team

Attacks whatever is put in front of it — an argument, plan, pitch, thesis, proposal, or piece of writing — from the strongest good-faith opposing position available. The goal is to find real weaknesses before someone else does, not to be contrarian for its own sake.

Output format depends on length/context: a quick red-team of a short argument fits a chat response; a full red-team of a substantial document (a real proposal, a trade thesis with real capital behind it) may be better as a saved file the user can reference alongside the original.

## Ground rule: steelman before you attack

Before attacking, state the position being red-teamed in its strongest form — the best version of the argument, not a weakened strawman. If the original is already well-argued, say so; the value of this skill comes from a genuinely honest adversarial pass, not from a rigged fight the original was always going to lose. An attack on a strawman is worthless to the user — they need to know what the *real* best objection is.

## Step 1: Identify what's actually being claimed

State the core claim(s) or decision being defended, in the terms the source itself uses. If there are several claims bundled together, separate them — a red-team that attacks a vague blend of claims produces vague objections that are easy to wave away.

## Step 2: Find the load-bearing points

Identify which parts of the argument/plan are actually doing the work — the assumptions or steps that, if wrong, bring the whole thing down — versus decoration that doesn't matter much either way. Focus the attack there. A red-team that spends equal energy on a minor phrasing issue and a fatal load-bearing assumption isn't useful; weight matters.

## Step 3: Attack from the strongest opposing position

For each load-bearing point, find the strongest real objection:
- **Wrong assumption** — what's being taken for granted that might not hold, and what evidence would actually test it
- **Missing consideration** — what a sophisticated opponent, competitor, or skeptic would immediately bring up that isn't addressed
- **Weak evidence** — where the support offered doesn't actually prove the claim it's attached to, or generalizes past what the evidence supports
- **Better alternative** — where a different choice would clearly outperform this one under the same constraints
- **Failure mode** — the specific way this goes wrong in practice, not just "it might not work"

Each objection should be the kind a smart, informed critic would actually raise — not a technicality or a bad-faith gotcha. If you can't find a real objection in a category, skip it rather than manufacturing a weak one to pad the list.

## Step 4: Weigh the objections

Not every objection found is equally serious. Close by ranking or at least distinguishing which objections are fatal (would actually change the decision/conclusion) versus which are real but survivable (worth addressing, wouldn't sink it). Don't leave the user unable to tell a dealbreaker from a nitpick.

## Step 5: Leave the verdict open

This skill's job is to surface the strongest attack, not to render a final verdict on whether the original position survives — that's the user's call once they see the objections. Don't soften the final read into "but overall it's fine" unless the objections genuinely turned out to be minor; equally, don't manufacture a dramatic takedown for content that actually held up well.

## Style rules

- Argue the opposing case as if you actually believed it — half-hearted objections aren't useful.
- Every objection must be specific to this argument/plan, not a generic "consider the risks" template applied to anything.
- Rank by severity — don't present a fatal flaw and a minor quibble with equal weight.
- If the source is genuinely strong, say so plainly rather than inventing weaknesses to justify the exercise.
