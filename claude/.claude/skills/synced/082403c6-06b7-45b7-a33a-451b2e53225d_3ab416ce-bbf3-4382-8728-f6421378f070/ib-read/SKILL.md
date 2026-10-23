---
name: ib-read
description: >-
  End-of-day capture of Bloomberg Instant Bloomberg (IB) chat boxes into per-deal
  Markdown transcripts, then filed into the matching Claude Project folders. Use this
  skill whenever the user wants to read, archive, export, back up, or "download the IB
  boxes", capture the deal/SAFT chat rooms, run the EOD IB sweep, or turn today's IB
  Manager conversations into .md files for the project folders - even if they don't say
  the skill name. Trigger on "run ib-read", "read the IB boxes", "export the IB chats",
  "EOD IB capture", "grab today's IB rooms", "save the Bloomberg chats to the projects",
  or any request to pull Instant Bloomberg conversations out of the terminal into files.
  This skill assumes a Bloomberg Anywhere web session that is ALREADY logged in inside a
  Claude-in-Chrome-controlled browser tab, with the IB Manager open. It reads the live
  session visually (the terminal is a Citrix pixel-stream, not a webpage) and never sends
  IB messages - it is read-and-file only.
compatibility: >-
  Requires the Claude-in-Chrome extension (mcp__claude-in-chrome__*) attached to the tab
  running the Bloomberg Anywhere web session. Optionally uses a Claude Project / mounted
  project directory connector for filing. Does not require any Bloomberg API.
---

# ib-read - EOD Instant Bloomberg capture -> per-deal Markdown -> Claude Projects

## What this skill does and why it works this way

At end of day, walk every chat box in the Bloomberg **IB Manager**, capture **today's**
messages from each, write one clean Markdown transcript per deal, and file each transcript
into its matching **Claude Project** folder.

Three facts about the environment drive every design choice below. Understanding them keeps
you from fighting the tool:

1. **Bloomberg Anywhere web is a Citrix pixel-stream, not a webpage.** There is no DOM text
   to scrape - `read_page` / `get_page_text` return nothing useful. Everything is read
   **visually from screenshots**. So capture is screen-by-screen, and you (the model) read
   the text off each screenshot with vision.
2. **The Claude-in-Chrome extension can only drive a tab it controls.** It cannot read or
   scroll a Bloomberg tab the user opened independently. The session must already be running
   in the extension-controlled tab (see Prerequisites). If it isn't, stop and tell the user
   rather than guessing.
3. **This is read-only by policy and by intent.** Never type into the IB message box, never
   click Send IB, never place an order. You are exporting conversations, nothing else.

## Prerequisites (the operator must do these BEFORE invoking)

Do not attempt to work around a missing prerequisite - if any is unmet, report exactly which
one and stop.

1. **Chrome is open with the Claude-in-Chrome extension installed and signed in.**
2. **The Bloomberg Anywhere session is logged in inside the extension-controlled tab.**
   The B-Unit login cannot be automated, so a human does it: let the extension open a tab,
   navigate it to `bba.bloomberg.net`, and complete Terminal username + password + B-Unit
   **in that tab**, so the Citrix session streams into the tab the extension controls (not a
   separate window). Logging in on a tab you opened yourself will NOT work - the extension
   can't see it.
3. **The IB Manager is open and visible** (`IB <GO>`), with the left-rail **chat list**
   showing and the IB window maximized / large enough that message text renders legibly.
4. **The box -> Claude Project mapping is available** - see `references/box-project-map.md`.
   Edit it so each IB box routes to the right project. Any unmapped box still gets a
   transcript; it just lands in the `_unmapped` bucket for manual filing.

## Step-by-step workflow

### 1. Attach and confirm the session

- Call `mcp__claude-in-chrome__tabs_context_mcp` to find the tab; if multiple browsers are
  connected, ask the user which one is the session tab, then `select_browser` /
  `switch_browser` as needed.
- Take a screenshot (`computer` action `screenshot`). Confirm you can see the IB Manager and
  the chat list. If you instead see a login page, a blank tab, or a launch error
  ("Failed to retrieve ICA"), the session is not in this tab - stop and tell the user to
  complete prerequisite 2.
- Note today's date from the environment; you will date-gate against it.

### 2. Enumerate the chat boxes

- Read the left-rail chat list from the screenshot. Record each box's **display label** and
  its on-screen click coordinates.
- If the list is longer than the visible pane, scroll the **list** (not a chat) to the bottom
  and collect the rest, then scroll back to the top. Build the full ordered list before you
  start capturing, so you have a stable checklist.
- Titles are often truncated ("SAFT (Safety Insur..."). Match on the leading, stable part of
  the label against the mapping file; don't rely on the truncated tail.

### 3. Capture each box - today only

For each box in the list, in order:

1. **Open it**: `left_click` the box in the left rail. Screenshot to confirm the header shows
   that box's title.
2. **Find the start of today.** Scroll the **message pane** up (scroll wheel over the messages
   area) until you either (a) hit a date separator / a message clearly dated before today, or
   (b) reach the very top of the room. Bloomberg shows a date header when the day rolls over;
   the first message *after* the most recent prior-day marker is your "start of today". If the
   whole room is from today, the top of the room is the start.
3. **Read forward to newest.** Scroll down roughly one pane at a time. After each scroll, take
   a screenshot and read every visible message: **sender, timestamp, and full text** (including
   @mentions and wrapped multi-line messages). Keep going until the newest message is on screen
   and the pane won't advance further.
4. **De-duplicate across overlapping screenshots.** Consecutive screenshots overlap on purpose
   (so nothing is skipped). Track the last message you already recorded (sender + timestamp +
   first few words) and only append messages that come after it. Never emit the same message
   twice.
5. **Date-gate.** Keep only messages timestamped **today**. Drop anything from a prior day that
   was visible at the top. If a message's day is ambiguous (bare `HH:MM:SS` with no date and no
   nearby date header), treat it as today only if it falls after the start-of-today boundary you
   established in step 2.

Capture accuracy matters more than speed - a slightly slower, overlapping scroll that misses
nothing beats a fast scroll that drops a message. If a box has no messages today, record it as
empty (it still counts as processed).

### 4. Build the Markdown transcript

Write one file per box using this exact structure:

```
# <Box display title>
**Date:** <YYYY-MM-DD>
**Captured:** <YYYY-MM-DD HH:MM local, timezone>
**Messages (today):** <N>

---

**<SENDER NAME>** - <HH:MM:SS>
<message text, verbatim, multi-line preserved>

**<SENDER NAME>** - <HH:MM:SS>
<message text>
```

Rules that keep the files trustworthy:
- **Verbatim.** Do not paraphrase, summarize, correct, or reorder. Preserve @mentions, tickers,
  numbers, and typos as shown.
- If a sender label repeats for consecutive messages, still label each message - it makes the
  file greppable.
- If any text was unreadable in the stream (glare, truncation), mark it inline as
  `[illegible]` rather than guessing.
- Empty room today -> keep the header block with `**Messages (today):** 0` and no message body.

Filename: `<SLUG>_<YYYY-MM-DD>.md`, where `<SLUG>` is the mapping's slug for that box (e.g.
`SAFT_2026-07-24.md`).

### 5. File into the matching Claude Project folder

Resolve each box to a destination using `references/box-project-map.md`. Then file it using
whatever the destination Claude actually exposes, in this order of preference:

1. **Mounted project directory** - if a project/working folder is connected (e.g. via
   `request_cowork_directory` or an already-mounted path), write the `.md` into that project's
   folder.
2. **Project/file connector** - if a Drive-style or project file tool is available for that
   project, upload the `.md` there.
3. **Fallback (always works):** write everything under
   `outputs/ib-read/<YYYY-MM-DD>/<PROJECT>/<SLUG>_<DATE>.md`, plus an `_unmapped/` folder for
   boxes with no mapping, and then present the files grouped by project so a human drops each
   group into the right Claude Project.

Because "add a file to a Claude Project" is not a guaranteed automatable action across
environments, **always** produce the fallback folder tree even when a connector is available -
it is the shippable artifact and the audit trail.

### 6. Produce a run summary

End with a short index (also saved as `outputs/ib-read/<DATE>/INDEX.md`):

- One row per box: title -> slug -> message count today -> destination (project or `_unmapped`)
  -> status (filed / fallback-only / empty / error).
- Call out anything that needs a human: unmapped boxes, boxes that errored, or rooms where the
  top-of-day boundary was uncertain.

## Box -> Project mapping

The routing table lives in `references/box-project-map.md`. Keep it versioned alongside the
skill so a shipped copy carries sensible defaults. Editing it is the main way the operator
customizes the run.

## Edge cases and guardrails

- **Wrong tab / not logged in:** stop and report; never try to log in on the user's behalf.
- **Session drops mid-run (Citrix disconnect, ICA error):** stop, report which boxes were done,
  and ask the user to re-establish the session before resuming.
- **List changes between runs:** always re-enumerate the list at the start of each run; don't
  cache box coordinates across days - the terminal layout and list order move.
- **Long rooms:** it's fine to scroll many times; prioritize completeness. If a room is
  enormous and clearly all prior-day at the top, you don't need to read pre-today history -
  just establish the today-boundary and capture forward.
- **Never send:** if the user asks you to reply in a box, that is out of scope for this skill -
  it is capture-and-file only. Surface the request; don't act on it.
