---
name: postmortem-writer
description: >
  Write a structured incident postmortem — timeline, root cause, blast radius, remediation, and follow-ups — from a description of what happened. Use ONLY when explicitly invoked — the user names this skill directly, types "/postmortem-writer", or says something like "use the postmortem-writer skill." Do NOT trigger on plain "write up what happened" or "summarize this incident" requests — those get a normal answer. Works from a freeform account of the incident, logs/error messages pasted in, or a mix of both.
---

# Postmortem Writer

Turns an incident — an outage, a bug that caused real impact, a failed deploy, a data issue — into a structured, consistent postmortem. The goal is a document that's fast to write, easy to scan, and comparable to other postmortems over time, not a fresh freeform narrative each time.

Output format depends on length/context: a minor incident can stay a chat response; anything that will actually be shared, filed, or referenced later (most real incidents) is a better fit for a saved markdown file.

## Step 1: Gather what's known

Work from whatever the user provides — a freeform account, pasted logs/error messages/alerts, timestamps, Slack/chat excerpts, or a mix. Don't invent details that weren't given: an unknown root cause or an unclear timeline gap should be marked as unknown/TBD in the document, not filled in with a plausible-sounding guess.

If something critical is missing (there's no timeline at all, or the actual impact is unstated), ask — but keep it targeted to what's actually needed to write the document, not a full incident-review interview.

## Step 2: Structure the postmortem

Use this structure, adapting section presence to what's actually known (an incident with no clear root cause yet should say so plainly rather than forcing a fabricated one):

### Summary
2-4 sentences: what happened, what was affected, how it was resolved, at a glance. This is the part a busy reader skims first — it should stand alone.

### Impact
Concretely what was affected: which systems/users/data, how long, any quantifiable impact (requests failed, data affected, revenue/time cost) if known. State "unknown" rather than guessing if it wasn't provided.

### Timeline
Chronological, timestamped where possible: when the issue started, when it was detected, key actions taken, when it was resolved. This is often the most valuable part of a postmortem for future reference — keep it factual and sequential, not narrated.

### Root cause
What actually caused it, at the right level of depth — the proximate trigger and, where known, the underlying condition that made it possible (not just "a bug" but what about the system allowed that bug to cause this impact). If root cause isn't fully known yet, say so explicitly and note what's still being investigated rather than presenting a guess as settled.

### Remediation
What was done to resolve the immediate incident (distinct from long-term fixes below).

### Follow-ups / action items
Concrete, ideally assignable items to prevent recurrence or reduce impact next time — monitoring gaps to close, tests to add, process changes, tech debt to address. Only include items that are real next steps, not generic "improve monitoring" filler unless the incident specifically pointed at that gap.

## Step 3: Keep the tone incident-report, not narrative

- Factual and neutral — this documents what happened, not who's to blame. Avoid language that assigns fault to a person; focus on what in the system or process allowed the failure.
- Timestamps and specifics over vague language ("the service was degraded for approximately 40 minutes" beats "the service was down for a while").
- Don't editorialize about severity beyond what the impact section already establishes — let the facts carry the weight.

## Style rules

- Every section should be scannable on its own — a reader should be able to jump straight to "Timeline" or "Follow-ups" without reading the whole document.
- Mark unknowns explicitly rather than smoothing over gaps in what's known.
- Keep follow-up items concrete and specific to this incident, not a generic best-practices checklist.
