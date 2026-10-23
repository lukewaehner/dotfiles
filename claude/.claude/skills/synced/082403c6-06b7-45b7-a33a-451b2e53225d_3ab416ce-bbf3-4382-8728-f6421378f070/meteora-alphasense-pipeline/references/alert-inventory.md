# Agent & alert inventory + routing

Two things run in AlphaSense for this (broker-research-only) pipeline: **scheduled Agents** (broker
synthesis, emailed) and **broker alerts** (download triggers, emailed). News alerts are RETIRED — news is out of scope. Email subject line =
the saved alert name, `"<Alert Name> : Daily Summary - <Mon DD, YYYY>"`, sender `info@alpha-sense.com`.
Match the subject prefix to the slug. Slugs match `BrokerResearch/<slug>/` and `ingestion_scope.json`.

## A. Scheduled GenSearch Agents (in-platform synthesis)
Weekdays (M-F), **5:00-7:00 AM ET**, "Limit documents to past 24hrs" ON, Broker Research, output = Report.
These do the sector synthesis; the pipeline reads each agent's latest thread via Chrome. Cap: **10 agents**.

| Agent title | slug | status |
|---|---|---|
| Nuclear Energy - Broker Research Daily | `nuclear-energy` | [x] created + validated |
| Crypto / Stablecoins - Broker Research Daily | `crypto-stablecoins` | [x] created |
| Software / Cyber / Networking - Broker Research Daily | `software-cyber-networking` | [x] created |
| Healthcare / Pharma - Broker Research Daily | `healthcare-pharma` | [x] created |
| Consumer Discretionary / QSR - Broker Research Daily | `consumer-disc-qsr` | [x] created |
| Autonomous Trucking - Broker Research Daily | `autonomous-trucking` | [x] created |
| Macro - Rates & Credit (HYG) - Broker Research Daily | `macro-rates-credit` | [x] created |
| Macro - SPAC / IPO Issuance - Broker Research Daily | `macro-spac-ipo` | [x] created |
| SPAC Sector - Broker Research Daily | `spac-sector` | [x] created |

Creation recipe: `browser-mechanics.md` Sec 5. Instruction prompts: `gensearch-prompts.md`.

## B. Broker Research alerts -> DOWNLOAD raw PDFs (Documents Only, Daily 7 AM)
Their only job now is to notify which new PDFs to download for the archive. One per sector/book, plus:

| Alert name (subject prefix) | slug |
|---|---|
| SPAC Broker Research Past Day | `spac-universe` (Meteora SPAC Universe watchlist) |
| Nuclear Energy Broker Research Past Day | `nuclear-energy` |
| Crypto / Stablecoins Broker Research Past Day | `crypto-stablecoins` |
| Software / Cyber / Networking Broker Research Past Day | `software-cyber-networking` |
| Healthcare / Pharma Broker Research Past Day | `healthcare-pharma` |
| Consumer Discretionary / QSR Broker Research Past Day | `consumer-disc-qsr` |
| Autonomous Trucking Broker Research Past Day | `autonomous-trucking` |
| Macro - Rates & Credit (HYG) Broker Research Past Day | `macro-rates-credit` |
| Macro - SPAC / IPO Issuance Broker Research Past Day | `macro-spac-ipo` |
| **SPAC Sector Broker Research Past Day** (state of the SPAC market: issuance, de-SPAC performance, redemptions, sponsor economics) | `spac-sector` [x] created |

## C. News alerts - RETIRED (news is out of scope)
The 5 "Daily News" AI-summary alerts are **deleted** — this pipeline is broker-research only, and news is
handled by the separate Meteora sector-brief skill. Delete these five saved alerts in AlphaSense (this
frees all 5 "Summarize Documents" AI-summary slots):

| Deleted alert (subject prefix) | former slug |
|---|---|
| ~~SPAC Daily News~~ | `spac-universe` |
| ~~Nuclear Energy Daily News~~ | `nuclear-energy` |
| ~~Crypto / Stablecoins Daily News~~ | `crypto-stablecoins` |
| ~~Software / Cyber / Networking Daily News~~ | `software-cyber-networking` |
| ~~Healthcare / Pharma Daily News~~ | `healthcare-pharma` |

The daily run reads ONLY the Agents (Section A) and the broker "Documents Only" alerts (Section B).

## Notes
- **Sources (per alert):** keep **Broker Research** and **Expert Insights** ON — both are wanted primary research, and expert-insight call transcripts must NOT be dropped. Keep **Intellectual Property (patents)** and **News** OFF (they flood).
- SPAC broker coverage on individual tickers is thin - an empty `SPAC Broker Research` alert is normal.
  The **SPAC Sector** agent/alert (thematic state-of-the-market) is where the real SPAC signal lives.
- This is an inventory reference (what should exist). One-time creation/editing is covered in the
  separate **setup guide** (`AlphaSense_Setup_Guide.md`), NOT in this skill. The daily run only reads
  whatever exists - it never creates or modifies agents/alerts/watchlists.


## Addendum (2026-07-02) - Space / Satellite + alert-source hygiene
- **Space / Satellite** is a live scope (it is in `ingestion_scope.json`) and now has its own Agent
  ("Space / Satellite - Broker Research Daily: Weekdays Update"), broker "Documents Only" alert
  ("Space / Satellite Broker Research Past Day"), slug `space-satellite`. It is the 10th agent/alert.
  It has its own Agent + broker "Documents Only" alert (no news alert — news is out of scope).
- **Patents flood the count.** On 2026-07-02 the Space / Satellite broker alert returned ~700 docs across
  8 emails because **Intellectual Property (patents)** was enabled as a source - it matched every
  satellite/LEO/direct-to-cell patent from Samsung, Apple, Qualcomm, Intel, etc. Fix on the saved alert:
  Sources -> uncheck Intellectual Property, keep **Broker Research** only. Until fixed, treat Space as
  noise-dominated: down-scope to genuine broker research (~a dozen SSRFS docs) and say so in the email.
- **Agent syntheses now arrive by email** ("... Broker Research Daily: Weekdays Update"), so Step 3 reads
  them from the inbox; Chrome `/gensearch` is a fallback only.
