# Browser mechanics (Chrome MCP) - execution only

Everything runs through the user's already-logged-in AlphaSense session. NO API, NO scraping
(PerimeterX/HUMAN bot protection + service-worker doc streaming). Drive the real browser.
This file covers the DAILY RUN only. Agents/alerts are assumed to already exist (one-time setup lives in
the separate setup guide, not in this skill - the skill executes, it does not build).

## Contents
1. Load tools & select the browser
2. Login check (auto-SSO)
3. Download a broker PDF (deep-link -> Download)
4. Read a scheduled Agent's report
5. Run a live GenSearch query (fallback only)
6. Known UI gotchas

## 1. Load tools & select the browser
One ToolSearch call:
`select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__find,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__select_browser,mcp__claude-in-chrome__list_connected_browsers,mcp__claude-in-chrome__read_page`
Select **Browser 1 (Windows)** deviceId `8eba543d-2309-4ce4-9e54-0242ce24b905`. Create a fresh tab.

## 2. Login check (auto-SSO)
Navigate to `https://research.alpha-sense.com/search`, wait ~5s. If a login/SSO wall shows instead of
the UI, **click the "Log in" button** - the org SSO auto-authenticates, no credential entry. Then
continue. Only STOP + email the user if it demands a typed password or captcha (never type credentials
or solve captchas).

## 3. Download a broker PDF (deep-link -> Download)
From an alert email, each new doc has a `docid` — `SSRFS-...` or `ASR-...` for broker research, `EC-...` for an Expert Insight (all download the same way).
1. Navigate `https://research.alpha-sense.com/search?docid=<DOCID>`; wait for the reader.
2. Click the **Download** icon (reader toolbar). "GENERATING DOWNLOAD..." appears bottom-left.
3. Wait until it clears (~5-15s). Chrome auto-saves (no OS dialog) to `C:\Users\rishi\Downloads` as
   `YYYYMMDD - Firm - Title - N pages.pdf`.
4. Archive: `python scripts/archive_pdf.py --slug <slug> --root "<project root>" --downloads "C:/Users/rishi/Downloads" --docid <DOCID> --newest` (moves it, dedupes, appends manifest).
5. Caps: 25/alert, 60/run. The script + `_state_seen.json` prevent re-downloads.
Reader bodies often render as streamed images (not selectable) - the Download is the reliable full-text
path; the results *feed* text is fully extractable via `get_page_text` for the manifest.

## 4. Read a scheduled Agent's report
Agent output is **in-platform only** (not emailed). Each morning the agent has already run (5-7 AM):
1. Go to `/gensearch`. In the left **THREADS** list, the agent's latest run appears as
   "<Agent title> - Scheduled Agent - <date>". Open it (or open the agent card under **My Agents** -> its
   latest thread).
2. **Wait for full completion before extracting** - the report is done only when "Related Questions" /
   "Build Slides" / "Create Agent" appear at the bottom and the red stop button reverts to ^. A
   mid-stream `get_page_text` truncates to the first firm's section (this bit us in testing - re-read
   once to be safe).
3. `get_page_text`, then save to `BrokerResearch/<slug>/<YYYY-MM>/_GenSearch_<slug>_<date>.md`.

## 5. Run a live GenSearch query (fallback only)
Only if a sector's agent is missing or its scheduled run failed. `/gensearch` -> **New Thread** -> click
the **"Ask AlphaSense..."** input (click twice if the "All Sources" dropdown steals the first click;
placeholder changes to "Type @ for company profile lookup...") -> paste the prompt from
`gensearch-prompts.md` -> submit (^) -> wait for FULL completion (Sec 4) -> `get_page_text`.

## 6. Known UI gotchas
- Toolbars reflow on resize; prefer `find`/`read_page` refs over fixed pixels; re-screenshot to
  re-locate controls.
- The reader's "Most Relevant Expert Insights" recommendation cards (sidebar) are NOT the alert's flagged docs — opening one navigates away, use **Back**. Expert-insight docs the ALERT itself flags (their own `EC-` docid) ARE wanted — download them like any other in-scope doc.
- `chrome://` URLs can't be opened by the extension; check downloads on the filesystem.
- Screenshots occasionally time out ("renderer frozen") - retry.
