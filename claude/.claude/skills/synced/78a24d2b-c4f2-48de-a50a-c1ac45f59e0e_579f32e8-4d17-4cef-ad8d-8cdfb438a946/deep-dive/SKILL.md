---
name: deep-dive
description: Go deep and narrow on a specific sub-topic or nuance — the opposite of a breadth-first overview. Use ONLY when explicitly invoked — the user names this skill directly, types "/deep-dive", or says something like "use the deep-dive skill" or "deep dive into X." Do NOT trigger on plain "explain X" or "tell me more about X" requests — those get a normal answer. Pairs naturally with concept-explainer (a map-level explanation followed by a deep-dive into one landmark from that map) but does not require it — can be invoked cold on any specific technical nuance.
---

# Deep Dive

Goes deep and narrow on one specific concept or nuance, in contrast to `concept-explainer`'s breadth-first map. Assume the reader can handle real technical vocabulary used precisely and directly — don't pre-translate jargon into plain-language intuition first the way concept-explainer does. This is the "now that I know this exists, actually explain it" response.

Output is a plain markdown chat response — no file, no artifact.

## The shape of a good deep-dive

### 1. Pin down the scope

Open by stating precisely what nuance/sub-topic this dive is about — one or two sentences. If the topic could mean several different things depending on context (e.g. "cache" could mean CPU cache, browser cache, or a caching layer in a distributed system), pick the most likely one given the conversation and say which one you're running with, rather than trying to cover all of them shallowly.

### 2. Check for relevant prior context — but don't force it

Before diving in, consider whether this conversation (or, if it seems genuinely relevant, past conversations via `conversation_search`) already touched this topic or something that connects to it — a prior explanation, a project the user mentioned, a related question they asked.

- If there's a real, specific connection, weave it in naturally: "Earlier when we talked about X, this is the piece that..." — and let that connection actually change the explanation (motivate why this nuance matters given what they were doing), not just namedrop the earlier topic.
- If nothing connects, or the connection would be a stretch, skip this entirely. Don't force a callback that doesn't add anything — a deep-dive that opens with a strained "as we discussed" when nothing was really discussed reads as noise, not context-awareness.
- Only search past conversations (outside the current one) when there's a real signal worth checking — not as a reflex on every deep-dive.

### 3. Explain the mechanism, precisely

This is the core of the response. Explain how the thing actually works — not just what it's for. Use the correct technical vocabulary throughout, and define any term precisely the first time it's used, but don't stop to build up plain-language intuition the way concept-explainer does — assume the reader can sit with a real definition.

Go as deep as the topic supports:
- The actual mechanism/process, step by step where relevant.
- How it connects to or interacts with adjacent concepts (what it depends on, what depends on it).
- Where the nuance or subtlety actually lives — the part that's easy to get wrong or oversimplify, since that's usually why someone wants a deep-dive instead of the overview.

### 4. Use cases and applications

Cover where this actually gets used or matters in practice — what problems it solves, what breaks or degrades if you don't understand it, what decisions in the real world hinge on it.

### 5. Real-world example(s)

Ground the mechanism in at least one concrete, real example — an actual system, a specific scenario with plausible details, or a well-known case where this nuance mattered. Prefer specificity (real numbers, real systems, real failure modes) over a generic hypothetical.

### 6. Where it connects outward (optional close)

If useful, briefly note adjacent nuances or related deep-dives this naturally leads into — not as a forced "want to know more?" pitch, just as an honest map of what's next to this, for the reader's own sense of what else is out there.

## Style rules

- Depth over breadth: it's fine, expected even, to spend the whole response on one mechanism rather than surveying several.
- Use precise technical vocabulary directly — no need to soften or pre-translate the way concept-explainer does, though still define terms the first time they appear.
- Prior-context callbacks are additive only — include them when they genuinely sharpen the explanation, never as filler or forced continuity.
- Don't pad with caveats or exhaustively cover every edge case — go deep on the actual nuance the user is asking about, not everything adjacent to it.
- Length should track how deep the topic actually goes, not a fixed target.
