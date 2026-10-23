---
name: bamsec-filing-handler
description: 'Process BAMSEC SEC filing alerts that hit filings@meteoracapital.com: parse the alert, filter to SPAC 8-Ks via EDGAR name→ticker→spac-details, pull the 8-K from EDGAR, run the Meteora 8-K analysis prompt, append a tagged entry to the ticker''s memory doc, and reply from walter@meteoracapital.com back into filings@ — threaded on the original BAMSEC conversation so the investment team sees alert and analysis together in the shared inbox. Supports two input modes: manual paste of the alert (Mode A) and Microsoft 365 outlook_email_search (Mode B — reads forwarded copies from the logged-in user''s inbox today, swaps to filings@ via delegated access on Walter). Trigger when the user pastes a BAMSEC alert, mentions BAMSEC or the filings@ inbox, or asks to "process BAMSEC alerts", "run the filing handler", "analyze this 8-K", "check the filings inbox", "process the morning filings", "catch up on overnight filings", or "triage the filings inbox". Always use this skill for BAMSEC alert handling — do not do this ad hoc.'
---

# BAMSEC Filing Handler

End-to-end automation for converting BAMSEC SEC filing alerts at filings@meteoracapital.com into Meteora-format trading notes. The handler reads the alert, pulls the underlying filing from EDGAR, runs the Meteora analysis prompt, updates the ticker's memory doc, and sends the analysis as a reply on the BAMSEC thread that lands back in filings@meteoracapital.com — the shared inbox the entire investment team has access to. Original alert and Meteora analysis sit threaded together in one place, visible to everyone.

Goal: cut the human review of an 8-K from ~5 minutes (open BAMSEC → click through to EDGAR → read filing → write up the implication) down to ~30 seconds (read the analysis email, make the trade call). Across 10 names a day that's an hour back.

## How to invoke (two modes)

This skill supports two input modes. The downstream steps (parse, gate, fetch, analyze, memory, reply) are identical in both.

### Mode A — Manual paste (test mode, current default)

The user pastes a BAMSEC alert email — subject + body — directly into the Cowork conversation. The skill starts at Step 2. This mode exists because Walter's read-email-as-MCP-tool is not yet shipped; until it is, manual paste is the only way to feed alerts in.

Trigger when the user pastes content containing `[BamSEC]` in the subject, or explicitly says *"run the handler on this"* / *"analyze this alert"* with email content attached.

### Mode B — Inbox search (Microsoft 365 connector)

The skill uses `Microsoft 365:outlook_email_search` + `Microsoft 365:read_resource` to pull BAMSEC alerts from the connected mailbox, then processes each one through Steps 2–9. Available now — no Walter-auth MCP read tool needed.

**Where it reads from depends on which Claude account triggers it:**
- **Lukas (test/dev today):** reads Lukas's own inbox. Luke set up a forwarding rule from filings@ to the AI_Interns distribution group, so Lukas's inbox already has forwarded copies of every BAMSEC alert. The forwarded subject is `FW: [BamSEC] ...` from `lgries@meteoracapital.com`, with the original alert quoted inline in the body.
- **Walter (production eventually):** reads filings@ directly via `mailboxOwnerEmail="filings@meteoracapital.com"` if Walter has delegated access. Or, once Henry ships a dedicated Walter-auth read tool on Meteora MCP, swap to that — one-line change in Step 1.

Trigger when the user says *"process BAMSEC alerts"*, *"check the filings inbox"*, *"catch up on overnight filings"*, *"run the morning handler"*, etc.

**Important caveat for test mode:** when reading forwarded copies from Lukas's inbox, the conversation-id Outlook returns is for Luke's forward chain, NOT for the original BAMSEC thread in filings@. So a Step 7 reply threaded on that conversation-id would land in the AI_Interns thread, not in the filings@ BAMSEC thread. For test runs, this is acceptable — combine with dry-run for Step 7 to avoid stray email. For production, threading needs the real filings@ conversation-id, which requires either delegated access (Walter) or the Meteora MCP read-email tool.

## Scope (v1 — locked)

- **Source inbox:** filings@meteoracapital.com (production mode only)
- **Sender filter:** `notifications@bamsec.com` (confirmed)
- **Filing type:** SPAC 8-Ks only. Everything else is flagged for manual review but NOT processed.
- **Universe filter:** SPACs only. The BAMSEC watchlist is NOT SPAC-curated — it contains a mix of SPACs, deSPACs, and other names. Every alert MUST be filtered via the SPAC universe check (see Step 3).
- **From:** walter@meteoracapital.com (default for `send-email` — hardcoded at the MCP tool level)
- **To:** filings@meteoracapital.com (same shared inbox the original BAMSEC alert hit)
- **Thread:** reply on the original BAMSEC conversation so the analysis nests under the alert in Outlook

Future versions will add 425s, S-4s, then redline S-4s (per Adis's build order). Do not expand scope unilaterally.

## Workflow

### Step 1 — Get the BAMSEC alert(s) [mode-dependent]

**Mode A (current):** User pastes the alert. Skip the inbox search. Capture:
- Subject line
- Body text (including the company name, View Filing URL, exhibit list)
- Original sender (should be `notifications@bamsec.com` — if not, flag and ask the user to confirm)
- Date the alert was sent
- The full conversation thread ID, if the user provides it (needed for threaded reply in Step 7 — if not provided, send as a new email to filings@ rather than threaded, and flag in run summary)

**Mode B (available now):** Call `Microsoft 365:outlook_email_search`. Two-step fetch — search returns metadata only, then `read_resource` for the body.

1. **Search.** Call `outlook_email_search` with:
   - `query="[BamSEC]"` — matches BAMSEC subjects (both direct `[BamSEC]` and forwarded `FW: [BamSEC]`)
   - `afterDateTime` — set from user input (default: `"yesterday"` for a morning catch-up; accepts natural language)
   - `limit=25` — max per page; paginate via `nextCursor`/`nextOffset` if more
   - `mailboxOwnerEmail="filings@meteoracapital.com"` — **only set this** when running on Walter Claude with delegated filings@ access. **OMIT this on Lukas** (reads Lukas's own inbox, which has the AI_Interns-forwarded copies).

2. **Read bodies.** For each result, call `read_resource` with `uri=mail:///messages/{messageId}` to get the full body. The body contains the View Filing link, exhibits list, and (for forwarded copies) the original BAMSEC content quoted inline.

3. **Capture per alert:**
   - `messageId` and `conversationId` (for threading in Step 7 — note caveat about forwarded-copy conv-ids landing in AI_Interns rather than filings@)
   - `subject` (strip `FW: ` prefix if present for cleaner downstream parsing)
   - `sender` (`notifications@bamsec.com` for direct alerts in filings@; `lgries@meteoracapital.com` or similar for forwarded copies)
   - `receivedDateTime`
   - `body` (full text from `read_resource`)

If zero results, say so plainly and stop. Do not proceed with empty alerts.

### Step 2 — Parse each alert

BAMSEC subjects follow the format `[BamSEC] {Company Name} {filing description}`. Extract:

- **Company name** — e.g., "JFB Construction Holdings", "Marti Technologies Inc.", "Sagaliam Acquisition Corp."
- **Filing/notification type** — see categorization below
- **Body content** — pull the View Filing URL (used to retrieve the EDGAR accession in Step 4)

**Filing/notification categorization** (gate at Step 2.5 before any EDGAR work):

- `8-K` (or `Form 8-K`) → **process** (v1 scope)
- `Form 425` → skip — "425, not in v1 scope (planned for v2)"
- `Form S-4`, `F-4`, `S-4/A`, `F-4/A` → skip — "S-4, not in v1 scope (planned for v3)"
- `10-K`, `10-Q`, `20-F`, `6-K`, `DEF 14A`, `PRE 14A`, `SC 13D`, `SC 13G`, etc. → skip — "{form type}, not in v1 scope"
- "new transcript available" / "transcript" → skip — "BAMSEC transcript notification, not a SEC filing"
- "new filings index" / "watchlist update" / non-filing BAMSEC service emails → skip — "BAMSEC service notification, not a filing alert"
- Subject doesn't match any known BAMSEC pattern → "parse failure — manual review"

If the subject says "8-K" or "Form 8-K," proceed to Step 3. Everything else falls into the skip bucket above. The reason field matters — clean run summaries let the user see at a glance why each alert was passed over.

### Step 3 — SPAC universe gate

The BAMSEC watchlist is NOT curated to SPACs. Every 8-K alert must be filtered against Meteora's SPAC universe via three cheap calls.

**3a. Company name → ticker via EDGAR static mapping.**
EDGAR publishes a static `company_tickers.json` at `https://www.sec.gov/files/company_tickers.json` that maps every public company name and ticker symbol to its CIK. Use `web_fetch` once per run (results can be reused across alerts in the same run). The mapping is keyed on a normalized name — strip "Inc.", "Corp.", "Ltd.", "Holdings", punctuation, and case before matching.

If the company name resolves to exactly one ticker → use it.
If it resolves to multiple tickers → take the one whose `cik_str` matches the registrant CIK in the EDGAR filing index (Step 4 short-circuit), or flag for manual review.
If no match → skip with reason "EDGAR name resolution failed — manual review."

**3b. Ticker → `spac-details`.**
Call `Meteora MCP:spac-details` with the resolved ticker. If the tool returns SPAC data → in universe. If it returns "not found" or equivalent → skip with reason "not a SPAC in Meteora universe."

**3c. Capture stage from `spac-details`.**
The `stage` field (`predeal` or `indeal`) determines which lens the 8-K analysis prompt uses in Step 5. Save it.

If both 3a and 3b succeed, proceed to Step 4. Otherwise skip and record the reason.

### Step 4 — Pull the 8-K from EDGAR

Use the CIK-based lookup as the primary path. We already have the ticker and CIK from Step 3a, and `edgar-filings` returns authoritative filing data directly from EDGAR — more robust than parsing the BAMSEC "View Filing" URL (which is a BAMSEC redirect URL, not a direct SEC.gov link, and may not survive the email paste anyway).

**4a. Locate the accession number via `edgar-filings`.**
Call `Meteora MCP:edgar-filings(ticker="[TICKER]", form_type="8-K", limit=5)`. Match the filing whose filing date is on or within 1 calendar day of the BAMSEC alert's received date (alerts can lag the filing by a few hours, especially overnight). Capture that filing's accession number.

If multiple 8-Ks were filed by the same registrant on the same day (rare but possible — e.g., one for an extension vote, another for a deal amendment), use the most recent one whose subject categorization matches the BAMSEC body description. If still ambiguous, take the most recently filed and note in the run summary.

If no 8-K matches within the date window, skip with reason "EDGAR filing not located — accession lookup failed."

**4b. Pull the 8-K text.**
Call `Meteora MCP:edgar-filing-text` with the accession number from 4a.

**4c. Pull material exhibits.**
If the 8-K references exhibits material to the event (attached extension agreement, PIPE subscription, NRA, BCA, press release with management quotes), call `Meteora MCP:edgar-filing-index` to enumerate exhibits, then `edgar-filing-text` on each material one. The analysis prompt in Step 5 indicates which exhibits matter for which event types.

**4d. (Optional shortcut.) URL parsing fallback.**
If the pasted alert content includes a direct SEC.gov URL (pattern: `sec.gov/Archives/edgar/data/{CIK}/{accession}/...`), the accession number is parseable from the path — use that as a shortcut to skip 4a. Do NOT attempt to follow `bamsec.com` URLs; they're redirect URLs and the MCP can't follow redirects.

### Step 5 — Run the 8-K analysis prompt

Use the prompt below verbatim. Pass the filing text, the company name + ticker, the stage from Step 3c, and any pulled exhibits.

---

#### SPAC 8-K Analysis Prompt

You are analyzing a SPAC 8-K for Meteora Capital's investment team. Output goes as a reply on the BAMSEC alert thread in filings@meteoracapital.com — read by traders in ~30 seconds to make a position decision.

The reader has the position data, current yields, working orders, and a memory-doc-derived thesis available in parallel from the trading-note skills. **Your job is to explain what changed in this filing and what it means for the position** — not to restate position data, not to write a generic SPAC summary.

##### Voice and calibration (non-negotiable)

- Walter-facing: colleague who just opened the filing. Terse, concrete, directional. No marketing language.
- **Preserve the filing's calibration.** If the 8-K says "expected to close in Q3," the analysis says "expected to close in Q3" — not "will close in Q3." Hedge stays on the verb, not the number.
- **Specificity test**: if a sentence could appear verbatim on another SPAC's 8-K analysis, it's too generic. Anchor every claim to specific facts of this filing.
- **Exact thresholds**: pull exact numbers from the filing. "$0.025/sh extension deposit, monthly, capped at $375K total" — not "small monthly deposit."

##### Stage-bifurcated reading

Use the stage passed in (`predeal` or `indeal`). Read the 8-K through the lens of where the SPAC sits.

**Pre-deal 8-K lens:**
- Is this a sponsor activity signal? (extension deposit terms, director changes, mandate refinement)
- Does this change the structural read? (trust top-up, founder share forfeit, fee modification)
- Does this materially shift the deal-find timeline?
- Does our posture change? (build common, work warrants/rights, FPA-origination posture)

**In-deal 8-K lens:**
- Does this change the closing probability? (PIPE add/drop, NRA, FPA, deal amendment, target swap)
- What does it tell us about sponsor incentive? (sponsor capital committed, deferred UW math, founder share economics)
- What's the process/timeline read? (vote dates set, S-4 effectiveness, regulatory clearances, outside date pressure)
- Does our posture change? (hold/add/trim, sell-rights-into-pop, redeem-at-vote)

##### Common SPAC 8-K event types

- Extension meeting result (redemptions, sponsor deposit, new deadline)
- Deal announcement (LOI / BCA / definitive agreement)
- Deal amendment (revised terms, valuation cut, structure change, target swap)
- Deal termination (BCA killed — trust mechanics for remaining holders)
- PIPE announcement / PIPE add / PIPE drop
- Non-redemption agreement (NRA)
- Forward purchase agreement (FPA) / backstop
- Vote results — extension, deal, or other shareholder matter
- Director / officer change
- deSPAC close (final redemptions, trust at close, new ticker)
- Trust deposit / withdrawal (sponsor extension contributions)
- Reference to S-4 / F-4 / 425 / proxy filing — note status
- Material press release content (use management quotes only if they signal conviction, risk, or direction — skip boilerplate)

##### Output format

Fenced code block. Tight. ~150 words max. Format mirrors the trading-note structure for visual consistency.

```
[TICKER] — 8-K — [event in plain English, 4–6 words]

Event: [1–2 sentences. What was filed, including Item number(s). Preserve filing-language calibration.]

Key facts:
- [Exact-threshold bullet: dates, dollar amounts, share counts, counterparties]
- [Another exact-threshold bullet]
- [3–5 bullets total — omit slots the filing doesn't speak to]

Trust / Deadline: [Current trust per share, current deadline, delta vs. prior if changed. "—" if unchanged.]

S-4 / F-4: [Status if mentioned or implied — filed / amended / effective / not yet filed]

Management read: [1 sentence with attribution IF there's a quote worth flagging. Omit line if quotes are boilerplate.]

Trade implication: [1–2 sentences. Stage-appropriate lens. Tie to closing probability, sponsor incentive, process timeline, or posture impact. No generic SPAC commentary.]

Recommended action: [Hold / Add / Trim / Flag for review] — [1-line why, anchored to a specific threshold from the doc or filing where possible]
```

Followed by a separate line outside the code block:

`Source: [EDGAR accession + URL]`

##### Forbidden moves

- **Don't restate header data** — positions, current yields, working orders, sponsor identity, UW. The trading note carries this.
- **Don't strip the filing's hedging** — "deal expected to close" stays "expected to close."
- **Don't synthesize from forbidden sources** — sheet notes, sheet recommendation, first-principles reasoning. Only the filing itself and `spac-details` data may inform the analysis.
- **Don't pad** — drop a slot if the filing doesn't speak to it. Better a 4-line key-facts block than a 6-line one padded with generics.
- **Don't be generic about action** — "Flag for review" with no reason is empty. Always anchor to a specific threshold or trigger.

---

### Step 6 — Update the memory doc (required, not optional)

Updating memory is a hard requirement of every successful run, not a side-effect. Every processed filing MUST land an entry in the ticker's memory doc — that's the audit trail and the input to future trading-note Thesis blocks.

1. Call `Meteora MCP:list-memory-docs` and find the doc for this ticker.
2. **If doc exists:** call `Meteora MCP:update-memory-doc` to append a new tagged entry. Tags include `#8-K` plus event-specific tags (`#extension`, `#deal-announcement`, `#PIPE`, `#NRA`, `#vote-results`, `#sponsor-change`, `#deal-termination`, `#deSPAC-close`, etc.). Entry body = the analysis from Step 5, plus the accession number and the date of the alert for traceability. The entry should be distillable into a future Thesis — active voice, exact thresholds, calibration intact.
3. **If doc does NOT exist:** do NOT auto-create it. Add the ticker to the skip-summary list with reason "no memory doc — run seed-memory first." Spurious cross-batch connections from auto-seeding without isolated context have burned us before — always seed memory in a dedicated conversation via the `seed-memory` skill, never as a side-effect of the filing handler.

### Step 7 — Reply on the BAMSEC thread, back into filings@

Call `Meteora MCP:send-email`:
- **From:** walter@meteoracapital.com (default — hardcoded at the MCP tool level)
- **To:** filings@meteoracapital.com (same as the source inbox — the analysis lands back in the shared inbox the team already monitors)
- **In-reply-to / conversation-id:** the original BAMSEC alert's conversation-id from Step 1, so the analysis threads under the alert in Outlook rather than appearing as a detached new message
- **Subject:** `Re: [original BAMSEC subject] — Meteora analysis`
- **Body:** the trading-note output from Step 5, followed by a footer line with the EDGAR URL and accession number

Mode A (manual paste): if the user couldn't supply a conversation-id, send as a new email rather than threaded, and flag in the run summary.

### Step 8 — Idempotency check (before sending)

Before sending in Step 7, check the ticker's memory doc for an existing entry containing the same accession number. If found, do NOT re-send the analysis email — add to the skip list with reason "already processed in prior run." This prevents duplicate emails if the handler is re-run on overlapping time windows.

### Step 9 — Final summary to the user

After the batch (or the single alert in Mode A) finishes, post one summary block in chat:

```
BAMSEC handler run — [date / time window / single-alert label]
Mode: [A: paste | B: inbox search]

Processed (N):
- [TICKER1] — 8-K [event type] — replied + memory updated
- [TICKER2] — 8-K [event type] — replied + memory updated

Skipped (N):
- [Company] — 425, not in v1 scope (planned for v2)
- [Company] — BAMSEC transcript notification, not a SEC filing
- [Company] — not a SPAC in Meteora universe
- [Company] — no memory doc, run seed-memory first
- [TICKER] — already processed (prior run)

Parse failures (N):
- [subject line snippet] — couldn't extract company name / filing type
```

## Tools used

| Step | Tool |
|---|---|
| 1 (Mode B) | `Microsoft 365:outlook_email_search`, `Microsoft 365:read_resource` |
| 2 | inline parsing |
| 3a | `web_fetch` on EDGAR `company_tickers.json` |
| 3b | `Meteora MCP:spac-details` |
| 4 | `Meteora MCP:edgar-filings`, `Meteora MCP:edgar-filing-text`, `Meteora MCP:edgar-filing-index` |
| 5 | inline LLM analysis (Adis's 8-K prompt above) |
| 6 | `Meteora MCP:list-memory-docs`, `Meteora MCP:read-memory-doc`, `Meteora MCP:update-memory-doc` |
| 7 | `Meteora MCP:send-email` |

## Failure modes & guardrails

- **No inbox access (Mode B):** if the read tool errors, surface the connector status to the user and stop — do not silently return "0 alerts found."
- **Cross-batch contamination:** when updating memory docs for multiple tickers in one run, treat every `update-memory-doc` call as fully isolated. Never let analysis of TICKER1 leak into TICKER2's entry. The prior failure mode produced spurious "this is the only NYSE name in the batch"-style connections.
- **Duplicate sends:** Step 8's idempotency check is mandatory, not optional. The same BAMSEC alert can surface twice if time windows overlap.
- **Send failures:** if `send-email` fails (auth, network, recipient rejection), do NOT log the entry to the memory doc. The memory doc is the source of truth for "this filing has been triaged" — if the email didn't go out, the work isn't done.
- **Thread linkage:** if `send-email` can't preserve the conversation-id, still send the email but flag in the chat summary that thread linkage failed — the analysis is in the inbox, just not nested. Don't block the run on it.
- **EDGAR name resolution ambiguity:** if a company name resolves to multiple CIKs and the EDGAR filing's registrant CIK doesn't disambiguate cleanly, skip with reason rather than guessing. Better to manually review one than to mis-tag the analysis to the wrong ticker.
- **Non-8-K SPAC filings:** flag, don't process. Future versions add these in Adis's order: 425s, S-4s, redline S-4s.

## Why this skill exists (context)

Adis's stated goal: turn the morning BAMSEC review from a 5-minute-per-filing manual process into a 30-second email read. The skill exists because every atomic piece already lives in the Meteora MCP — `send-email`, `edgar-filing-text`, `update-memory-doc`, `spac-details` — but nothing was tying them into the end-to-end workflow. This skill is that glue.

The two-mode design (paste-first, inbox-search-later) is the dev's call: validate the analysis/memory/reply pipeline manually before Henry wires up the read-email-as-Walter MCP tool. Once the pipeline is proven on real BAMSEC alerts, swapping in the read tool is a one-line change to Step 1.

Parallel project: Luke and Lee are building a Python listener on filings@ that performs the same workflow as a continuous daemon. The Cowork skill is the on-demand version. Both converge on identical output — a threaded reply on the BAMSEC alert plus a memory doc update.
