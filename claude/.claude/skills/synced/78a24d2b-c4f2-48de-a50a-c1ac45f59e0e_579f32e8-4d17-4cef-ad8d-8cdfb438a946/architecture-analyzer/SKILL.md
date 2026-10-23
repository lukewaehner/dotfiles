---
name: architecture-analyzer
description: Dissect software/programming architecture and code for unconsidered edge cases, structural inefficiencies, and weak points, then suggest concrete fixes grounded in the actual context. Use ONLY when explicitly invoked — the user names this skill directly, types "/architecture-analyzer", or says something like "use the architecture-analyzer skill." Do NOT trigger on plain "review my code" or "what do you think of this design" requests — those get a normal answer. Works on code/design already in the conversation, uploaded files, or a project directory on disk if given a path.
---

# Architecture Analyzer

Finds what's wrong or unconsidered in a software architecture or codebase — edge cases nobody handled, structural inefficiencies, and weak points — then proposes fixes that are grounded in the actual system, not generic best-practice advice.

Output is a plain markdown chat response — no file, no artifact.

## Step 1: Gather context

Before analyzing anything, make sure there's enough real material to analyze:

- Use whatever is already available: code pasted or uploaded in the conversation, files already read, or a project directory/path the user gives you (read it directly if so — don't ask them to paste it in if you can just read it).
- If a path is given, get a real sense of the actual structure (view the directory, read the key files) rather than analyzing based on the path name or a guess at what's probably in there.
- Do not fabricate or assume the contents of code you haven't actually seen.

## Step 2: Decide if you have enough to work with

Before producing an analysis, check whether you actually understand:
- What the system does and who/what depends on it
- The scale and load it's expected to handle (roughly)
- Any hard constraints already in play (existing stack, team size, latency/cost budgets, compliance needs) that would rule out otherwise-reasonable fixes

If critical context is missing and guessing would make the analysis generic or wrong, ask — but keep it targeted. Ask only for what actually changes the analysis, not a general intake questionnaire. If you can infer or reasonably assume something (e.g. "this looks like a typical CRUD API, I'll assume standard REST semantics unless told otherwise"), state the assumption and proceed rather than stopping to ask.

If you already have enough to produce a real analysis (the code/design itself often answers most of this), skip straight to Step 3.

## Step 3: Analyze

Work through the system looking for these categories. Not every category will apply to every system — skip ones that genuinely don't apply rather than padding.

### Edge cases not considered
Concrete scenarios the current design doesn't handle: empty/null inputs, concurrent access, partial failures, retries and idempotency, boundary values, ordering assumptions, what happens when a dependency is slow/down/returns garbage. Name the specific scenario and trace what actually happens in the current code/design when it occurs — not just "consider edge cases."

### Architecture inefficiencies
Places where the structure does more work than it needs to, or makes a later change harder than it should be: unnecessary coupling, redundant computation or storage, chatty calls that could be batched, layers that don't earn their complexity, missing caching or caching in the wrong place, N+1 patterns, premature or misapplied abstraction.

### Weak points / flaws
Places the system is fragile: single points of failure, missing error handling or overly broad catch-alls that hide problems, race conditions, unclear ownership of state, security gaps (auth, input validation, secrets handling), things that will silently do the wrong thing rather than fail loudly.

For each issue found, be specific: point to the actual place in the code/design it lives, and briefly say why it matters (what breaks, when, under what conditions) rather than just labeling it a smell.

## Step 4: Suggest fixes

For each significant issue raised, suggest a concrete fix — not just "add error handling" but what the fix actually looks like given this system's real constraints (its existing stack, scale, and whatever context was gathered in Step 1-2). If a fix has a real trade-off (more complexity for more robustness, cost vs. latency, etc.), say so briefly rather than presenting it as free.

If a fix genuinely depends on information you don't have (e.g. "this is only worth fixing if you're expecting concurrent writers — are you?"), ask rather than guessing, but don't let this block reporting the issues you can already state confidently.

## Style rules

- Prioritize: lead with what actually matters most (correctness and reliability issues before minor inefficiencies), don't give every finding equal weight.
- Be direct about severity — don't soften a real flaw into a vague "you might consider," but don't manufacture issues to pad the list either. If the architecture is solid, say so.
- Ground everything in the actual code/design in front of you — no generic "best practices" lecture disconnected from what's actually there.
- Skip categories or sections that don't apply rather than forcing structure onto a system that doesn't have that kind of issue.
