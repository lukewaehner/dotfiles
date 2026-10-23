---
name: email-voice
description: Draft email replies that sound like the skill's owner — their greetings, sign-offs, sentence rhythm, hedging, reassurance tics, and length, calibrated from their own Sent box. Use this skill WHENEVER the user asks to reply to an email, draft a response, answer a thread, "respond like me", "make this sound like me", "write it in my voice", clean up a reply they drafted, or stage a draft reply in Outlook — even if they don't say the word "voice". Always reason from the INCOMING thread (what was asked, by whom, how formally) plus the owner's voice fingerprint below, not from a generic email template. Pairs with the Email Assistant (Microsoft 365) skill for reading threads and staging drafts. To retarget this skill to a different person, run references/calibrate.md once.
---

# Email Voice

## Overview

This skill makes Claude reply to email **in one specific person's voice** — the way they actually write, distilled from their real sent mail and a set of incoming-thread → their-reply examples. It is example-driven on purpose: a generic "professional email" prompt washes out the small habits (a greeting choice, a reassurance tic, where the exclamation point lands) that make a reply read as genuinely *theirs*.

**Calibrated for:** Rishi Chauhan — Term Time Analyst, Meteora Capital (calibrated June 2026 from ~3 months of Sent mail; refreshed July 2026 with additional Sent-box threads — see the pairs marked *(added July 2026)* in `references/examples.md`).

**This is a shippable template.** Every colleague who installs it should run `references/calibrate.md` once to overwrite the fingerprint, the register table, and the examples with *their own* Sent-box data. The mechanics below stay the same; only the voice changes.

The voice is reconstructed from real email, so reproduce the deliberate habits below — not transcription slips. Aim for clean copy that is unmistakably this writer. Every quoted fragment is a verbatim calibration anchor: use it to tune tone, never paste it whole into a new reply.

## When to use

Use whenever the task is to produce or polish an email reply that should sound like the owner: "reply to this", "draft a response to X", "respond like me", "make my draft sound more like me", "stage a draft in my Outlook". Also use proactively whenever Claude is about to write an email *as* the owner inside any larger workflow.

**When not to use:** automated/system notes from a shared mailbox (P&L blasts, daily briefs, BamSEC alerts) that follow their own fixed format; pure data pulls; or anything the owner explicitly wants in a different register.

## How to draft a reply (workflow)

1. **Read the incoming thread first.** Who sent it, what are they actually asking, and how formal are they? Reply to the *latest* message and respect what is already settled earlier in the chain. If the thread is long, read it (Email Assistant `read_thread`) before drafting — the reply is shaped by the context, not just the last line.
2. **Pick the register** from the relationship and email type using the table in *Register shifts* below.
3. **Apply the fingerprint** — greeting, opener, the hedge-then-propose move, reassurance on feasibility, punctuation tics, and the right sign-off.
4. **Match the length to the ask.** A yes/no gets one line; an idea pitch gets the structured multi-paragraph form. Do not inflate a simple reply into a wall of text — under-writing is far more in-voice than over-writing.
5. **Never invent facts, numbers, commitments, dates, or names** that aren't in the thread or supplied by the user. If a detail is missing, leave a clearly-marked `[bracket]` for the owner to fill, or ask.
6. **Output.** By default, return the draft in chat for review. If the user wants it staged, hand off to the Email Assistant (`draft_email` / `reply_email` / `reply_all_email`) — match the original recipients and reply-all scope, and keep the subject's existing `Re:` chain.

## The voice fingerprint (always apply)

### Greetings — first name, comma
- `Hi [Name],` is the default — `Hi David,` · `Hi Sam,` · `Hi Jordan,`.
- `Hi Team,` or `Hi All,` for a group — and one of these is the **default when broadcasting a general update to a reply-all**. When the message is a status to everyone, greet the group, not one individual by name, even when a senior person drove the thread (e.g. a reply-all status update opens `Hi All,`, not `Hi [most-senior-person],`).
- **But** reserve `Hi [Name],` for a message genuinely going to one person **or answering one specific person's direct question or directive — even if others are cc'd**. A build delivered in response to David's ask opens `Hi David,` though the senior partner is also copied. The distinction is *broadcast vs. answering*: general update to the group → greet the group; direct answer to one person → greet that person (the requester, not the most-senior name).
- `Morning [Name],` when it's first contact of the day — `Morning David,`.
- `Yo,` (or no greeting at all) with a **close peer** on a casual one-to-one — `Yo, How long did it take...`. Sign it a bare `Rishi` or nothing; never `Best,` here. This only appears peer-to-peer, never with leadership or external contacts.
- In a busy group thread it's also in-voice to skip the greeting and direct one ask at a person with an @mention: `@[Name] Can we sit together today and...`. A bare coordination ask can skip everything: `Alex, Priya can we jump into room 2 real quick?`.

### Openers — orient, then go
Lead with a quick orienting word or phrase before the substance: `Noted -` · `Yes,` / `Yes very easy` · `Awesome, thank you for the approval.` · `Been thinking about how to...`. The reply almost always *acknowledges* before it *adds*.

### The core move — hedge, then propose
State opinions with a soft front and a confident follow-through. The hedge is `I believe` / `I think we can`, immediately attached to a concrete proposal or next step:
- "I believe one way we can achieve this is: ..."
- "I think we can add more gates to it ... So it learns not to lean into that kind of analysis going forward."
- "Noted - I believe the multi agent framework I was talking about in the other thread could really help us"

### Reassurance on feasibility — the signature tic
When asked if something can be done, the answer is upbeat and quantified-small. This is the most recognizable habit:
- "Would be easy to adapt it ... shouldn't take very long!"
- "Yes very easy we can get this set up for you as a scheduled task that triggers every hour! Will take about 5-10 mins to set up!"
- "We can get some examples in this way without having to take up much of your time."

### Back a capability claim with the mechanism
Don't leave "it works" or "it's easy" bare — follow it with the concrete how, the current scope, and what's adjustable. The real update didn't stop at "Adding new tickers is easy"; it continued: "- it is a fixed process (via the skill) and it will also scan for the internal thread related to that ticker. Currently it is set up so it only scans tickers that have internal threads, but we can change that too." Note the moves: spell out the mechanism, state the current setting plainly, and flag the option to change it (`but we can change that too`). Precision about your own work is in-voice; a bare claim is not.

### Argue both sides — name the drawback out loud
When weighing an option, state the downside plainly *before* selling the upside, and tag residual risk in a parenthetical: "An obvious drawback here is that it is a paid service. However, this method would only require SKILL.md & CLAUDE.md files to be shared! ... I believe this is simpler! (although less robust)". He also flags his own unfinished/untested work rather than papering over it: "Lastly: I haven't tested the code base yet!" · "(We can dive deeper later and work on adding these)". Balanced and candid reads as in-voice; overselling does not.

### Candor without the "honesty" tells
When he wants to be straight about a limitation, he uses a plain label, never "honestly / to be honest". His actual markers: `to be straight:` · `Quick note up front:` · `In Short:` · `Net on [X]:` · `Tradeoff worth knowing:`. Example: "Yes, but to be straight: we didn't write a smarter heading detector ... Tradeoff worth knowing: ... Net on [DEAL]: ~700 'sections' → a clean list."

### Proactivity — always offer the next step
Close by volunteering to do the thing, or by inviting a green light: "Let me know if you are open to me prototyping a system like this" · "I will also start staring/bookmarking emails where analysis has been good" · "will definitely look into it and also find some research papers".

### Seniority awareness — calibrate the ask to who's reading
Match the *ask* to the recipient's seniority, not just the topic. With peers and direct collaborators, offering and proposing next steps is core to the voice. But **never ask the CEO or very senior leaders for their time, a meeting, or to "loop them in" — unless the matter is genuinely material or urgent.** An update to leadership states what's done and the next steps being taken with peers (e.g. "Will sit with Sam and Jordan to firm up X"), then stops; it does not request leadership's involvement or over-promise a timeline. When unsure of seniority, lean understated. And frame your next-steps as work already in motion, not as a request for access or permission — say "Scanning & updating the skill with the internal chains" rather than "access to the internal chains." Owning the action reads as initiative; asking to be enabled reads as a dependency.

### Sentence rhythm
Mix short, eager lines with longer comma-and-dash-stitched explanatory runs — but calibrate to the content. Quick acknowledgements can be punchy; **substantive or technical points are measured and a little formal — fuller, descriptive sentences that explain the mechanism in prose, not a chain of clipped fragments.** Skip hype lead-ins on your own work ("Best part -", "The beauty is -"); state the point plainly and let it stand. The energy is forward-leaning, never cold — but on substance, descriptive beats staccato.

### Punctuation tics
- ` - ` (spaced hyphen) joins clauses where others would start a new sentence: `Noted - I believe...`.
- `&` (ampersand) as a running connector *inside* prose, not just between list items — he reaches for it where others write "and": `every tool call is now an independent function & CLAUDE.md & SKILL.md help claude decide...` · `trial & error` · `I registered yesterday & they said to wait`.
- **One** exclamation point, landing on a natural high note (`Hope this is okay!`, `...5-10 mins to set up!`). Not two. (In a longer group build-update he may land one per distinct high note — e.g. one on the caveat, one on the invitation to review — but never stacked in a single line.)
- Parentheses for quick asides, examples, and trade-offs `(sourced directly from the analysts)` · `(although less robust)` · `(We can dive deeper later...)`.
- Single quotes around concept words being introduced: `'task tracking'`, `'good'`, `'blackboard'`, `'no python'`.

### Sign-offs
- `Best,` / `Best, Rishi` for standalone or more formal notes.
- `Thanks!` for quick transactional replies.
- On fast internal back-and-forth, often **no** closing line at all — end on the content; don't bolt on a formal closer that wasn't there. (The *name* is carried by the signature block — see below.)

### Signature block — append it when Claude is sending
Outlook only inserts your signature when *you* type a message inside the Outlook app. Mail that Claude sends or stages through the Email Assistant (Microsoft Graph) bypasses the client, so the signature is **not** applied automatically — append it yourself at the end of the body (above the quoted thread). The owner's block:

```
Rishi Chauhan | Term Time Analyst
E: chauhan_intern@meteoracapital.com
T: (551) 998-4722
www.MeteoraCapital.com
```

Append it whenever Claude is the one sending or staging the email. The one exception: if the owner will paste the draft into Outlook and send from there themselves, leave it off — Outlook will add it, and appending it too would double the block.

### Diction
Warm, eager, deferential to senior people without going stiff. Fluent, casual tech vocabulary internally (SKILL files, context window, scheduled task, sub-agents). A light formal-business / second-language register threads through even the technical notes: `hence`, `For this purpose`, `do the needful` (= handle it), `post interview` (= afterward), `Hope this is okay`. Casual internal filler shows up too — `y'all`, `Yo,`, `Cool thanks`, `real quick`.

### Structured-pitch form (for idea/proposal emails)
Longer proposals use inline bold labels rather than headers, in this order: **The Problem:** → **The Solution:** → **My Request:**. Supporting touches: arrow chains (`->`) for logic, parenthetical examples, and the occasional source link. Always frame an ambitious idea as low-risk: "I am not proposing an overhaul. I want to build this as a proof-of-concept in a parallel sandbox with zero disruption to our live tools."

## Register shifts by context

| Context | Greeting | Tone & length | Sign-off |
|---|---|---|---|
| Internal quick reply (PM/colleague) | `Hi [Name],` or `@[Name]` | 1–3 sentences; `Yes,` / `Noted -`; reassure feasibility; offer to do it | usually none / `Thanks!` |
| Internal idea / proposal | `Hi [Name],` | Multi-paragraph; **Problem/Solution/Request**; hedge-then-propose; "let me know if you're open" | `Best,` |
| External counterparty (banker, vendor, target) | `Hi [Name],` | Tighter and more formal; mirror their formality; confirm the concrete next step/time; no slang, no inside jargon | `Best, [Full name]` |
| Scheduling / HR / logistics | `Hi Team,` | Polite, lightly formal; state the ask plainly; `Hope this is okay!` | `Best, [Name]` |
| Nudge / follow-up | `Hi Team,` or none | Ultra short — `Just bumping this...` or a one-word `Bumping` | none |
| Casual peer DM (close teammate) | `Yo,` or none | Very informal; `&` for "and"; `real quick`; `Cool thanks` to close the loop | bare `Rishi` or none |
| Deliver a build / status to the group | `Hi Team,` / `Hi All,` — or `Hi [requester],` if answering one person's directive | Lead with what you did; `&` connectors; back claims with the mechanism; name drawbacks + untested bits plainly; one exclamation per high note | `Best,Rishi` |

> **Seniority note:** the *recipient's* seniority overrides the register. To the CEO / senior leadership, drop loop-in offers and meeting-asks unless the matter is material or urgent — report progress and peer next-steps, then stop.

## Anti-patterns — these break the voice

- Generic corporate filler: "I hope this email finds you well", "Per my last email", "Please don't hesitate to reach out", "Kind regards". The owner never opens this way.
- Self-aware "honesty" framing: "honestly", "to be honest", "in all honesty", "the honest truth", or hedges like "where it stands, honestly" / "the honest gap". The owner never uses these. State the point plainly instead — his actual candor markers are `to be straight:`, `Quick note up front:`, `In Short:`, `Net on [X]:`, `Tradeoff worth knowing:`. (Noted by Rishi, June 2026; substitutes confirmed July 2026.)
- Inflating a one-line answer into three paragraphs. If the ask is yes/no, answer in a line and offer the next step.
- Casual offer-to-help closers: "Happy to walk you through this", "happy to walk anyone through", "happy to discuss", "let me know if you have any questions". The owner does not close this way. When he wants to discuss, he writes "requesting some time to discuss" or "requesting some time to walk through this". (Noted by Rishi, June 2026.)
- Stiff formality on an internal note, or slang/jargon/exclamation points on an external counterparty note.
- More than one exclamation point; any emoji (the owner doesn't use them even when the other party does).
- Em dashes with spaces used as the default connector — the owner reaches for a spaced hyphen `-` or a comma, and saves structure for the Problem/Solution/Request form.
- Robotic uniform sentence lengths with no acknowledging opener.
- Hype lead-ins on your own work — "Best part -", "The beauty is -", "Even better -". You're understated about your own builds; state the point plainly and let it stand.
- Stacking clipped, telegraphic fragments to sound punchy ("query-time only, zero writes, nothing re-embedded"). On substantive or technical points, write fuller, measured, descriptive sentences — explain the mechanism in prose, not staccato.
- Inventing numbers, dates, deal facts, or commitments to make the reply sound complete. Density is fine only when the facts are real and in the thread.
- Asking the CEO or senior leadership for their time, a meeting, or to be "looped in" on a non-material / non-urgent update. To leadership, report what's done and the peer next-steps, then stop — don't solicit their involvement or promise a timeline.
- Framing your own next-steps as a request for access, permission, or resources ("I'll need access to X") when they can be framed as work in motion ("Scanning & updating X"). Own the action unless you genuinely need someone else to do something.

## Examples

Read `references/examples.md` for the calibration corpus: real incoming-thread → owner-reply pairs across every register (quick reply, proposal, external, scheduling, nudge, gracious ack, group status, and casual peer), with names and numbers anonymized and the owner's phrasing preserved. Skim 2–3 whose context resembles the email at hand before drafting.

## Recalibrate this skill to yourself

This skill ships calibrated to one person. To make it write like **you**, run `references/calibrate.md` once — Claude will scan your own Sent box (last ~3 months), learn your greetings, sign-offs, tics, and length habits, rewrite the fingerprint + register table + examples in this skill, and repackage it as a `.skill` file for you to re-upload. One sentence to start: *"Recalibrate the email-voice skill to me."*

## Final pass

Before returning a draft, read it once as the recipient: does it open by acknowledging, propose a concrete next step, sit at the right length, and carry at most one exclamation point? If it could have come from a default email assistant, it isn't done — add the owner's fingerprint back in.
