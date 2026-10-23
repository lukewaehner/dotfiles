---
name: runbook-writer
description: >
  Turn a process described in freeform terms — or done once ad hoc — into a clean, repeatable step-by-step procedure someone else (or future-you) could follow without you in the room. Use ONLY when explicitly invoked — the user names this skill directly, types "/runbook-writer", or says something like "use the runbook-writer skill" or "turn this into a runbook." Do NOT trigger on plain "how do I do X" or "walk me through X" requests — those get a normal answer. Domain-agnostic: works for a deploy process, an onboarding flow, a recurring data pipeline step, a household task, or anything explained more than once.
---

# Runbook Writer

Converts a process — described freeform, reconstructed from a conversation about how something was done, or given as rough notes — into a clean, repeatable runbook that someone with less context could actually follow.

Output format depends on length/context: a short process fits a chat response; anything meant to actually be kept, followed repeatedly, or handed to someone else is almost always better as a saved file.

## Step 1: Extract the actual process

Work from whatever's given — a freeform description, a reconstruction of "here's what I did last time," logs/commands/steps already in the conversation. Pull out the real sequence of steps actually required, in the order they need to happen. If steps were described out of order or with asides, reorder them into the clean sequence — the runbook should read as the ideal walkthrough, not a transcript of how it was explained.

## Step 2: Identify what's assumed vs. what must be stated

A runbook fails when it assumes context the follower doesn't have. For each step, check: would someone with less context than the person who wrote this actually know how to do it as written? Make explicit:
- Prerequisites (access, tools, credentials, prior steps) needed before starting
- Anything environment-specific (which machine, which account, which directory) that isn't obvious
- Decision points — where the process branches based on a condition, state the condition and both paths clearly rather than assuming the "obvious" branch

Don't over-explain things a reasonable follower would already know (don't explain what `cd` does) — the goal is filling real context gaps, not padding.

## Step 3: Write the steps

Each step should be:
- **Actionable** — a concrete action, not a vague goal ("run `X`" not "make sure X is configured")
- **Verifiable** — where possible, note what success looks like for that step (expected output, a state change, a place to check) so the follower knows whether it worked before moving on
- **Self-contained** — numbered/ordered so the follower can pick up mid-process if needed, without having to hold the whole thing in their head

Include the exact commands, paths, URLs, or values where they're part of the actual process — don't paraphrase specifics into vague description.

## Step 4: Cover what to do when it goes wrong

For steps with a known failure mode (something that commonly breaks, a step that requires a specific state to already be true, a place where the process is fragile), add a short note on what to check or do if that step doesn't go as expected. Don't invent failure modes that weren't part of the actual process described — only include ones that are real or highly likely given the process.

## Step 5: Close with scope and staleness

Note anything the runbook assumes will stay true (a specific tool version, an account, a config) that would make it go stale — this helps future-you or a teammate know when to double check before blindly following an old runbook rather than trusting it forever.

## Style rules

- Written for someone with less context than whoever is dictating the process — that's the whole point of a runbook over a one-off explanation.
- Concrete over abstract: real commands/paths/values, not paraphrased descriptions of them.
- Numbered, followable sequence — not prose that requires re-reading to extract the actual steps.
- Don't pad with generic caveats; only include warnings/failure notes tied to real, known failure points in this specific process.
