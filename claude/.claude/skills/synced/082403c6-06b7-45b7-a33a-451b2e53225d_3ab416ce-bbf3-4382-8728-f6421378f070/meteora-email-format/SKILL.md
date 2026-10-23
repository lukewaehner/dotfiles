---
name: meteora-email-format
description: "House HTML format for internal Meteora email on SPAC names. Invoked explicitly by the user — never applied automatically, and it never overrides a format another skill already produces. DEFAULT mode renders exactly what the user asked for, in house format, at the TOP of the note. ENHANCED mode keeps that on top and adds the SPAC Snapshot table plus supporting detail BELOW it, on request: 'enhanced', 'full note', 'add the table', 'more detail'. Internal chains only — every recipient must be @meteoracapital.com. Keeps the Cowork-generated stamp when Claude wrote the bulk of the body; drops it when the user typed the body themselves. Renders content VERBATIM and in full unless asked to shorten."
---

# Meteora internal email format

One house format for internal SPAC email, so every thread reads the same way and
the desk can scan a note without re-learning its layout.

## What this skill is

**The user calls it explicitly.** It does not fire on its own, and it is not a
layer other skills pass through. A skill that builds its own email keeps its own
format — this one is never used to rewrap someone else's finished body.

**SPAC names only, for now.** Non-SPAC threads are out of scope; say so rather
than improvising a variant.

**Internal chains only.** Every recipient — To, Cc, Bcc — must be
`@meteoracapital.com`. The footer says *"for internal discussion only"*, so an
outbound note in this format states something untrue about itself. Check the
real recipient list before rendering; if anything is external, say the format is
internal-only and offer plain prose.

## The ordering rule — what was asked for goes on top

**What the user asked for is the note.** It goes at the top, in full, formatted.
Everything else is support and sits below it.

This holds in both modes and it is the rule that matters most. A reader opening
the note sees the thing they wanted first — not context, not a table, not
background. If the requested content has been pushed below anything, the note is
wrong however good it looks.

## The two modes

### Default

The requested content, in house format. Header, the content, footer. That's it.

No table, no rail, nothing appended. Most notes are this, and should stay this:
the format's value is that a short note looks short.

### Enhanced — on request only

Everything default has, unchanged and still on top, **plus**, below it:

1. `references/background-rail.html` — supporting detail and catch-up material,
   when there is genuinely some.
2. `references/snapshot-table.html` — the SPAC Snapshot, appended last.

Fires on an explicit ask: "enhanced", "full note", "add the table", "more
detail", "the long version". Never automatic.

Enhancement never displaces or rewrites the requested content — it is added
underneath it.

## Verbatim by default — do not condense

**Render the text you were given, in full.** Summarising, tightening, or
"improving" the prose is editing, and editing is deciding what the message says.

If asked to send an executive summary, send the executive summary — all of it,
as written — not a digest of it. Length is not a reason to cut. A long note that
renders correctly is a success; a short one that dropped three quarters of the
source is a failure, even when everything it kept is accurate.

**Condense only when asked** — "keep it short", "summarise", "just the
highlights". Absent those words, verbatim.

Never cut silently. The reader cannot tell a note that was short from one that
was shortened, so a silent trim reads as the whole truth. If it genuinely needs
cutting and nobody asked, say so and let the sender decide.

This has already gone wrong. A memory-doc summary of ~1,100 words was rendered
as ~500, dropping the provenance note, the Street Map and most of the open
questions. Every surviving figure was verbatim and it read well — which is
exactly why nobody would have caught it.

## The provenance stamp

The `Cowork generated` stamp is the first line, and it turns on **who wrote the
body** — not who clicks send, and not whose mailbox it leaves from:

| Who composed the bulk of the body | Stamp |
|---|---|
| Claude wrote it | **keep it** |
| The user typed it and Claude only rendered it | **delete the div entirely** |

Sending from the user's own account, at their instruction, does not make a note
human-written — that describes nearly every note this skill renders. Mixed notes
go by bulk; a true 50/50 gets the stamp. Never reword it: a stamp that varies
stops reading as a stamp.

## How to build a note

**1. Read `references/shell.html` immediately before writing any HTML.** Not
earlier in the session — as the first action of the render step. Copy its markup
out of that fresh read, then fill the `{{PLACEHOLDER}}`s.

A model's memory of a document's *structure* degrades into a plausible paraphrase
long before it forgets the document exists, and a paraphrase of a pixel-precise
template is exactly wrong. This has produced a silent rendering fork before: the
rail flattened to a shaded box, the Snapshot lost rows, and every fact in the
notes was still correct. Nobody caught it until a human read the sent mail.

**2. Put the requested content in, in full.** Every `{{...}}` is replaced or its
element deleted — never ship a `{{`. Add headings and lists as the source needs;
the template stretches. Mirror the source's own structure rather than flattening
it into prose.

**3. Enhanced only: append the rail, then the Snapshot**, each copied from its
own fresh read, before the footer.

**4. Validate.**

```bash
python3 scripts/validate_html.py note.html --mode enhanced
```

**5. Check the three things the script cannot see:**

- The requested content is on top, and complete.
- The stamp matches who wrote the body.
- Every recipient is inside `meteoracapital.com`.

## Hard rules

**Inline styles only.** No `<style>` block, no classes, no flexbox, no grid.
Outlook desktop renders with Word's engine and strips all of it. Tables for
layout, with `width="100%" cellpadding="0" cellspacing="0"`.

**Emit the new block only.** Never touch the quoted chain below your note — the
`<hr>` and `divRplyFwdMsg` history belong to Outlook.

**Reply into the existing thread.** Never fork the subject. Note that reply-all
resolves to no recipients on a message the signed-in user sent; use a plain
reply there, which still reaches the original recipients.

**Missing data is stated, not omitted.** `n/a — Bloomberg cannot resolve this
ticker`. `not retrieved this run`. A blank cell reads as zero. Never invent a
figure to fill a slot, and where two internal records disagree, print both and
name the conflict rather than silently picking one.

**Red is rationed.** `#c0392b` marks a fact that needs attention — nothing else.
Use it for emphasis and the desk stops seeing it. The palette in
`references/style-tokens.md` is closed; the validator fails an off-palette hex.

**No collapsible sections.** `<details>`/`<summary>` renders permanently *open*
in Outlook desktop, and the checkbox-accordion hack fails for the same reason.
The anchor-jump illusion works but costs a full copy per state (~84KB before the
note is even quoted). All three were built, tested and removed. The hierarchy is
visual — size, colour, indent — not interactive.

## Files

| File | Role |
|---|---|
| `references/shell.html` | The note itself, both modes |
| `references/background-rail.html` | Supporting detail, enhanced only |
| `references/snapshot-table.html` | SPAC Snapshot, enhanced only |
| `references/style-tokens.md` | Palette and type scale, canonical |
| `scripts/validate_html.py` | Pre-send gate |

`snapshot-table.html` and the rail are lifted **verbatim** from
`spac-filing-digest/references/email_template.html`, which stays canonical. When
it changes, re-lift these; never edit the copies in place. Two skills quietly
maintaining two versions of the same markup is how a fork starts.
