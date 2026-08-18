# Test mode, live mode & the dedup state file

Backs the TEST MODE block and Steps 6, 11, 12.

## The confirm gate = the safety net

The Email Assistant connector is built so a write tool only sends when called with
`confirmed=True`:

- `draft_email(...)` returns an *ephemeral preview only* — it does NOT persist a Draft in
  Outlook (verified in testing). It's fine for previewing, but to give a human something to
  open, you must actually send (to self in test mode).
- `reply_all_email(message_id, body)` **without** `confirmed` returns a *preview* (the exact
  computed recipients + the body) and sends nothing.
- The same call **with** `confirmed=True` actually sends. The server rejects a confirmed send
  whose arguments differ from the preview, so you must re-send identical args.

This is why `TEST_MODE` is safe: in test mode we simply never pass `confirmed=True`.

## Test mode (default)

```
TEST_MODE = true
```

Because `draft_email` does not persist and `reply_all` would email the real thread, test
mode produces its reviewable artifact by **sending to the operator only** (the signed-in
mailbox from `whoami`) — never to `Filings@`, never `reply_all`. Render the body to email-safe HTML (Step 11) and pass `html=True` on both the draft and the send here too:

- **New thread (S-1):** `draft_email(to=[operator], subject="[TEST] Internal <TICKER>",
  body=<extraction output>)` to preview, then `send_email(to=[operator],
  confirmed=True)` with identical args. First body line: "TEST SEND TO SELF — production
  recipient would be Filings@meteoracapital.com".
- **Amendment (S-1/A):** `draft_email(to=[operator], subject="[TEST] Internal <TICKER>",
  body=<change summary>)` then `send_email(to=[operator], confirmed=True)` — use the
  **canonical (renamed) subject**, not `Re: …`, so the operator sees the rename that would
  happen live. Note in the body which internal thread this would reply-all to in production.
- Always print, per item, in the run summary: the **production** To / Subject and the first
  ~15 lines of body, so the operator sees exactly what would go out live.
- The `[TEST]` subject prefix and the self-only recipient make it unmistakable and safe.

## Live mode

```
TEST_MODE = false
```

- New thread: `draft_email(...)` then `send_email(..., confirmed=True)` with identical args.
- Amendment: `reply_all_email(..., confirmed=True)` with args identical to the preview.
- **Reply-all really does email every participant** on the internal thread — that is the
  intent, but confirm the participant list looks right on the first few live runs.

### Go-live checklist
1. Run several times in test mode across real morning/afternoon windows.
2. Open the staged Drafts and read the reply-all previews; confirm subjects, recipients,
   bodies, and that deSPAC alerts were skipped.
3. Confirm dedup: re-run a window and verify already-processed accessions are skipped.
4. Only then set `TEST_MODE = false`.

## Dedup state file

Because the S-1 body must be **exactly** the extraction output (no footer marker) and the
subject is a fixed format (no room for an accession), accession-level dedup relies on a small
durable state file rather than a marker in the email.

- **Location (durable, on the user's machine):**
  `%USERPROFILE%\Documents\Claude\Scheduled\s1-filing-handler\state.json`
  — the same persistent-folder pattern the other Meteora scheduled skills use. Read/write it
  with the Desktop Commander (or Windows-MCP) file tools. Create the folder + an empty
  `{"processed": {}, "titles": {}}` on first run. The bash sandbox is ephemeral, so do **not**
  keep state there.
- **Shape:**
  ```json
  {
    "processed": {
      "0001104659-26-079324": {
        "ticker": "CGCC", "spac_name": "Cartesian Growth Corporation III",
        "filing_type": "S-1", "thread_subject": "Internal CGCC",
        "mode": "TEST", "ts": "2026-06-30T17:31:00-04:00"
      }
    },
    "titles": { "Cartesian Growth Corporation III": "Internal CGCC" }
  }
  ```
- **Check before every send** (Step 6): if the accession is in `processed`, skip
  ("already processed"). This makes overlapping windows and manual re-runs safe.
- **Record only on success** (Step 12): add the accession *after* the draft/preview/send
  succeeds. If the send failed, leave it out so the next run retries.
- **`titles`** remembers the corrected `Internal <TICKER>` once an amendment reveals a
  ticker for a thread that was opened name-only (see `s1a-redline.md` §5).
- **Secondary guard (belt & suspenders):** even with the state file, Step 8's thread
  detection prevents a duplicate *thread* — if an `Internal …` thread for the SPAC already
  exists, route to the "exists" branch rather than creating a new one. So a lost state file
  degrades to "might re-reply on an amendment", never "spawns duplicate threads".
