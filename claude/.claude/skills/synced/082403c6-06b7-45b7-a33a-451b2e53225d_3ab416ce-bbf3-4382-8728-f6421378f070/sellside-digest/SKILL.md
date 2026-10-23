---
name: sellside-digest
description: Two-phase daily sell-side research router. Phase A (5:00 PM) emails the signed-in user asking for today's "tickers of interest"; Phase B (5:30 PM) sweeps the last 24h of sell-side research in Outlook (Email Assistant / Microsoft 365) — broker desk notes in email bodies, attached research PDFs (text-extracted every run), and research-portal links — attributes each note to its primary ticker(s), scopes the run to the replied tickers (no reply or "ALL" = full digest), then reply-alls a per-ticker summary onto the existing INTERNAL chain, creating a new "INTERNAL {TICKER}" thread to Filings@meteoracapital.com when none exists. Also renames ad-hoc chains, attaches source PDFs, flags unroutable notes, and archives digests to Google Drive. Trigger on "run the sell-side digest", "sellside digest", "research sweep", "comb my email for broker notes", "run the ticker ask", "ask for tickers of interest", or the 5:00/5:30 PM scheduled runs. Always use this skill for the daily sweep — never triage broker research ad hoc.
---

# Sell-Side Digest (5:00 PM ticker ask + 5:30 PM research router)

The daily workflow runs in two phases, as two scheduled tasks (see Scheduling):

- **Phase A — 5:00 PM ticker ask.** Email `ask_recipient` (the signed-in user who owns the scheduled runs) asking which tickers matter today. They reply to that email with tickers.
- **Phase B — 5:30 PM digest.** The sweep-and-route run below. When Phase A got a reply, only the listed tickers are digested; **no reply means the full digest runs for all tickers**, so the ask can never cost you a day's research.

Phase B does four things:

1. **Sweep** the signed-in user's inbox for sell-side research received in the last 24 hours.
2. **Attribute** each note to its primary ticker(s) and summarize it.
3. **Route** a per-ticker digest onto the existing internal email chain whose subject contains that ticker (reply-all, renaming ad-hoc chains to `INTERNAL {TICKER}` on the way), or
4. **Create** a new thread `INTERNAL {TICKER}` to Filings@meteoracapital.com when no chain exists.

On every run it also **downloads and extracts every attached research PDF** (the substance often lives only in the PDF, not the email) and **opens the research links** inside each note — using whatever the signed-in mailbox is entitled to reach and discarding the ones behind a login/paywall. Around that it attaches the source PDFs to each digest, flags notes it couldn't route so they surface on your Outlook follow-up list, optionally archives originals to disk, and saves each digest to a Google Drive folder as its own Google Doc (Step 4d). A separate one-time command sets up server-side Outlook rules that pre-sort broker research before the run even starts.

Designed to run unattended on a daily schedule, and to be portable: everything binds to the *signed-in user's* mailbox and domain, so the same .skill file works on anyone's Claude once they connect their Microsoft account.

---

## Config

Edit these lines to retarget the skill. The invoking prompt can override `test_mode` (see Modes).

| Key | Default | Meaning |
|---|---|---|
| `internal_domain` | `auto` | Domain that counts as "internal". `auto` = the domain of the signed-in user's own address (from `whoami()` / `get_me`). Set explicitly (e.g. `meteoracapital.com`) to override. |
| `new_thread_recipient` | `Filings@meteoracapital.com` | Where new `INTERNAL {TICKER}` threads are sent. |
| `new_thread_subject` | `INTERNAL {TICKER}` | Subject template for new threads. Bare ticker, no brackets (e.g. `INTERNAL WBD`) — matches the house "Internal TICKER" convention. |
| `lookback_hours` | `24` | Sweep window, measured back from run time. |
| `test_mode` | `true` | `true` = drafts only, `[TEST]` subject prefix, new-thread drafts addressed to SELF instead of Filings@. Flip to `false` after one verified run (or say "live" in the prompt). |
| `ignore_senders` | (empty) | Addresses/domains never treated as research (e.g. newsletter feeds). |
| `extra_research_senders` | (empty) | Addresses/domains always treated as research candidates even if they don't look like a bank. |
| `rename_threads` | `true` | When routing onto a chain whose subject isn't already `INTERNAL {TICKER}`, rename it to the house convention via `reply_all_rename_thread` (stays nested). Future runs then match it on the priority-1 search. Email Assistant only — falls back to a plain reply-all on the M365 connector. |
| `attach_pdfs` | `true` | Attach the source research PDFs to the digest email (per-file cap ~3 MB; oversized files are noted instead). Note: this only governs *attaching* PDFs to the outbound email — it does **not** gate PDF *ingestion*, which always happens (see "PDF ingestion is mandatory" in Step 1). |
| `follow_links` | `true` | Open the research links inside each note (portal "READ MORE" / "View PDF" / "Access this report" links) and fold the fetched content into the summary. Links that resolve to real content (a signed-in session, or a public page) are used; links that hit a login/paywall/consent wall are discarded — noted, never treated as an error. See "Follow the links" in Step 1. |
| `flag_unrouted` | `true` | Put the Outlook follow-up flag on research the run couldn't route (no ticker / borderline), so it doesn't vanish into the chat transcript. |
| `archive_dir` | (empty) | When set (e.g. `~/Downloads/SellsideResearch`), save each unique note under `{archive_dir}/{YYYY-MM-DD}/` — original email as `.eml` plus its PDFs. Empty = no archiving. |
| `research_folder` | (empty) | Exchange folder that server-side rules move broker research into (see One-time setup). When set, the sweep searches this folder **and** the inbox. Empty = inbox-only sweep, no rules assumed. |
| `drive_archive` | `true` | After composing each per-ticker digest, save a copy as a Google Doc in the Drive folder below (one Doc per digest). Set `false` to disable. Needs the Google Drive connector; if it's absent the run skips this and says so. |
| `drive_folder_id` | `1EidMywHbawquHCcG79xDo-jE3bMI0YRz` | Target Drive folder ("Sellside Digest") for the archived digest Docs. This is the folder id from the Drive URL, not the whole URL. |
| `ask_tickers` | `true` | Two-phase mode: 5:00 PM ask (Phase A) + 5:30 PM scoped run (Phase B, Step 0). `false` = no ask, every run is a full digest (legacy single-run behavior). |
| `ask_recipient` | `SELF` | Who receives the 5:00 PM ask and whose reply scopes the run — the signed-in user who set up the scheduled tasks (at Meteora typically `lfeldman@meteoracapital.com`). Set an explicit address to override; it must be on `internal_domain`. |
| `ask_subject` | `Tickers of interest — sell-side digest {YYYY-MM-DD}` | Subject template for the ask email. Phase B locates today's ask thread by this subject plus the `[SELLSIDE-TICKERS` body marker — change it in both phases or not at all. |

---

## Modes

- **TEST (default):** never pass `confirmed=True` to any send, rename, rule, or flag tool — no mailbox mutation of any kind. Create drafts only. Prefix every subject with `[TEST]`. Address new-thread drafts to the signed-in user (SELF), not `new_thread_recipient`. Skip flagging and thread renaming (report "would flag/rename" instead). Local archiving to `archive_dir` still runs — it writes to disk, not the mailbox. Google Drive archiving (Step 4d) also still runs, because it writes to a dedicated archive folder rather than the mailbox — but prefix the Doc title with `[TEST]` so test artifacts are obvious and easy to delete. Report where the drafts and Docs are. Phase A in TEST likewise only drafts the ask (to SELF, `[TEST]` subject prefix) — which means a TEST Phase B will normally find no reply and correctly exercise the full-digest fallback.
- **LIVE:** actually send. Activated when `test_mode` is set to `false` in this file, **or** when the invoking prompt contains the word "live" (e.g. a scheduled task prompt of `Run the sell-side digest (live)`). This lets the owner go live without re-packaging the skill.

Never loosen the internal-only guard (Step 3) in either mode.

---

## Scheduling — two weekday tasks (ET)

- **5:00 PM** — prompt `Run the sell-side digest ticker ask (live)` → Phase A only (send the ask, stop).
- **5:30 PM** — prompt `Run the sell-side digest (live)` → Phase B (Step 0 onward).

"live" in the prompt flips LIVE mode per Modes. An ad-hoc "run the sell-side digest" works at any time: if no ask thread exists for today, Step 0 simply falls back to the full digest. When `ask_tickers` is `false`, schedule only the digest task.

---

## Tooling

Mailbox operations go through the **Email Assistant (Microsoft 365) extension** when present. Core set: `whoami`, `search_emails`, `read_email`, `read_thread`, `list_attachments`, `download_attachments`, `draft_email`, `send_email`, `reply_all_email`. Enhancements: `reply_all_rename_thread` (thread renaming), `flag_email` (follow-up flags), `download_email_as_eml` (archiving), `list_message_rules` / `create_message_rule` / `delete_message_rule` (server-side pre-filtering). Load them via ToolSearch with query `Email Assistant` (or `outlook`).

- If the Email Assistant extension is absent, fall back to equivalent tools on the **Microsoft 365 connector** (ToolSearch `outlook email search`, `send mail`, etc.). The core workflow is identical; only tool names change. The enhancement tools mostly have no connector equivalent — degrade gracefully: skip renaming (plain reply-all), flagging, .eml archiving (archive PDFs only), and rules, and say in the run report which features were skipped and why. If neither surface exposes email read+send for the signed-in user, stop and tell the user which connector to enable — do not improvise.
- **Never send through any other MCP's send-email** (e.g. a Meteora MCP `send-email` that sends as a fixed shared mailbox). This skill must send as the signed-in user, otherwise it is not portable and misattributes authorship.
- First step of every run: `whoami()` (or `get_me`). If not signed in, stop and print the sign-in instruction. Record the user's address — it defines SELF and (when `internal_domain: auto`) the internal domain.
- On a fresh chat the extension may still be registering: if one ToolSearch returns nothing, say the connector is warming up and ask the user to resend — do not declare it broken.

Link-following (Step 1, `follow_links`) uses **`web_fetch`** for the research links, and the **browser tools** (`navigate` + `get_page_text`, load via ToolSearch) when a page is JS-rendered and `web_fetch` returns only a shell. These read pages the signed-in user is already entitled to; they never authenticate or bypass a wall. If neither is available, skip link-following and note it — the run still proceeds on body + PDF content.

Drive archiving (Step 4d) uses the **Google Drive connector** — the `create_file` tool (load via ToolSearch `google drive create file`) and `search_files` for the dedup check. This is a separate connector from email; it is not needed for the core sweep-and-route workflow. If it isn't connected, skip Step 4d and note it in the run report — never block the digest send on it, and never fall back to some other storage.

File I/O note (Windows hosts): any temp text you write while extracting PDFs must use `encoding='utf-8'` in Python `open()` calls — Windows defaults to cp1252 and silently corrupts non-ASCII.

---

## One-time setup — server-side pre-filtering (optional)

Not part of the daily run. Trigger when the user says "set up the research rules" (or asks to pre-sort broker mail), and offer it once if runs keep classifying a large inbox from scratch.

Create Exchange inbox rules with `create_message_rule` so research is pre-sorted **before** the 5:00 PM run — rules execute server-side, even with Claude closed:

- For each known broker domain the user confirms (seed the list from domains actually seen in recent sweeps, plus `extra_research_senders`): move to `research_folder` (or `assign_categories=["Sell-side"]` if the user prefers mail to stay in the inbox).
- For `ignore_senders`: `mark_read` + move to a junk-adjacent folder the user names. Never auto-delete.

Mechanics: preview each rule by calling `create_message_rule(...)` **without** `confirmed`, show the user the When/Then, then repeat with identical arguments and `confirmed=True`. Review existing rules first with `list_message_rules()` to avoid duplicates; remove stale ones with `delete_message_rule`. Because this mutates the mailbox permanently, set rules up only interactively — never mid-run on a schedule, and never in TEST mode.

Rules are a **pre-filter, not the classifier**: they only catch listed domains, and Graph rules can't judge content. The sweep still classifies by content, and still covers the inbox for research from senders no rule knows about.

---

## Phase A — 5:00 PM ask for tickers of interest

Runs as its own scheduled task ~30 minutes before the digest. Skip entirely when `ask_tickers` is `false`.

1. `whoami()` — resolve SELF; stop if not signed in.
2. **Idempotence check:** search Sent Items (and Drafts in TEST) for today's `ask_subject`. If today's ask already exists, don't send a second one — report "ask already sent" and stop.
3. Send a **fresh email** (not a reply) to `ask_recipient`:

```
Subject: Tickers of interest — sell-side digest {YYYY-MM-DD}

Reply to this email with today's tickers of interest, separated by spaces or commas
(e.g. "WBD LKSP NVDA"). The 5:30 PM digest will cover only those names.

- Reply "ALL" for the full digest.
- No reply by 5:30 PM = full digest (all tickers), as usual.

[SELLSIDE-TICKERS {YYYY-MM-DD}]
```

The marker line is load-bearing twice over: Phase B locates today's ask thread by it, and Step 1 uses it to keep the ask email and its replies out of the research sweep. Never omit it.

Send mechanics follow the house gate: preview without `confirmed`, verify the recipient is on `internal_domain`, then send with identical arguments and `confirmed=True`. (TEST mode: draft only, to SELF, `[TEST]` subject prefix.) Phase A sends exactly one email and does nothing else — no sweeping, no routing.

## Step 0 — Read the tickers of interest (Phase B, before anything else)

Skip when `ask_tickers` is `false`. Otherwise:

1. Find today's ask thread: `search_emails(subject="{ask_subject for today}")`, falling back to a body search for `[SELLSIDE-TICKERS {YYYY-MM-DD}]`. Only today's marker counts — yesterday's reply must not scope today's run.
2. `read_thread` and take the **latest human reply** (any message after the ask itself). Parse tickers from it: split on whitespace/commas/semicolons/newlines, uppercase, strip `$` and punctuation, keep 1–5 letter tokens that look like tickers, ignore filler words. Normalize SPAC class variants to the base common ticker (strip trailing U/W/R/WS) exactly as in Step 2 — a reply of "LKSPU" scopes to LKSP.
3. Outcome (state it in the run report either way):
   - **Tickers parsed → scoped run.** Only notes whose primary ticker(s), after normalization, intersect the list are summarized and routed. Everything else — research on other tickers AND no-ticker macro/sector pieces — is **disregarded**: no digest, no flag, just an `Out of scope` tally in the run report. The Step 1 sweep still covers the entire window at full depth; scoping is applied at attribution (Step 2), never by narrowing the mailbox search — a keyword-narrowed sweep would misattribute forwards and multi-name notes.
   - **Reply is ALL** (or "all tickers" / "everything") → full digest.
   - **No thread, no reply, or nothing parseable** → full digest, exactly as if `ask_tickers` were off. An ambiguous reply ("the usual", "same as yesterday") is also a full-digest fallback — guessing a scope risks silently dropping research, and the full digest merely costs a few extra emails.

A reply that arrives after Phase B has started counts for nothing — the run uses whatever was in the thread when Step 0 executed; don't re-run automatically.

## Step 1 — Sweep the last 24 hours

Compute `after = now − lookback_hours` as an ISO timestamp. Then:

```
search_emails(after=<ISO>, folder="inbox", max_results=<large>, sort_by="date", order="desc")
```

**No cap on how many emails the run parses — cover the *entire* window.** The invariant is completeness: every message received on/after `after` must be classified. `max_results` is a per-call **page size**, never a ceiling on the sweep, and the tool's small default (often 25) will silently truncate a busy inbox — so pass a large value (e.g. 1000, the Graph page maximum) explicitly and treat a full-looking page as "there may be more," not "done."

Keep fetching until the window is provably exhausted, then classify the union. A page is **not** the end of the window while either is true: it came back with as many messages as you asked for, **or** its oldest message is still newer than `after`. When that holds, get the next slice — using whichever mechanism the tool offers:

- **Pagination token / next-page link** (preferred when present) — follow it until there are no more pages.
- **Otherwise, slice so no single call can truncate the window.** Re-query the same window per sender (broker domains seen so far + `extra_research_senders`), and/or split the time window into smaller sub-windows (e.g. 24h → 6h → 1h) and union everything. Narrow until each call comes back not full.

Union all pages/slices and **dedup by message id** before classifying (the same message id can surface in overlapping slices). If for any reason you cannot confirm the whole window was covered (a tool cap you can't page past), say so explicitly in the run report with the count seen and the boundary reached — never quietly stop at a round number. Under-fetching drops research on the floor, which defeats the skill; err toward more calls.

If `research_folder` is set, run this same exhaustive sweep over that folder too — its contents are pre-qualified candidates (a rule put them there), but content still decides whether each is research. Then classify every message across both folders.

**Counts as sell-side research (collect it):**
- **Published research** — PDF attachment(s) with rating / price target / estimates / analyst certification / disclosure pages. The email body may be a stub ("please see attached").
- **Desk commentary in the email body** — sales & trading / event-driven / merger-arb / SPAC desk notes: analytical text on a name, often headed "EVENT DRIVEN", "SALES & TRADING", "For Institutional Use Only", with probability trees, spread math, or catalyst timelines. (Reference example: an "RJF Event Driven: WBD - TGNA Part II ?" note from RaymondJames.com — body-only, no PDF.)
- **Internal forwards OF broker research** (`Fw:` chains where the underlying content is a broker note). The research is the underlying note; attribute it to the original broker/analyst, not the forwarder. It's in scope if the forward landed inside the window.
- Sender heuristics: bank/broker domains (raymondjames.com, cantor.com, gs.com, jefferies.com, etc.), research distribution addresses, anything in `extra_research_senders`. But content decides — a broker email that is pure logistics is out; an analytical note from an unlisted boutique is in.

**Not research (skip, but list in the run report if borderline):**
- Corporate access / conference invites, roadshow logistics, call scheduling, marketing blasts with no analysis.
- Pure news clippings / press releases without broker analysis.
- Internal-origin analysis that isn't forwarding broker content (that's the team's own work, not sell-side).
- Prior digests sent by this skill (any message whose body contains the `[SELLSIDE-DIGEST` marker) and their threads' confirmations.
- The skill's own ticker-ask emails and their replies (subject or body contains `[SELLSIDE-TICKERS`).
- Anything from `ignore_senders`.

**Collapse duplicate copies.** The same note routinely arrives 2–3 times (direct + team distribution + an internal forward + "confirming receipt" replies). Fingerprint each note as `(broker, note title with Fw:/Re: stripped, publication date)` and summarize it **once**, keeping the cleanest copy (prefer the original broker email; else the most complete forward).

**PDF ingestion is mandatory — do it on every run.** For any note with a PDF attachment, always `download_attachments` then extract the text (`pdftotext -layout`, or pypdf as a fallback) and summarize from the *extracted content*, not from the covering email. The email body is frequently a stub ("please see attached") while the real rating/PT/thesis lives only in the PDF — skipping extraction silently drops the substance of the note. This is not optional and is not gated by `attach_pdfs` (that flag only controls whether the file rides along on the outbound email). Read enough to get the rating/PT/thesis and the numbers — first pages plus the summary/valuation section usually suffice; read fully when the note is short or the thesis is unclear. Keep the downloaded file paths — Step 4 attaches them when `attach_pdfs` is on. If a PDF genuinely won't extract, fall back to the body and mark the entry "(attachment unreadable — see original email)" per Failure handling — but attempt extraction first, every time.

**Follow the links (when `follow_links` is true — the default).** Body notes and PDF cover-emails routinely put the real content one click away — a portal "READ MORE" / "View PDF" / "Access this report" / "Continue reading" link, or a linked research aggregator. On every run, open these links and fold what you get into the summary, because the emailed teaser is often just the first paragraph. Use `web_fetch` (or the browser tools if the page is JS-rendered); expect a mix and handle each by what comes back:

- **Signed-in / public → use it.** If the link resolves to the actual note (an authenticated research-portal session that's already logged in, or a public page), read it and treat it as the primary source for that note's findings — richer than the email teaser.
- **Login / paywall / consent wall → discard it.** If the fetch lands on a sign-in page, SSO redirect, paywall, cookie/consent gate, or an empty JS shell, that link yielded nothing — drop it silently, fall back to whatever the email body/PDF gave you, and note it (see the run report's `Links` line). Never treat a gated link as a failure that aborts the note, and never try to bypass the wall.

The point is to capture everything actually reachable from the signed-in mailbox's own entitlements without getting blocked on the links that aren't. Which providers are logged in varies by user and by day, so decide per-link on what the fetch returns rather than assuming — a provider that's gated today may be open tomorrow and vice-versa. Respect `web_fetch`'s content restrictions: if a fetch is blocked, that link counts as discarded; do not reach for other means to retrieve it.

**Archive (when `archive_dir` is set).** For each unique note, save the kept copy with `download_email_as_eml(message_id, output_dir="{archive_dir}/{YYYY-MM-DD}")` and put its downloaded PDFs alongside. The .eml matters most for body-only desk notes — with no PDF, it is the only durable copy of the research. Runs in both modes (disk write, not a mailbox write); on the connector fallback, archive PDFs only and note the limitation.

## Step 2 — Attribute and summarize

For every unique note, extract:

- **Primary ticker(s)** — the name(s) whose investment case the note actually analyzes. The subject line is the strongest anchor (`RJF Event Driven: WBD - TGNA Part II ?` → WBD); the body confirms. Counterparties, acquirers, and comps mentioned in passing are *secondary* — do not open a digest for them. A note that materially analyzes two names as investable situations goes under **both**, marked "(multi-name note, also filed under {OTHER})".
- Company named without a ticker → resolve the ticker; verify with a quick lookup if unsure rather than guessing.
- No attributable single name (macro, sector, strategy pieces) → skip the note and list it in the run report under "no ticker".
- **Broker, analyst/desk, note title, publication date/time, delivery form** (body note vs. PDF vs. portal link). When a link was followed and used, source the findings from it; when a link was gated and discarded, summarize from the body/PDF and don't imply you read the full note.
- **Action**, if any: initiate / upgrade / downgrade / reiterate / PT change / estimate change / event-probability update.
- **3–6 finding bullets**, front-loaded: the call, the numbers (PTs, probabilities, break prices, spreads), the catalysts and dates. House style: findings first, methodology never. Flag clearly when a figure is the desk's *market-implied* framework rather than the desk's own estimate — desk notes often present both.

**Scoped runs (Step 0 produced a ticker list):** after attribution, drop every note whose primary ticker(s) don't intersect the list — no summary, no routing, no flag; tally it for the run report's `Out of scope` line. A multi-name note survives if *any* of its primary names is listed, and is filed only under the listed name(s). Secondary mentions never rescue a note: a TGNA-primary note that mentions WBD in passing is out of scope when only WBD is listed. "No ticker" macro/sector pieces are likewise disregarded on scoped runs (report-only, no flag).

Ticker normalization for thread matching (Step 3): treat SPAC class variants as their base common ticker (strip trailing U / W / R / WS when it's a unit/warrant/right of the same issuer) — a note on LKSPU should route to the LKSP chain. Keep the as-published ticker inside the summary text.

## Step 3 — Find the ticker's email chain

For each ticker with ≥1 note, in priority order:

1. `search_emails(subject="INTERNAL {TICKER}")` — an exact house internal thread (accept `Internal {TICKER}` case-insensitively). If found, use the most recently active one.
2. Otherwise `search_emails(subject="{TICKER}")` and filter to candidates where the ticker appears as a **standalone token** in the subject (delimited by start/end, space, `-`, `:`, `/`, `(`, `[`, or `$` prefix). "WBD" matches `Re: WBD spread math` and `WBD - TGNA situation`, not `WBDS`. Pick the most recently active qualifying conversation.

Then apply two hard filters to the chosen candidate before sending anything:

- **Internal-only guard (never skip this).** `read_thread` on the candidate and inspect the **latest message's** From/To/Cc. Every address must be on `internal_domain`. If any live participant is external, the thread is **disqualified** — try the next candidate or fall through to thread creation. This is the guard that matters: the broker's own distribution email has the ticker in its subject and *will* appear in the search; replying-all onto it would send your internal summary to the broker. In LIVE mode, re-verify recipients one more time from the reply-all preview before confirming.
- **Not the delivery chain of today's notes.** Exclude conversations that are merely the forward/receipt chain of a note collected in this run (subject fingerprint-matches a Step-1 note). Posting a summary of a note onto the note itself adds nothing; that ticker gets a dedicated `INTERNAL {TICKER}` thread instead, which becomes the consolidation chain going forward. (An older internal discussion chain whose subject happens to start with `Fw:` but is *not* one of today's notes remains a valid target.)

No qualifying chain → **create one** (Step 4b).

## Step 4 — Compose and send

One email per ticker per run, covering **all** of that ticker's notes from the window.

**Body template (plain text):**

```
Sell-side research received in the last {lookback_hours}h — {TICKER} ({N} note[s]).

1) {Broker} — {Analyst or desk} — "{Note title}" ({Mon D, h:mm a ET}; {body note | PDF})
   {Action line, if any: e.g. "Reiterates OW, PT $31" or "Event framework update"}
   - {finding}
   - {finding}
   - {finding}

2) ...

[SELLSIDE-DIGEST run {YYYY-MM-DD HH:mm ET}]
```

The final marker line is load-bearing — it is how future runs recognize prior digests (dedup) and how the sweep excludes the skill's own output. Never omit it.

**Attachments (when `attach_pdfs` is true):** pass the local paths of the ticker's downloaded research PDFs in `attachments` (applies to 4a and 4b alike), so the internal thread is self-contained instead of pointing back at the original email. Skip any file over ~3 MB and mark its entry "(PDF too large to attach — see original email)". Body-only desk notes have nothing to attach — that's fine.

**4a — Existing chain:** reply-all on the **latest message** of the chosen conversation so recipients = current participants. Which tool depends on the chain's subject (strip `Re:`/`Fw:` prefixes, compare case-insensitively):

- Subject already `INTERNAL {TICKER}` → `reply_all_email(message_id, body)`.
- Anything else (e.g. `Re: WBD spread math`) and `rename_threads` is true → `reply_all_rename_thread(message_id, body, new_subject="INTERNAL {TICKER}")`. This replies to everyone AND renames the conversation while keeping it nested, converting the ad-hoc chain into the house convention — the next run finds it via the priority-1 search instead of fuzzy ticker matching. If the tool isn't available (connector fallback), use plain `reply_all_email` and note it in the report.

Same confirm gate either way: call **without** `confirmed` to preview recipients (and, for renames, the old→new subject); verify every recipient is internal; then call again with identical arguments and `confirmed=True`. (TEST mode: stop at the preview/draft, no rename, `[TEST]` prefix in the body's first line since reply subject is inherited.)

**4b — No chain:** `draft_email(to=[new_thread_recipient], subject="INTERNAL {TICKER}", body=..., attachments=[...])`, verify, then `send_email` with identical arguments and `confirmed=True`. (TEST mode: draft only, subject `[TEST] INTERNAL {TICKER}`, addressed to SELF.)

**4c — Flag what fell through (when `flag_unrouted` is true):** after routing, call `flag_email(message_id)` on the kept copy of every research note that got no digest — "no ticker" macro/sector pieces and borderline items worth a human look. The chat report scrolls away; the Outlook follow-up flag doesn't. Don't flag non-research skips (invites, logistics). When the user later handles one, they can clear it themselves or ask for `unflag_email`. (TEST mode / connector fallback: report "would flag" instead. Scoped runs: skip flagging entirely — out-of-scope and no-ticker notes were deliberately disregarded per the reply, not dropped by accident; they live in the run report only.)

**Dedup across runs (stateless — works even where the filesystem resets).** Before composing, scan the target thread for prior messages containing `[SELLSIDE-DIGEST`. Any note whose broker + title + date already appears in a prior digest on that thread is dropped from today's email. If every note for a ticker is already covered, skip the ticker and say so in the run report. The 24h window plus this check makes overlapping or re-triggered runs safe.

**4d — Archive the digest to Google Drive (when `drive_archive` is true).** Save the exact digest — the same body you composed for 4a/4b, marker line included — as a **Google Doc** in the `drive_folder_id` folder, one Doc per ticker per run. This is the archive the user reads later in Drive; it mirrors the email, not the raw research.

- **Title:** `{YYYY-MM-DD} {TICKER} — sell-side digest ({N} note[s])`, e.g. `2026-07-14 WBD — sell-side digest (2 notes)`. In TEST mode prefix `[TEST] ` so test Docs are obvious.
- **Dedup first (idempotent, so a re-run doesn't double-write):** `search_files(query="title = '{exact title}' and parentId = '{drive_folder_id}' and mimeType = 'application/vnd.google-apps.document'")`. A hit means this digest is already archived → skip and note it. This is the Drive analogue of the thread `[SELLSIDE-DIGEST` check; the title carries date+ticker+count, so a same-day re-run with the same notes is a no-op and a genuinely new run (different date or note count) writes a new Doc.
- **Create:** `create_file(title=<title>, parentId=<drive_folder_id>, textContent=<digest body>, contentMimeType="text/plain")`. Leave `disableConversionToGoogleType` unset — Drive converts `text/plain` into a native Google Doc, which is what makes it searchable and previewable. Do **not** base64-encode; the body is UTF-8 text, so `textContent` is correct.
- Archive **every** digest the run produces, whether it routed via 4a or 4b. A ticker that was skipped (already covered, or no research) produces no digest, so it gets no Doc.
- Only the digest is archived here — raw broker emails/PDFs are handled separately by `archive_dir` (Step 1), if enabled.

The Drive write is a **convenience archive, never a gate**: if `create_file` errors or the connector is absent, the digest email has already been sent — just record the failure in the run report and move on. See Failure handling.

## Step 5 — Run report

End every run with a compact report in chat (this is what the scheduled-task transcript shows):

```
SELL-SIDE DIGEST — {date} {time} ET — {LIVE|TEST}
Tickers of interest: WBD, LKSP (reply 5:12 PM ET) | ALL (reply) | none — full digest (no reply)   [omit line when ask_tickers off]
Swept: {n} messages in window ({inbox|inbox + research_folder}) | research notes: {k} unique ({d} duplicate copies collapsed)

TICKER  NOTES  ACTION
WBD     2      replied-all on "Re: WBD spread math" — renamed to INTERNAL WBD (2 PDFs attached) — Drive Doc saved
LKSP    1      created INTERNAL LKSP -> Filings@meteoracapital.com — Drive Doc saved
NVDA    1      skipped — already covered in today's earlier digest

Skipped (no ticker): {broker} "{title}" — macro — flagged for follow-up
Skipped (not research): {sender} "{subject}" — conference invite
Out of scope (not in tickers of interest): {n} notes ({tickers})      [scoped runs only]
PDFs: {n} extracted ({m} unreadable — summarized from body)          [omit line when no notes had PDFs]
Links: {n} followed and used | {m} gated/discarded ({provider list})  [omit line when follow_links off or no links seen]
Archived: {n} .eml + {m} PDFs -> {archive_dir}/{YYYY-MM-DD}   [omit line when archiving is off]
Drive: {n} digest Doc(s) -> "Sellside Digest" ({p} skipped, already archived)  [omit line when drive_archive off]
Degraded: {features skipped and why}                          [omit line when none]
```

Send nothing when zero research is found — just report it.

## Failure handling

- Not signed in → stop; print the sign-in step. Never attempt to send through another identity.
- A tool returns "Session expired" → call `sign_out()` then `sign_in()`. `sign_in()` returns a device-code URL + one-time code instantly: print both in the run report and stop there — the browser step needs a human, and an unattended run must never work around it by sending through another identity. The next run (or the user resuming) picks up after they complete sign-in.
- A PDF that won't extract → summarize from the email body/subject and mark the entry "(attachment unreadable — see original email)". Still attach and archive the file — unreadable to a parser ≠ unreadable to the team. Always attempt extraction first.
- A research link that's gated (login/paywall/consent/JS-shell) or blocked by `web_fetch` → non-fatal and expected. Discard that link, fall back to the body/PDF, and tally it on the `Links` line of the run report. Never let a gated link abort a note, and never try to authenticate or route around the wall.
- A rename preview whose recipient set looks wrong → fall back to plain `reply_all_email` on the same message; recipients are computed the same way, but never confirm anything whose preview you haven't re-verified as internal-only.
- A Drive `create_file` failure (or absent connector) → non-fatal; the digest email already went out. Record it in the run report and move on.
- Phase A failed to send, or Phase B finds no ask thread for today → run the full digest and say so in the run report. The ask is a convenience; never let it block or shrink the sweep by accident.