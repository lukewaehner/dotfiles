---
name: "transcript-principles"
description: "Distill Meteora's daily PM/EOD trading-desk transcript into the live SPAC-only TRANSCRIPT-PRINCIPLES memory doc, which is organised as six governing chains of reasoning rather than a list of rules. Trigger on \"run the transcript principles\", \"update the brain\", \"process today's transcript\", \"transcript principles\", or the daily 7:30pm run. Tests each observation against the existing chains and sharpens them; never adds a bullet per anecdote. Silent — writes only the memory doc."
---

# Transcript → Principles (the desk "brain")

## What this is
Every trading day the desk records a call where analysts talk through the tape off the blotter.
This skill turns that raw, noisy transcript into the **generalized reasoning** behind our SPAC views
and maintains it in the live `TRANSCRIPT-PRINCIPLES` memory doc. It is a backbone other skills read,
**not** a daily email.

### The point of the whole exercise
**Give the analyst enough of a *tell* to judge whether a name is worth investing in — or worth
walking away from.** A contribution earns its place only if it sharpens how you'd approach the next
analogous SPAC.

### The doc is chains, not a rule list — this is the most important thing about this skill
As of 8.5.26 the brain is **six governing chains of reasoning**. Each chain is a line of thought
that generates its own conclusions; the tells beneath it are that reasoning already applied, kept
because they are fast. The chains are the unit of maintenance.

1. **A SPAC is a bond stapled to an option. Price them separately.**
2. **The carry is a fraction, and every error lives in the denominator** (the date you assumed and
   the cash you trusted).
3. **Validation means an independent party with money at risk. Everything else is a claim.**
4. **A deal closes when the binding gate clears — and it is rarely the one in the press release.**
5. **Your position is denominated in days of volume, not dollars.**
6. **Separate what you know from what the market knows, and know which of your reasons is still true.**

This structure replaced a 118-principle, example-per-rule version that had grown to ~70 pages and
became an index rather than a brain. **Do not rebuild that.** The failure mode this skill now exists
to prevent is appending a fresh bullet, with a fresh anecdote, every single day.

### Advise, don't instruct
You cannot see current position and basis, risk limits and mandate, available liquidity and borrow,
what else competes for the capital, or the PM's read of the moment. A prescribed trade will often be
wrong *even when the analysis is right*. Numbers from the desk go in as ***reference points***
("~5% ref.") — calibration, never thresholds to trade to. If you catch yourself specifying a price,
size or timing, convert it into the consideration behind it.

### Scope: SPAC-only
General merger-arb, credit and macro reasoning was retired from this doc on 8.5.26 and is **not**
maintained here. There is **no** merger-arb principles doc and one is not to be created. When a
transcript produces a good observation about the WBD / MKTX-ICE / ATKR / SMTI class of name, note it
in the dated Entry and move on — do not add it to the summary.

---

## CONFIG
```
DOC_NAME          = TRANSCRIPT-PRINCIPLES        # LIVE memory doc
DOC_PATH          = G:\Shared drives\Interns\Master Docs\TRANSCRIPT-PRINCIPLES.docx
BLOTTER_PATH      = G:\Shared drives\GPT\Blotter\blotter_report_v2.xlsx
SENDER_ALLOWLIST  = *@meteoracapital.com   (seen: APuskorius, lgries, vik, jdavis)
SUBJECT_MATCH     = subject contains "transcript" (case-insensitive) AND a date for today
SUMMARY_CEILING   = 30,000 characters (hard limit; the doc sits ~21,000 — protect the headroom)
VDB               = DO NOT WRITE (existing pipeline owns ingestion)
TEAM_EMAIL        = DO NOT SEND (silent)
```
**Memory-doc MCP tools:** `read-memory-doc` (summary_only=true) to load the chains ·
`patch-memory-summary` for targeted edits (strongly preferred) · `update-memory-summary` only for a
genuine restructure · `update-memory-doc` (tag `call-notes`) to append the dated Entry.

The **Executive Summary is the living brain** (chains + tells + walk-away screen); the **Entries are
the audit trail** (one per transcript, carrying the example-level anchors). Keep that split — anchors
and blotter detail belong in the Entry, not in the summary. That separation is what keeps the summary
from re-bloating.

---

## Procedure

### Step 1 — Get today's transcript
**The desk often sends a morning file first and the complete full-day file later as a REPLY on the
same subject, both named `transcript.txt`. Taking the first one silently discards the afternoon —
including the EOD blotter walk-through, the densest part of the day.**

1. Search the mailbox for `subject: transcript`, newest first, `after:` today. Formats vary — accept
   all (`8.4.26 AM + PM Transcript`, `July 9, 2026 -- EOD Transcript`, `7/16/2026 - EOD transcript`,
   `7.20.26 Morning Transcript`). Match on "transcript" + today's date from an allowlisted sender.
2. **Enumerate the whole thread including `Re:`/`Fwd:` replies**, and call `list_attachments` on
   every matching message — not just the original, not just the newest.
3. Build a candidate table before downloading: message · send time · filename · size. Identical
   filenames with different sizes are different transcripts.
4. Download each distinct candidate to its **own folder** (they share a filename) and measure what it
   covers: first timestamp, last timestamp, line count.
5. **Select on coverage, not arrival order** — widest first→last span. If two overlap only partially,
   process the union.
6. Classify AM vs PM from the transcript's own timestamps, not the subject line. The 7:30pm run
   targets PM/EOD or full-day. If only an AM transcript genuinely exists, run principles-only (skip
   the same-day blotter tie-out) and say in the Entry that you checked the replies.
7. If no attachment exists anywhere on the thread, use the email body. Record in the Entry which file
   you used and what the rejected candidates covered.

### Step 2 — Load the current brain, and check for duplicates
`read-memory-doc` with `summary_only=true`. **Read the six chains before extracting anything** — the
whole method depends on knowing what reasoning already exists. Scan recent entries: if this exact
transcript (date + AM/PM) is already logged, **stop**.

*Exception:* a re-run that widens coverage is not a duplicate. If today is logged as AM/partial and
you now have a fuller file, process the uncovered portion and append a `correction`-tagged Entry.

### Step 3 — Load and verify the blotter (PM/full-day only)
1. `get_file_info` on `BLOTTER_PATH`. **Verify `modified` is today** — if stale, say so loudly and
   proceed with reduced confidence.
2. Read **New Fills** (today's executions), **New Orders** (working), **Current Markets** (CIT, C−T,
   stage, deal, deadline).
3. Build a decode map `ticker → {stage, CIT, C−T, price, fills, volume, bucket, deal, deadline}` to
   resolve garbled tickers and "X cents over trust" talk. What the blotter shows is **observed fact**,
   not a recommendation.
   > *Stale-blotter fallback:* the afternoon session is often the PM reading the blotter line by line.
   > Decode from that walk-through instead and label it spoken-on-the-call rather than file-verified;
   > machine-transcribed levels are frequently garbled, so record them as directional.

### Step 4 — Condense
Strip timestamps and one-word backchannel, merge consecutive same-speaker lines. Then **confirm the
last block you read corresponds to the last timestamp in the raw file** — the condenser merges
aggressively, so a small block count is not evidence of a short session.

### Step 5 — Route every observation through the chains
Walk the condensed transcript for each place someone expresses a view, decision or piece of
reasoning. Prioritize **Vik Mittal** (PM/founder, highest signal and decisive); Aidas Puskorius,
Luke Gries, Alex Piskunov are the analysts.

For each candidate, in this order:

1. **Decision test.** Would an analyst approach the next analogous SPAC differently knowing this? If
   no, drop it. Describing the day is not the job.
2. **Scope test.** Is it about a SPAC? If it's general merger arb, credit or macro, it goes in the
   Entry only — never the summary.
3. **Chain test — the important one.** Which of the six chains is this an instance of? Almost
   everything is an instance of one; that is what it means for the doc to be organised by reasoning.
   Ask *why* the desk reached that conclusion, not just what the conclusion was, and follow it back
   to the governing idea.
4. **Then choose the smallest sufficient change** (see Step 6).

**Resist the anecdote reflex.** A new ticker exhibiting a pattern already in the doc is a
reinforcement, not a new principle. The question is never "is this interesting" — it is "does the
brain reason differently now."

Tag anything you add with its regime(s): **IPO** new issue · **PRE** pre-deal · **ANN** in-deal ·
**DESPAC** post-close · **WIND** winding down/OTC · **ALL**. Map from the blotter: Pre-Deal → IPO if
it IPO'd within ~1 month, else PRE; In-Deal → ANN; DeSpac → DESPAC; any name near max deadline,
paying extensions, or heading to the OTC → WIND regardless of the sheet label.

### Step 6 — Make the smallest sufficient change
In descending order of preference. Use `patch-memory-summary`:

- **SHARPEN (most common).** The day restated reasoning already present. Improve the wording of an
  existing tell, or fold in a better reference point. No new bullet. This is the default and on many
  days it is the entire output.
- **EXTEND.** Genuinely new consequence of an existing chain → add **one** tell under that chain,
  ≤2 lines, with its regime tag and `[ID]`. Keep IDs stable; never renumber.
- **DEEPEN THE CHAIN.** The day exposed something about the *reasoning itself* — a case the chain's
  narrative doesn't cover, or a sharper way to state why it holds. Edit the chain paragraph. This is
  high-value and under-used; prefer it to adding a tell where both would work.
- **MERGE / RETIRE.** Two tells are saying one thing, or something is contradicted or obsolete →
  merge into the better version, or move it to a Retired note with a one-line reason and date. Never
  silently delete. Retiring is a legitimate and encouraged output of a run.
- **NEW CHAIN (rare).** Only a genuinely new line of reasoning — not a new fact pattern — earns a
  seventh chain. Expect this roughly never. If you're reaching for it, you probably have an EXTEND.

Also update the **fast walk-away screen** if the day produced a new disqualifying tell.

**Guard the ceiling.** The summary caps at 30,000 characters and currently sits ~21,000. If a run
would push it past ~28,000, do not trim the chains — merge or retire tells until it fits. The chains
are the asset; the tells are expendable.

### Step 7 — Append the dated Entry, then stop
`update-memory-doc` (tag `call-notes`) with:
- **The ticker decode** — for each name: the tell, the desk's read, what the blotter shows, and the
  regime. This is where example-level detail and anchors live.
- **Which chain each observation routed to**, and the change made (sharpened / extended / deepened /
  merged / retired / none).
- Anything dropped as non-SPAC, so it is recoverable.
- Open questions.
- Which transcript file was used, what it covered, what the rejected candidates covered.

**Do not** email anyone. **Do not** write to the VDB. Scrub anything personal, comp or legal.

---

## Guardrails
- **Chains first.** Read the existing reasoning before extracting. A run that adds bullets without
  having checked which chain they belong to is the failure this structure exists to prevent.
- **Most days should change little.** A day that sharpens one tell and retires another is a good day.
  Do not manufacture novelty; the brain refines, it does not accumulate.
- **Anchors live in Entries, not the summary.** Ticker/date/speaker detail in the summary is what
  bloated the old version.
- **SPAC-only. No merger-arb doc.**
- **Take the widest transcript, not the first one.**
- **Faithful, not inventive.** Every tell must trace to something actually said. You may generalize
  and connect — that is the point of the chains — but never fabricate a view the desk doesn't hold.
  Where you're synthesizing across sessions rather than reporting one, say so in the Entry.
- **Ground in the blotter** — from the file when current, from the PM's walk-through when not.
- **Correct in the open.** A pass that missed material gets a `correction` Entry, not a rewrite.
- **Silent + read-mostly.** Reads email, blotter and memory docs; writes only `DOC_NAME`.

## Output
The updated live `TRANSCRIPT-PRINCIPLES` doc. For a scheduled run, one line is enough:
`processed <date> <AM/PM/FULL DAY>: N sharpened / M extended / K chains deepened / L retired.`
Flag it in that line if the blotter was stale, if a fuller transcript superseded an earlier pass, or
if the summary is approaching the character ceiling.

