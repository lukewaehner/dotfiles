---
name: relationship-tracker
description: >
  Scan the signed-in user's Outlook for SPAC DEAL conversations and maintain their
  personal SPAC & Public-Markets relationship / outreach tracker. Use this skill
  whenever the user says "refresh my tracker", "scan my email for deals", "update my
  outreach tracker", "who do I need to follow up with", "update the relationship
  tracker", "rebuild my deal tracker from email", or opens/refreshes the SPAC
  relationship tracker artifact. ALSO trigger proactively whenever the user talks
  about keeping track of which sponsors/banks they've spoken to, last-contacted
  dates, or when it's time to reach back out on a deal. This skill reads email,
  decides whether each message is an actionable DEAL email (and drops generic
  bank IPO / market / research blasts), tags each as Bank/Broker vs Sponsor/Target,
  and rebuilds the tracker artifact. Always use this skill for the relationship/
  outreach tracker — do not hand-classify deal emails ad hoc, because consistent
  keep/drop and bank-vs-sponsor rules are the entire point.
---

# SPAC Relationship / Outreach Tracker

This skill keeps one personal tracker of the user's **deal relationships** — the
sponsors, targets, and banks/brokers they are actively working SPAC transactions
with. It reads their Outlook, keeps only the emails that are about a *specific,
actionable deal*, figures out who each email is from (bank vs. sponsor) and what
the next step is, and rebuilds the tracker artifact.

The hard part — and the whole reason this skill exists — is **deciphering**: most
of the inbox is noise (IPO calendars, market color, research, syndicate axes).
The user does **not** want that here; other trackers cover new issues and market
data. This skill is ruthless about keeping only deal correspondence.

## What the tracker is for

One row per SPAC / relationship, capturing: SPAC name + ticker, contact(s) and
their firm, **Bank/Broker vs Sponsor/Target**, last-contacted date, live deal
status, a one-line deal summary, a concrete next step, and a follow-up date so
stale relationships resurface ("time to reach out"). Banks chase us; sponsors we
chase — so the source tag drives follow-up urgency.

## Workflow

1. **Confirm mailbox access.** Use the `email-assistant` plugin. Call `whoami()`;
   if not signed in, run the sign-in flow (`configure` → `sign_in` → show the
   URL+code → `complete_sign_in`). The tracker reads the *signed-in* user's own
   mailbox.
2. **Pull the window.** Default to the last **90 days** unless the user says
   otherwise. Search **both** received mail and **Sent Items** — sent mail is how
   you capture *who the user reached out to* and the real last-contacted date.
   Use `search_emails(after=<ISO date>, folder=...)`, then `read_thread()` on each
   candidate conversation to judge it in context (a one-line reply is meaningless
   without the thread).
3. **Apply the sender exclusions** (Step A). Drop the senders that are never in
   scope before reading bodies — it saves time.
4. **Apply the relevance gate** (Step B). For everything that remains, decide
   KEEP (a specific actionable deal) vs DROP (market/new-issue/research noise).
5. **Classify the source** (Step C): Bank/Broker vs Sponsor/Target.
6. **Extract a row** (Step D) and **cross-check live deal data** with
   `spac-details` (Step E).
7. **Group and merge** (Step F): one row per SPAC; newest contact wins; merge
   notes chronologically.
8. **Rebuild the tracker** (Step G): write the rows JSON and regenerate the
   artifact so the user sees it refreshed.

---

## Step A — Sender exclusions (drop before reading)

Never track these. They are not deal relationships:

- **Internal Meteora mail** — any sender `@meteoracapital.com`. Internal back-and-forth
  (Vik, HR, MC, Jim D, the desk) is not outreach; it's discussion. Skip it.
- **BAMSEC filing alerts** — `notifications@bamsec.com` / anything `@bamsec.com`.
  Filings are handled by the filing pipeline, not here.
- **Pure no-reply / system senders** — calendar, DocuSign, Zoom, newsletters,
  list-servs with `no-reply`/`do-not-reply` addresses (unless the body is clearly
  a specific deal — rare).

Everything else (external people at banks, brokers, sponsors, targets, primes,
law firms acting on a deal) is a *candidate* — but still has to pass the relevance
gate.

## Step B — The relevance gate (KEEP vs DROP)

Ask one question of every candidate thread:

> **Is this about a specific transaction Meteora could act on as a counterparty —
> or is it broadcast market / new-issue information?**

If it's a specific, actionable deal → **KEEP**. If it's broadcast info → **DROP**,
*even if it comes from a relationship we like.* The user explicitly does not want
IPO/market noise in this tracker.

**KEEP — actionable deal signals** (specific to one name, something we could do):
- Financing / structured deals: **FPA / forward purchase**, **bridge**, **term
  sheet / TS**, **SEPA / ELOC / convertible / PIPE** participation, NAV financing.
- SPAC mechanics on a specific vehicle: **reverse / non-redemptions**, extension,
  trust, warrant/rights restructuring, "**wall-cross**" on a named deal,
  share/warrant holiday.
- **Business combination** discussion: BCA/DA, target intro, "would you look at
  this deal", diligence on a specific target.
- A sponsor/target/banker **introducing or advancing a specific opportunity** to us,
  or responding to our outreach on one.
- Scheduling/holding a call *about a specific deal* ("TTW call re [name]",
  "catch-up on [ticker]").

**DROP — broadcast / out-of-scope noise** (other trackers own these):
- IPO **new-issue announcements, pricing blasts, IPO calendars**, "deals of the
  week", allocation/book-build spam.
- Sell-side **research notes**, market commentary, macro, newsletters.
- **Axe lists / runs** and indications not tied to a deal we're working.
- Generic relationship pleasantries with no deal substance (pure "congrats on the
  IPO" with nothing actionable can be logged as a light touch, but never as a deal —
  see edge cases).

**Worked examples**
- Input: Kingswood banker emails "wall-crossing you on QUMS — possible FPA, terms
  attached." → **KEEP** (specific FPA on a named deal). Source: Bank/Broker.
- Input: UBS ECM blasts "This week's SPAC IPO calendar + pricing." → **DROP**
  (broadcast new-issue info; other trackers cover it).
- Input: Sponsor CFO writes "we'd like Meteora to reverse redemptions before the
  meeting." → **KEEP** (specific SPAC mechanic). Source: Sponsor/Target.
- Input: Prime broker sends "morning axes across 40 names." → **DROP** (axe blast,
  not a deal).
- Input: Banker intro: "meet the [Target] team — they're looking at a de-SPAC and
  need a backstop." → **KEEP** (specific opportunity). Source: Bank/Broker.

When genuinely unsure, lean DROP for anything that reads like a list/blast, and
KEEP anything addressed personally about one named deal. Note borderline calls in
the row's notes so the user can correct them.

## Step C — Source classification: Bank/Broker vs Sponsor/Target

Why it matters: **banks/brokers are intermediaries who are incentivized to chase
us** (placement agents, sell-side, prime, ECM) — so the follow-up burden is on
them. **Sponsors/targets are the deal principals** — we have to chase them. The tag
drives follow-up urgency in the tracker, so getting it right is the point.

Use three signals together; don't rely on any one:

1. **Sender domain.**
   - Bank/Broker: investment-bank / broker-dealer / placement-agent domains
     (e.g. kingswood, btig, cantor, ubs, jefferies, maxim, clear street, cohen &
     co, chardan, ladenburg, ep-wealth, b. riley, roth, lucid, etc.).
   - Sponsor/Target: the SPAC's **own entity domain**, the sponsor **fund/family-
     office domain**, or the **operating target's company domain**. These are the
     principals.
2. **Signature / title.**
   - Bank/Broker: "Managing Director / VP, Investment Banking · ECM · Capital
     Markets · Equity Syndicate" at a bank.
   - Sponsor/Target: "CEO / CFO / Chairman / Founder / General Partner" of the SPAC,
     the sponsor entity, or the target company.
3. **Content stance.**
   - Bank/Broker: relays or *pitches* an opportunity — "my client", "we're running
     this process", "happy to introduce", "we can place".
   - Sponsor/Target: speaks as the owner of the deal — "**our** trust / **our**
     shareholders / **our** extension / **our** target / we are the sponsor".

**Tie-breakers**
- A banker emailing about a *specific live deal we're a counterparty to* → KEEP,
  tag **Bank/Broker** (this is exactly the bank email the user *does* want — it's a
  deal, not market noise).
- If the same name involves both a banker and the sponsor, the row's **source is
  whoever we're actually transacting with**; record the other contact in notes.
- Fold a pure operating-company **target** into **Sponsor/Target** (it's still a
  principal, not an intermediary).

Output the tag as one of: `Bank/Broker`, `Sponsor/Target`. (If the user prefers a
three-way split with `Target` separate, honor that — the tracker template accepts
`Sponsor`, `Bank/Broker`, `Target`.)

## Step D — Extract the row

For each KEEP relationship, pull:

- `display` — SPAC name or group (e.g. "LOKV", "Cohen Circle", "Yorkville").
- `ticker` — primary SPAC ticker if identifiable (resolve names → tickers; use
  `spac-details` filters or EDGAR if unsure).
- `contacts` — person name(s) + firm ("Adam Fishman, Richard Hendrix (Live Oak)").
- `type` — from Step C.
- `lastContacted` — the most recent date **the user** sent or received a deal
  message on this name (sent mail counts).
- `nextStep` — concrete and inferred from the thread: "Awaiting term sheet",
  "Reach out re FPA", "Hold TTW call", "Chase sponsor on reverse redemptions".
- `followUp` — a date when to resurface, if the thread implies one ("follow up in
  Dec", "after the new year", "ping in a week" → concrete date). Leave blank if none.
- `notes` — 1–2 line summary of what's happening + any borderline-classification note.

## Step E — Cross-check live deal status

Call `spac-details` (single ticker, or pull `stage:indeal` and `stage:predeal`
lists once and match locally) to attach **stage** (In-Deal / Pre-Deal), **target**,
**deadline**, **bucket**, and **company_name**. This is the authoritative deal
status — prefer it over guessing from the email. If a name shows as liquidating or
the deal is closed, reflect that.

## Step F — Group, merge, dedup

One row per SPAC/relationship. If multiple threads hit the same name: keep the
**latest** contact date, union the contacts, and merge notes newest-first. Don't
let one ticker appear twice.

## Step G — Rebuild the tracker artifact

1. Assemble the rows into the seed schema (see `references/row-schema.md`).
2. Run `scripts/build_tracker.py rows.json out.html` to inject the rows into the
   bundled `assets/tracker_template.html`.
3. Refresh the artifact: if a `spac-relationship-tracker` artifact already exists,
   `update_artifact` with the new HTML; otherwise `create_artifact`. List
   `mcp__<meteora-server>__spac-details` in `mcp_tools` so the artifact's live
   "Refresh deal status" button keeps working.
4. Preserve the user's manual edits where you can: the artifact stores per-row
   edits (type / next step / follow-up / notes) in browser localStorage keyed by
   row id, so keep row ids stable across rebuilds (derive id from ticker/name).

**Encoding safety for Step G:** `build_tracker.py` already uses `encoding='utf-8'`
on all file I/O. Do not modify it to remove those arguments. If you ever write a
replacement script or inline the template injection, the same rule applies: always
pass `encoding='utf-8'` to every `open()` call on Windows. Without it, Python
inherits the system code page (cp1252), which silently corrupts non-ASCII characters
(`·`, `→`, `…`, etc.) into mojibake sequences (`Â·`, `â†'`).

## Edge cases

- **Light touches** ("congrats on the IPO", "let's grab a beer") with no deal
  substance: log as a row only if there's an ongoing relationship, mark next step
  "relationship touch — no live deal", and don't flag it as urgent.
- **No ticker yet** (private target, brand-new sponsor): keep the row, leave ticker
  blank, status "Unknown", note the firm.
- **Ambiguous bank-vs-sponsor**: pick the better guess, and say so in notes so the
  user can flip it in one click.
- **Nothing new**: if no KEEP emails since the last run, say so and leave the
  tracker unchanged rather than rewriting it.

Keep the bias clear: when in doubt about *relevance*, drop noise; when in doubt
about *source*, label and annotate so the user can correct fast.
