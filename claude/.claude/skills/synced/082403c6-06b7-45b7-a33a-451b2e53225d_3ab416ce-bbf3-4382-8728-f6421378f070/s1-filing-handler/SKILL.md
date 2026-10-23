---
name: s1-filing-handler
description: "Twice-daily handler for Meteora's SPACInsider \"[S-1]\" and \"[S-1/A]\" filing alerts (SPACInsider tech@spacinsider.com -> Walter -> Filings@meteoracapital.com; a copy lands in the signed-in user's own Outlook inbox). For each new IPO S-1 it downloads the filing file and runs the spac-s1-extractionv3 skill, then opens an internal thread \"Internal TICKER\" (bare ticker) to Filings@; for an S-1/A it redlines the amendment against the prior filing and replies-all on the existing internal thread. Several S-1s in one run fan out to one sub-agent per filing so the main context stays clean. Use whenever the user says \"run the S-1 handler\", \"process the S-1 filings\", \"check the S-1 inbox\", \"morning/evening S-1 run\", \"handle the SPACInsider S-1 alerts\", or when it fires on its 9:00am / 5:30pm ET schedule. Always use this skill for these SPACInsider S-1/S-1-A alerts — the routing, dedup, and test-mode rules are the point."
---

# S-1 Filing Handler

Turns SPACInsider `[S-1]` / `[S-1/A]` alerts into Meteora internal research threads in
`Filings@meteoracapital.com`, with no manual triage.

**In one line:** the orchestrator does the cheap shared triage (scan the inbox, classify, dedup) and
then fans out **one sub-agent per filing, all at once** — each downloads its own S-1 from the alert's
EDGAR link, finds its thread, runs `spac-s1-extractionv3`, and sends the result into the correct
`Internal <TICKER>` chain. The slow per-filing work runs in parallel, not one filing at a time.

## Architecture — two roles, and why it's fast

The two things that eat the time are the **thread search** and the **download**. They used to run
serially in the main flow, one filing after another. So the split is built to parallelize them:

- **Orchestrator (this main flow) — cheap and central.** Scan the inbox once, classify each alert with
  `parse_alert.py`, drop deSPAC and already-processed ones, and **fan out**. It does **not** download,
  discover threads, or extract — those are the slow parts and they belong to the sub-agents. At the end
  it writes the state file from what the agents report.
- **One sub-agent per filing — parallel, does everything heavy.** Each agent, for its one filing:
  downloads the S-1 from the alert's `index_url` (Desktop Commander), resolves the ticker, finds the
  internal thread, runs `spac-s1-extractionv3` (or a redline), and sends. One filing → one agent →
  one whole-skill call.

**Why this is faster than the first version:** the download and the thread search now run
**concurrently across filings**; each agent fetches its **own** file (no cross-boundary handoff, so no
`edgar-filing-text` fallback); and thread discovery is **cached, fast-pathed, and batched** (Step 4.3)
instead of ~18 sequential searches. See **## Speed** for the full list of levers.

Keep the extraction rule intact: one whole-skill `spac-s1-extractionv3` call on the local file,
output verbatim — never split by section, never fetch the body from `edgar-filing-text`/EDGAR.

---

## TEST MODE (read first)

```
TEST_MODE = false
```

While `TEST_MODE = true`, every send goes **only to the signed-in operator** (`whoami`), subject
prefixed `[TEST]`, with a first body line naming the real recipient (`Filings@` or the thread).
`draft_email(...)` alone returns an ephemeral preview and does **not** persist to Outlook Drafts, so
the reviewable artifact is a real `send_email(..., confirmed=True)` addressed to the operator. Never
`reply_all` the real thread in test mode. Flip to live with `TEST_MODE = false` — see
`references/test-mode.md` first.

---

## Connectors & config

- **Email Assistant (Microsoft 365)** — all mailbox actions: `whoami`, `search_emails`, `read_email`,
  `read_thread`, `list_attachments`, `download_attachments`, `draft_email`, `send_email`,
  `reply_all_email`, `reply_all_rename_thread`. Never use another connector for mail. To reply on a
  chain **and** fix the ticker in the subject in one shot, use `reply_all_rename_thread(...)` (Graph
  `createReplyAll` — keeps it nested); for a same-subject reply use `reply_all_email`.
- **Desktop Commander** — the file channel on the user's **real disk**: `create_directory`,
  `write_file`, `read_file`, `get_file_info`, `start_process` (e.g. `curl`/`pdftotext`). Each sub-agent
  uses it to **download and read its own filing**; the orchestrator uses it for the durable **state
  file**. Use it, not the Bash sandbox, for anything that must persist or be seen by another agent.
- **No Meteora MCP / no EDGAR tools.** This skill uses **no** `edgar-filing-text`, `edgar-filing-index`,
  `edgar-redline`, `spac-details`, or any other Meteora MCP tool. Everything it needs is already here:
  the filing link from the alert, Desktop Commander for the file, the mail connector for the thread, and
  the lean skill for the body. **Never fetch a filing from `edgar-filing-text` or any EDGAR/web source**
  — the filing body always comes from the local file.
- **spac-s1-extractionv3 skill** — the entire new-chain body for a new IPO S-1. This handler runs no
  other analysis skill (never `spac-bios`, never `spac-ioi-summary`).

Scan the **signed-in user's own inbox** (it receives forwarded copies of the Filings@ alerts). New
threads and existing chains live in `Filings@meteoracapital.com`. Source chain:
`tech@spacinsider.com` → `walter@meteoracapital.com` → `Filings@`. Timezone `America/New_York`.

---

## Workflow

### Step 0 — Preflight (orchestrator)
`whoami()`. If "Not signed in", run the Email Assistant sign-in flow and stop. If the connector isn't
registered yet (a fresh-chat ToolSearch for `Email Assistant` returns empty), tell the user *"The Email
Assistant connector is still warming up — please resend your request in a few seconds,"* and stop.
Never report a false "0 filings" when the real cause is no access — fail loud. Read the durable state
file (`references/test-mode.md`) into memory now so its caches are ready for the fan-out.

### Step 1 — Scan the inbox (orchestrator)
`search_emails(subject="[S-1", after="<window start ISO>", folder="Inbox", max_results=50)`. The
`subject="[S-1"` filter catches both `[S-1]` and `[S-1/A]`. The connector only bounds the start, so
filter client-side to the window end. Default window = today ET (or since the last run); paginate if
capped.

### Step 2 — Classify & gate (orchestrator)
Fetch the hit bodies **concurrently** (batch the `read_email` calls in one message, don't read them one
by one), then per hit run `python scripts/parse_alert.py --parse` → `filing_type` (`S-1` vs `S-1/A`),
`spac_name`, decoded `index_url` + `cik` + `accession`, `subtype` (`ipo` vs `despac`). Verify the
SPACInsider→Walter chain. Then gate:

- **deSPAC skip:** `subtype == despac` → skip ("out of scope").
- **Dedup:** `accession` already in the state file → skip ("already processed").
- **Not from the chain** → skip.

If nothing survives, **send nothing** — post "no new S-1 filings in the window" in chat and stop. Never
send a "nothing found" email. Otherwise carry a brief per survivor:
`{ message_id, spac_name, filing_type, cik, accession, index_url }`.

### Step 3 — Fan out (orchestrator)
Fire **one sub-agent per surviving brief, all in a single message** so they run concurrently. Give each
its brief plus the in-memory caches it needs (`threads` and `titles` from the state file). Each agent
runs Step 4 end to end and returns a status line + the fields to cache. Collect the returns.

### Step 4 — Per-filing job (each sub-agent, in parallel)

1. **Download the S-1 with Desktop Commander.** From the brief's `index_url`: `start_process` a
   `curl`/`Invoke-WebRequest` (descriptive EDGAR User-Agent, e.g. `Meteora ops@meteoracapital.com`) to
   fetch the index page, pick the **primary document** (the S-1/S-1-A `.htm`, not an exhibit) from its
   document table, and download that document to a real-disk temp path. (Attachment case:
   `download_attachments` then save.) The body comes from this file — **never** `edgar-filing-text`. If
   the download is empty, report an error for this filing; do not fall back to EDGAR.
2. **Resolve the ticker** from the alert body and the **downloaded cover page** (`spac-s1-extractionv3`
   also enumerates the tickers). Base **common ticker** (strip trailing `U`/`W`/`R`/`RT`/`WS`;
   `VII.U`→`VII`), disambiguate reuse by the `cik`. Canonical subject = **`Internal <TICKER>`** (bare
   ticker). No ticker yet → `Internal <SPAC Name>` placeholder. Never invent a ticker.
3. **Find the internal thread — fast. Stop at the first hit:**
   - **(a) Cache.** Look up the ticker in the `threads` cache (and the name in `titles`). A hit gives the
     thread's `message_id` + subject → **skip searching entirely.**
   - **(b) Fast path.** One **batched** `search_emails` on the two likeliest subjects — `Internal <COMMON>`
     and `Internal <COMMON>U` (the unit) — fired **concurrently** across SentItems + Inbox.
   - **(c) Full matrix, only if (a) and (b) miss AND this is an S-1/A.** An amendment must have a chain
     somewhere, so run the full identifier×folder matrix in `references/decision-tree.md` — but fire
     **all its searches concurrently in one batch**, never one after another.
   - **Brand-new S-1 shortcut:** for an **S-1 (IPO)** where (a) and (b) miss cleanly, **open a new chain**
     — do **not** run the full matrix to prove a negative for a fresh name.
   - Match rules unchanged (exact token, never collapse roman numerals, clean threads only) —
     `references/decision-tree.md`.
4. **Decide & build the body (the 2×2 — `references/decision-tree.md`):**
   - **`full-lean`** (new chain, or S-1/A with no chain) → **run `spac-s1-extractionv3` on the local
     file**, whole skill, one invocation, output **verbatim**. Never section-split or re-derive.
   - **`redline`** (S-1/A on an existing chain) → run `spac-s1-extractionv3` on the local file, then
     diff its fields against the **prior extraction in the thread** (`read_thread`) — impactful changes
     only, `old → new` verbatim (`references/s1a-redline.md`). No EDGAR.
5. **Render + send.** One-line header (`ticker · form · filing date · CIK · accession`), then
   `python scripts/render_email_html.py <body.md> <out.html>` (inline styles, bordered tables, no
   colors), send with `html=True`:
   - **TEST_MODE:** `send_email(..., html=True, confirmed=True)` to the **operator only**, subject
     `[TEST] <canonical_subject>`.
   - **LIVE — new chain:** `send_email(to Filings@meteoracapital.com, subject=<canonical_subject>,
     html=True, confirmed=True)`.
   - **LIVE — reply:** `reply_all_email` (same subject) or `reply_all_rename_thread` (ticker newly known)
     on the thread. Preview first, verify a clean recipient list, then resend identical + `confirmed=True`.
6. **Return** one status line **plus** the cache fields the orchestrator needs:
   `[TICKER] SPAC Name — <S-1|S-1/A> — <action> — accession` and
   `{ accession, ticker, spac_name, thread_subject, thread_message_id }`. Never return the body.

### Step 5 — Record & summarize (orchestrator)
From the returns, for each **successful** send write the state file (centralized here to avoid parallel
write races): add `processed[accession]`, `titles[spac_name]`, and — the speed win —
`threads[ticker] = { subject, message_id }` so the **next amendment does no discovery at all**. Never
record a failed send. Post the run summary.

---

## Speed (the levers, in one place)

- **Parallel, not serial.** Every per-filing job — download, discovery, extract, send — runs in its own
  sub-agent, all fired in one message, so N filings take ~1 filing's time, not N×.
- **Each agent fetches its own file.** No cross-boundary handoff, so no re-download and no
  `edgar-filing-text` fallback.
- **Discovery is cache → fast → full.** The `threads` cache skips discovery outright; a miss tries just
  two likely subjects; the full ~18-search matrix runs **only** for an amendment that still wasn't
  found — and even then every search is fired **concurrently in one batch**.
- **A brand-new S-1 skips the matrix.** There is nothing to find, so it opens a new chain immediately.
- **The cache compounds.** After a name's first filing, its amendment (the redline case) does **zero**
  discovery searches — it replies straight to the cached `message_id`.

---

## Run summary (post in chat every run)

```
S-1 handler — <date> — MODE: <TEST|LIVE>

Processed (N):
- [TICKER] SPAC Name — S-1 (IPO) — new thread → Filings@ (accession)
- [TICKER] SPAC Name — S-1/A — reply-all on "Internal …" (accession, redline vs <prior>)

Skipped (N):
- SPAC Name — deSPAC registration, out of scope
- SPAC Name — already processed (prior run)

Needs attention (N):
- SPAC Name — no ticker yet → used "Internal <SPAC Name>" (rename when assigned)
- subject snippet — parse failure, manual review
```

---

## Guardrails

- **Each sub-agent downloads and reads its own file (Desktop Commander).** No cross-boundary handoff —
  the file lives in the agent that uses it. The body always comes from that local file; **never**
  `edgar-filing-text` or any EDGAR/web fetch. A `redline` reads the prior extraction from the thread
  (`read_thread`), so it needs no EDGAR either.
- **Discovery is cached, fast-pathed, and batched.** Check the `threads` cache first; try two likely
  subjects; run the full matrix **only** for an amendment that's still unfound; skip it entirely for a
  brand-new S-1. Fire every multi-search step **concurrently in one message** — never ~18 sequential
  searches.
- **The sub-agent invokes the whole skill.** One `spac-s1-extractionv3` call per filing on the local
  file, output verbatim — identical to a manual run. Never section-split or hand-reproduce the field spec.
- **State writes are centralized in the orchestrator** (Step 5) so parallel agents never race on the file.
- **One sub-agent per filing** — each returns a status line, not the body.
- **Fail loud on no access**; **empty run sends nothing**; **dedup is mandatory** by accession; **never
  record a failed send.**
- **deSPAC skip** — the `[S-1]` stream mixes IPO and deSPAC registration S-1s; only IPOs extract.
- **Clean-thread only** — never reply-all onto a chain with a no-reply/alert participant; verify the preview.
- **No-ticker fallback** `Internal <SPAC Name>`, renamed to `Internal <TICKER>` once known.
- **Redline baseline is the prior extraction in the thread** (the immediately-prior filing), named in the reply.
- **Send as HTML**, never raw markdown. **TEST_MODE is the safety net** — keep it `true` until the user
  has reviewed real self-sends.

## Files
- `scripts/parse_alert.py` — SafeLinks decode, `index_url`/CIK/accession parse, S-1-vs-S-1/A + IPO-vs-deSPAC classify. Deterministic; prefer it over eyeballing.
- `scripts/render_email_html.py` — markdown → inline-styled, email-safe HTML.
- `references/decision-tree.md` — fast discovery (cache/fast-path/batch), the full matrix, routing 2×2, edge cases.
- `references/s1a-redline.md` — diffing the new S-1/A extraction against the prior thread post, the change-summary format.
- `references/test-mode.md` — test vs live send rules, and the state file (dedup + the `threads`/`titles` caches).
