---
name: spac-db-weekly-update
description: >-
  Refresh the local SPAC Research SQLite database — the `spacs` + `sponsors` tables that back the
  Sponsor Franchise Book — from spacresearch.com's own native exports. Use this whenever the user
  wants to update, refresh, rebuild, or re-pull the SPAC database / SPAC Research data / franchise
  data, says that data is stale or out of date, asks to "run the weekly SPAC update", "refresh
  spacresearch", "rebuild the spac db", "pull the latest SPAC data", or when a scheduled weekly
  refresh fires. The skill drives Claude in Chrome (a browser logged into the FULL spacresearch.com
  account) to download the "All SPACs" CSV and harvest the Sponsors grid, then rebuilds the database
  atomically with integrity checks and a dated backup. Prefer this over ad-hoc, tab-by-tab scraping:
  the native exports are cleaner and richer, and this skill guards against silently ingesting a
  trial/partial pull. Not for answering one-off questions against the existing database — for those,
  just query the database directly.
---

# SPAC DB — weekly update

Keep `spacresearch.sqlite` current by re-pulling spacresearch.com's own exports and rebuilding the
database the same, verifiable way every time. The database has two base tables — `spacs` (one row
per SPAC, every lifecycle stage) and `sponsors` (one row per sponsor vehicle, grouped into families)
— plus helper views. See `reference/SCHEMA.md` for the full schema.

## Why it works this way

Two design choices matter, so keep them intact:

- **Native exports, not grid-scraping.** spacresearch.com renders its tables from a virtualized
  grid, so scraping the DOM is slow and lossy. The site's own "All SPACs" CSV export
  (`/symbol?export-all=csv`) returns every SPAC across all stages in one clean file with more
  columns (counsel, newco tickers, unit/warrant/right specs). The Sponsors page has no clean CSV
  endpoint, so it's the one place we read the grid directly.
- **Atomic rebuild with a trip-wire.** The site shows deliberately *scrambled* placeholder data to
  trial/logged-out sessions. If a run silently ingested that, the database would look full but be
  wrong. So the build writes to a temp file, runs integrity checks, and only replaces the target if
  they pass — otherwise the previous database is left untouched.

## Configure first

Set two values before running (edit them here, or pass at run time):

- `TARGET_DB_PATH` — **`<SET ME>`** — where the rebuilt `spacresearch.sqlite` should be written
  (e.g. a synced Drive folder or a fixed local path). *Placeholder for now; update once decided.*
- `DOWNLOAD_DIR` — the folder the browser downloads into **and** that is connected to this session
  (default: the user's `Downloads`).

## Prerequisites

- **Claude in Chrome** connected to a browser **logged into the full (paid) spacresearch.com
  account.** The refresh reads that logged-in session; a trial or expired login returns limited or
  scrambled data (the integrity check below will catch it and abort).
- `DOWNLOAD_DIR` connected to the session so the rebuild step can read the downloaded files.
- Python 3 (standard library only — no packages to install).

## Procedure

1. **Pick the right browser.** If several are connected, select the one logged into
   spacresearch.com. Open a tab and go to `https://www.spacresearch.com/symbol?s=live-deal` to load
   the session.

2. **Confirm full access.** Check the page has no "symbol-limited trial" banner. If it does, pause
   and ask the user to log into the full account, then continue — everything downstream depends on
   this being the real dataset.

3. **Download the All-SPACs CSV.** Trigger the site's own export so we get every stage in one file:
   ```js
   (() => { const a=document.createElement('a');
     a.href='/symbol?export-all=csv';
     a.download='spac_all_export_'+new Date().toISOString().slice(0,10)+'.csv';
     document.body.appendChild(a); a.click(); a.remove(); return 'triggered'; })();
   ```
   The server may name the saved file `spac-research_<timestamp>.csv` — that's expected.

4. **Harvest the Sponsors grid.** Go to `https://www.spacresearch.com/sponsor`, let the grid load,
   then run the contents of `scripts/harvest_sponsors.js`. It reads the grid's row model and
   downloads `sponsors_<YYYY-MM-DD>.j