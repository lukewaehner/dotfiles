---
name: first-principles
description: >
  Break a claim, system, or plan down to its actual load-bearing assumptions and rebuild the reasoning from there, flagging which assumptions are solid, borrowed, or unexamined. Use ONLY when explicitly invoked — the user names this skill directly, types "/first-principles", or says something like "use the first-principles skill" or "break this down from first principles." Do NOT trigger on plain "explain X" or "why is this true" requests — those get a normal answer. Domain-agnostic: works on a belief, a business plan, a technical design, a strategy, or a claim someone else made.
---

# First Principles

Takes a claim, system, plan, or belief and breaks it down to the assumptions it actually rests on — then checks each one and rebuilds the reasoning back up. This is different from explaining how something works (that's `deep-dive`): this interrogates *why it's believed to be true or the right approach at all*.

Output format depends on length/context: a quick breakdown of a single claim fits a chat response; a full breakdown of a complex plan or system is often clearer as a saved file with the assumption tree laid out.

## Step 1: State the claim/conclusion plainly

Restate what's actually being asserted or planned, precisely — not a vaguer or stronger version than what was actually claimed. If the claim is really several stacked claims, note that up front.

## Step 2: Decompose into assumptions

Work backward from the conclusion: what has to be true for this to hold? Keep decomposing until you hit assumptions that are either (a) genuinely self-evident / directly verifiable, or (b) borrowed from somewhere else (an authority, a convention, "that's how it's usually done," a prior result taken on faith). Don't stop decomposing early just because an assumption sounds reasonable — the point of the exercise is finding the ones that only sound reasonable because they're unexamined.

Lay these out as a visible structure (a list or tree, not buried in prose) so the user can see the actual chain from foundational assumption to final conclusion.

## Step 3: Classify each assumption

For each one, be explicit about its status:
- **Solid** — actually verifiable or directly demonstrable; state how you'd check it if not already checked.
- **Borrowed** — taken from convention, authority, precedent, or "that's just how it's done" without independent verification here. Not automatically wrong, but worth knowing it hasn't been independently checked in this context.
- **Unexamined / shaky** — asserted without real support, or resting on something that doesn't actually hold up under a first-principles look. This is where the real risk usually is.

Don't inflate a genuinely solid assumption into a manufactured doubt just to have something in every category — if an assumption is well-founded, say so plainly and move on.

## Step 4: Rebuild from the ground up

Once the assumptions are classified, reconstruct the reasoning starting only from what's actually solid. See what the argument looks like built back up from verified ground rather than from convention — does the original conclusion still follow, does it follow more weakly, or does a different conclusion actually fit the solid foundation better?

## Step 5: State what changes

Close with what this exercise actually revealed: did the original conclusion survive intact, survive with caveats, or fall apart once the borrowed/shaky assumptions were stripped out? Be direct about it — the point of doing this is to find out, not to perform rigor and then quietly reaffirm whatever was already believed.

## Style rules

- Every assumption named must be a real load-bearing one — not padding to make the tree look more thorough.
- Distinguish clearly between "unverified" and "wrong" — a borrowed assumption isn't automatically false, just unconfirmed here.
- Don't manufacture doubt about assumptions that are actually solid; the classification should be honest, not performatively skeptical.
- The rebuild in Step 4 is the point of the exercise — don't skip straight from "here are the assumptions" to a verdict without actually reconstructing from the solid ground up.
