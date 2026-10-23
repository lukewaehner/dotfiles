---
name: meteora-alphasense-pipeline
description: End-to-end AlphaSense research-INGESTION pipeline for Meteora. Each weekday morning it turns AlphaSense's own AI output (scheduled GenSearch Agents delivered by email) plus email alerts into (1) raw broker-research + expert-insight PDFs archived locally and (2) one consolidated team-ready Broker Research email (a section per sector) that simply RELAYS AlphaSense's own broker syntheses plus each alert's doc counts and download status. This is an INGESTION tool ONLY: it does NOT analyze, does NOT cross-reference against Meteora's memory docs / positions / internal threads / VDR, and adds NO thesis, call, or opinion. NO API and NO scraping for the reader: it drives the user's already-logged-in AlphaSense browser session (Chrome MCP) only to download PDFs and log in. Trigger on "run the AlphaSense pipeline", "pull today's broker research / expert calls", "AlphaSense morning digest", "ingest today's AlphaSense research", or on its scheduled morning run.
---

# Meteora AlphaSense Research-Ingestion Pipeline

**This is an ingestion tool.** Its whole job is to (a) archive the raw broker-research and expert-insight PDFs locally and
(b) deliver AlphaSense's OWN broker syntheses (the Agent "Weekdays Update" reports) to the team as
ONE consolidated Broker Research email (a section per sector under its own header; sectors with no material new broker research are omitted), plus a small ingestion tally (how many docs the alert flagged, how many were
in-scope, how many were downloaded). It does **not** analyze those summaries against Meteora's book, and
it never adds a thesis, a call, or an opinion. Keeping it lean is the point: the analysis lives in the
other Meteora skills, not here.

## 1. Goal & the daily clock
By ~**8 AM ET each weekday**, deliver ONE consolidated team-ready Broker Research email — a **section per sector** — that **relay what's new in the broker research (as AlphaSense's own syntheses)**, while **archiving the raw broker-research + expert-insight PDFs locally**
for the vector DB.

- **5:00-7:00 AM ET** - scheduled **GenSearch Agents** run server-side. Their synthesis is now delivered
  **by email** (the "<Sector> - Broker Research Daily: Weekdays Update" alerts) in addition to staying
  in-platform.
- **7:00 AM ET** - the alert emails land: broker "Documents Only" alerts (download triggers) and the
  agent "Weekdays Update" broker syntheses.
- **7:00-8:00 AM ET** - this pipeline runs: read the agent syntheses (from email)
  + download the alert-triggered PDFs -> **relay the broker syntheses into ONE consolidated email — a section per sector** (no analysis).

## 2. Division of labor
- **AlphaSense discovers** what's new (email alerts).
- **AlphaSense summarizes** the content - scheduled **Agents** (broker synthesis, emailed as "Weekdays
  Update"). Heavy inference, ~zero Claude cost.
- **Claude INGESTS**: it downloads/archives the raw PDFs and **relays** AlphaSense's summaries into
  ONE consolidated team email (a section per sector; sectors with no material new broker research omitted) with a per-sector ingestion tally. This is the only Claude-token step, and it is
  deliberately mechanical - **no cross-referencing against our book, no thesis, no call, no opinion**
  (see `assets/fusion_email_template.md`).
- **Raw broker-research AND expert-insight PDFs** are downloaded and archived locally (later: ingested to the Pinecone VDR). Expert-insight call transcripts are valuable primary research and are archived, never dropped.

Because the Agent synthesis is now emailed, **Chrome is no longer needed to READ agent reports**. Chrome
is still needed only to (a) log in / session-check and (b) **DOWNLOAD the raw broker-research + expert-insight PDFs** (the email
carries `docid` deep-links, but the PDF itself is generated on-demand behind bot protection - no
API/email path to the file). If local PDF archiving is ever dropped, Chrome can be dropped entirely.

## 3. Hard constraints
- **No API, no scraping** for the reader/PDF. Drive the real logged-in browser only, and only for
  downloads + login.
- **Scheduled-agent cap = 10.**
- **News is OUT OF SCOPE.** Broker-research only — do NOT read, parse, or relay any "Daily News" AI-summary alerts. News reporting is handled by the separate Meteora sector-brief skill.
- **Multi-browser.** Select the **LOCAL** connected browser (`isLocal = true`, macOS). Do NOT hard-code a
  deviceId — the display label may drift (Browser 1 / Browser 2) and the offline original host appears as a
  non-local (Windows) browser. Always select by `isLocal = true`. If a non-local browser connects mid-run and
  deselects the session, RE-SELECT the isLocal macOS browser and continue — on an unattended scheduled run do
  NOT stop to ask which browser to use (there is standing authorization to use the isLocal browser).
- **Session expiry -> click "Log in"** (org SSO auto-authenticates). Only STOP + notify if it demands a
  typed password or captcha (never type credentials or solve captchas).

## 4. Inventory
See `references/alert-inventory.md`. In brief: 10 scheduled **Agents** (emailed "Weekdays Update"
syntheses) and 10 broker **"Documents Only"** alerts (download triggers). (No news alerts — broker research only.)
Scope keywords/tickers live in `ingestion_scope.json` (+ `spac_universe.txt`) - read them there, never
hard-code. Here, the scope list is only a **download filter** (decide which flagged PDFs are worth
archiving); it is not an analysis hook.

**ALERT-SOURCE HYGIENE:** an alert's "N new docs" count reflects whatever **sources** the alert is set
to. If an alert has **Intellectual Property (patents)** or **News** enabled as a source it floods - e.g.
Space / Satellite pulled ~700 semis/telecom patents (Samsung, Apple, Qualcomm) in one run, and its
"Broker Research News" variant repeatedly hits the 100-doc cap on general-news items. Broker alerts
should be scoped to **Broker Research + Expert Insights** (both are wanted primary research — expert-insight call transcripts must NOT be dropped), with **Intellectual Property (patents)** and **News** kept **OFF**. If a scope comes in flooded, note it in the email and
down-scope to the genuine broker-research + expert-insight docs rather than downloading patent/news noise.

## 5. The daily run
> **TEST MODE:** emails are **DRAFTS ONLY**, recipient = the **signed-in user (self)**, `[TEST]` subject
> prefix, no VDR writes. Do not send.

**Step 0 - Browser.** Load the Chrome MCP toolset, select the LOCAL (`isLocal=true`) browser, open `research.alpha-sense.com`. If
logged out, click **Log in** (auto-SSO). (Only needed for downloads/login now.)

**Step 1 - Read alert emails.** Email Assistant `whoami` (expect `chauhan_intern@`). `search_emails`
sender `info@alpha-sense.com`, today, newest first. Route each by subject prefix -> scope + type
(`references/alert-inventory.md`). **Exporting the alerts as `.eml` and parsing them** is the reliable
way to get BOTH the full untruncated summary text AND the per-doc **`documentId` deep-links** (the reader
strips them from the on-screen view; docids may be `SSRFS-...` OR other prefixes such as `ASR-CNTR-...`,
so match any `documentId=<ID>&...&category=main_doc`). From each broker "Documents Only" email, extract
the new docs + their `documentId`; dedup against `BrokerResearch/_state_seen.json`. Parse the agent
"Weekdays Update" broker syntheses from their emails. Ignore any "Daily News" AI-summary alerts — news is out of scope.

**Step 2 - Download raw broker PDFs.** For each new **in-scope** broker-research OR expert-insight doc: open
`research.alpha-sense.com/search?docid=<DOCID>`, click **Download**, then **wait for the "GENERATING
DOWNLOAD..." state to fully clear** (a "Cancel" button in the reader = generation still in progress; for
a large PDF this can take 20-40s - keep waiting and re-check `C:\Users\rishi\Downloads` until the
`YYYYMMDD - Firm - Title - N pages.pdf` file appears, rather than assuming failure early). Then archive
with `scripts/archive_pdf.py` (`--slug/--root/--downloads/--docid --newest`). Download the genuine
in-scope broker research AND expert insights (Expert Insights carry `EC-` docids and are primary expert-network research — download + archive them, do NOT skip; still skip off-scope EM round-ups, patent noise, and general-news items); the Broker
Research email states how many were flagged, how many in-scope, and how many downloaded. Caps: 25/alert,
60/run (Expert Insights count toward these caps — on a heavy expert-insight day they will bind; note it in the email and prioritise the most on-theme docs). Idempotent via `_state_seen.json`. ("In-scope" for BROKER RESEARCH means: does the doc's primary ticker /
coverage map to a name in `ingestion_scope.json`. For EXPERT INSIGHTS (`EC-` docids): the sector alert has already scoped them to the sector, so treat an expert-insight doc surfaced in a sector alert as in-scope by default — dedup, and skip only obvious cross-sector noise. A download filter, nothing more. Watch ticker aliases — a name can surface under more than one ticker (e.g. EchoStar = SATS and ECHO); match the entity, not just the literal string, so an in-scope name isn't dropped as off-scope.)

**Step 3 - Read the agent syntheses.** Read each scope's Agent **"Weekdays Update" email** (this replaces
driving Chrome `/gensearch` - the synthesis is now emailed). Save each verbatim-in-substance to
`BrokerResearch/<slug>/<YYYY-MM>/_GenSearch_<slug>_<date>.md`. Only if an agent email is missing/failed,
run the GenSearch prompt live via Chrome (`references/gensearch-prompts.md`, `references/browser-mechanics.md`).

**Step 4 - Assemble + draft the email (relay only).** Produce, per the templates in
`assets/fusion_email_template.md`, **ONE consolidated Broker Research email** with a **section per sector**
(each sector = one Desk-memo card under its own sector header) and a **single shared footer** at the bottom
(do not repeat the footer per section). Subject `AlphaSense AM - Broker Research - <Mon D>` (one email; no
per-sector suffix). Send via `draft_email` then `send_email` (confirmed) with an identical body:
- each sector section = the **Agent "Weekdays Update" synthesis** for that scope (each firm's own thesis +
  issuance/deal implication, taken in substance from the synthesis or a downloaded deal-terms PDF) + the
  ingestion tally (**flagged / in-scope / downloaded**) + that sector's download ledger (list downloaded
  broker-research PDFs and downloaded expert-insight transcripts separately).
- **Omit empty sectors:** include a section only for sectors with material new broker research; omit any
  sector whose synthesis reports no material new broker research, and omit the individual-ticker SPAC
  watchlist when it has only an off-theme match / no synthesis. Omitting a sector from the email does NOT
  narrow the download/archive scope in Step 2 — all in-scope broker + expert docs are still archived.

**Download-reconciliation (mandatory — if it's good enough to summarise, it's good enough to archive).** Every broker report NAMED in the relayed synthesis must have a matching downloaded PDF. Before finalising a Broker Research email, list the reports it names (firm + title) and cross-check them against the download ledger. For any named report NOT already downloaded from an alert doc, find it live in AlphaSense — search the company (mind ticker aliases, e.g. EchoStar = SATS and ECHO), filter to Broker Research, match the firm/analyst — and download it. If a named report genuinely cannot be located, do NOT silently drop it: flag it in the ledger as `NOT DOWNLOADED - needs manual pull: <firm> - <title>`. The Agent synthesis (GenSearch) can cite reports that never appear in the "Documents Only" download alerts, so this reconciliation is the only thing that catches them.

Do **NOT** pull `spac-details`, `list-memory-docs` / `read-memory-doc`, the `Internal <TICKER>` Outlook
thread, or `semantic-search`/VDR, and do **NOT** add any Meteora-specific commentary. The email carries
AlphaSense's own summary content and the ingestion counts - nothing about our positions, theses, or
book. (The report-summary sentences are the *report's* content as AlphaSense stated it,