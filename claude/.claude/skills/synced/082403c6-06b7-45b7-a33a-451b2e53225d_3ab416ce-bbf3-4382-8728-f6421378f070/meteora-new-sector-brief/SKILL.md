---
name: meteora-new-sector-brief
description: Orchestrator for creating a new Meteora Daily Morning Brief sector. Clones the canonical template, swaps ONLY sector-specific fields (name, slug, tickers, exchange suffixes, ticker count, keywords, sector whitelist + IR pages, Step C.1 WebSearch queries, optional extra unreliable sources), writes the new SKILL.md to C:\Users\rishi\Documents\Claude\Scheduled\meteora-SLUG-brief\, and registers a scheduled task on cron `15 8 * * 1-5` for 9 AM ET delivery. Trigger when the user asks to add a new sector to the morning brief family, create a new sector brief, spin up a [sector] brief, or any variant. Preserves ALL existing rules VERBATIM: Bloomberg get-price primary perf fetch with freshness gate, 24-hr cap, whitelist/paywall rules, bullet format, pub-date verification, 9 AM send_at, [TEST] subject prefix, Stage 1 to AI_Interns, Stage 2 to filings@ HELD pending confirmation. Always use this skill for new sector briefs — do not fork files by hand.
---

# Meteora Daily Morning Brief — New Sector Orchestrator

## WHAT THIS SKILL DOES

Creates a new sector brief in the Meteora Daily Morning Brief family by cloning the canonical template (`template.md` shipped alongside this skill) and substituting ONLY the sector-specific fields. Every rule — Step 0 JS-based date computation, Step A Bloomberg get-price primary performance fetch (with HARD freshness gate + Yahoo fallback chain, rewritten 2026-06-05 after the stale-close incident), Step B Google Finance scraper, Step C mandatory pub-date verification, Step D HTML template (Performance-on-top canonical order as of 2026-06-03, Pre-Mkt column added 2026-06-05), Step E pre-send audit, Step F send-as-me 9 AM `send_at`, Stage 2 approval gate, every production-failure rule layered on top — is preserved verbatim from the template.

The user's exact instruction (2026-06-03): **"MAKE SURE THAT THE RULES THAT WE ARE FOLLOWING NOW INCLUDING HOW WE DO THE JS stuff & EVERYTHING STAYS THE SAME. ONLY THING THAT WILL CHANGE IS BASICALLY THE NAME/TICKER/SUFFIXES etc etc!"** Honor this strictly.

## CRITICAL — WHAT NEVER CHANGES

You MUST NOT edit any of the following when running this skill:
- The SOURCE OF TRUTH preamble
- The KNOWN BUG explanation in Step 0
- Step 0a JS block (date computation + send_at_iso) — verbatim character-for-character
- Step 0b bash cross-verify
- Step 0c FORBIDDEN language + the weekday-verbatim rule
- Step 0d weekday match audit
- CRITICAL RULES 1-9
- BULLET FORMAT (LOCKED) — entire section verbatim
- Step A Bloomberg get-price workflow (A.1 spot batch, A.2 history, A.3 returns, A.4 FRESHNESS GATE, A.5 fallback chain) — EXCEPT the `tickers` array literal substitution in A.1
- Step B `window._scrapeResult` JS — verbatim
- JS SCRAPER FALLBACK section — verbatim
- URL EXTRACTION DISCIPLINE — verbatim
- URL PATTERN BLACKLIST — verbatim
- Step C.2 / C.3 / C.4 / C.5 — verbatim (ONLY C.1 queries change)
- Step D HTML structure — Performance-on-top order; ONLY `<h2>` sector name and ticker-count in date line change
- Step E pre-send audit 1-12 (incl. E.12 anchor freshness audit) — verbatim
- Step F send_email procedure — verbatim except subject sector name
- Stage 2 approval gate — verbatim except sector name in the question text
- Scheduled-run mode (HELD by default) — verbatim
- LOCKS section — verbatim except sector name + subject

If you find yourself "improving" or "simplifying" any of these on the way through, STOP. The rules are battle-tested. Add new sectors with the same rules.

## SUBSTITUTION VARIABLES

These are the ONLY fields that change. They are marked in `template.md` as `{{PLACEHOLDER}}`:

1. `{{SECTOR_NAME}}` — display name. Examples: `Autonomous Trucking`, `Crypto / Stablecoins`, `Healthcare`, `Energy / Oil & Gas`, `Industrials / Defense`.
2. `{{SECTOR_SLUG}}` — kebab-case slug used in folder name + scheduled-task ID. Examples: `autonomous-trucking`, `crypto-stablecoins`, `energy-oil-gas`. Final folder name will be `meteora-SLUG-brief`.
3. `{{TICKER_COUNT}}` — integer; number of tickers tracked. Appears in the body date line.
4. `{{TICKERS_JS_ARRAY}}` — double-quoted JSON array literal for Step A.1 (Bloomberg get-price batch call) and the A.5 Yahoo fallback. Example: `["AUR","KDK","UBER","EH"]`.
5. `{{TICKERS_DOC}}` — comma-separated string for the SECTOR CONFIG bullet. Example: `AUR, KDK, UBER, EH`.
6. `{{EXCHANGE_SUFFIXES_BLOCK}}` — indented markdown sub-bullets, two-space indent, grouped by exchange.
7. `{{SECTOR_KEYWORDS}}` — comma-separated, double-quoted keyword phrases. 15-25 phrases.
8. `{{SECTOR_WHITELIST_LINE}}` — sector-specific publisher domains, comma-separated.
9. `{{COMPANY_IR_LINE}}` — comma-separated IR page domains.
10. `{{SECTOR_UNRELIABLE_ADDITIONS}}` — optional. Default empty. If present, MUST start with `, ` to chain onto the existing UNRELIABLE list.
11. `{{WEBSEARCH_QUERIES_BLOCK}}` — 3-4 markdown bullets for Step C.1. Keep `${TODAY_SHORT}` and `${YESTERDAY_YYYY_MM_DD}` as literal placeholders.

Everything else in the template is preserved verbatim. NO other variables, NO other edits.

## EXECUTION FLOW

### Step 1 — Gather sector specifics

Ask the user in chat (free-text needed). Suggested prompt:

> To spin up a new sector brief, I need:
> 1. Sector name (display, e.g. `Energy / Oil & Gas`)
> 2. Sector slug (kebab-case, e.g. `energy-oil-gas`)
> 3. Tickers + exchanges (e.g. `XOM:NYSE, CVX:NYSE, COP:NYSE`)
> 4. 15-25 sector keywords (comma-separated, double-quoted)
> 5. Sector-specific whitelist sources (publisher domains)
> 6. Company IR pages
> 7. Extra unreliable domains (optional)
> 8. 3-4 Step C.1 WebSearch queries (or "derive defaults")

If user gives partial info, ask follow-ups. If "derive defaults" for queries, derive mechanically and show before proceeding.

### Step 2 — Read the canonical template

`Read` the file at the same folder as this SKILL.md: `template.md` (sibling file).

### Step 3 — Apply substitutions

Build new content in memory by string-substituting every `{{PLACEHOLDER}}`. Audit: confirm zero `{{` markers remain. If any do, re-check Step 1.

### Step 4 — Write the new SKILL.md

- Folder: `C:\Users\rishi\Documents\Claude\Scheduled\meteora-{{SECTOR_SLUG}}-brief\`
- File: `<folder>\SKILL.md`

Use PowerShell (`mcp__Windows-MCP__PowerShell`) directly — Desktop Commander writes can land in a sandbox and not persist. Verify with `Test-Path` and content read-back before proceeding.

### Step 5 — Register the scheduled task

First, query an existing task with `mcp__scheduled-tasks__list_scheduled_tasks` and inspect the prompt of (say) `meteora-autonomous-trucking-brief`. Copy the exact phrasing.

Then `mcp__scheduled-tasks__create_scheduled_task`:
- `taskId`: `meteora-{{SECTOR_SLUG}}-brief`
- `cronExpression`: `15 8 * * 1-5`
- `prompt`: same phrasing as existing tasks, slug substituted

If pattern not queryable, fall back to: "Read and execute `C:\Users\rishi\Documents\Claude\Scheduled\meteora-{{SECTOR_SLUG}}-brief\SKILL.md` following every rule verbatim. Stage 1 → AI_Interns via send_at 9 AM ET, [TEST] subject prefix. Stage 2 (filings@) → HELD by default, requires explicit confirmation."

### Step 6 — Confirm

Report: path of new SKILL.md, scheduled task ID + cron + next fire, Stage 1 recipient (AI_Interns) + 9 AM send_at + [TEST] prefix, Stage 2 (filings@) HELD-by-default pending confirmation. Remind: when production rules update in any live brief, mirror to `template.md`.

## ANTI-PATTERNS — DO NOT

- DO NOT rewrite the JS or the Bloomberg get-price workflow in your own style. Copy verbatim via template substitution only.
- DO NOT relax the 24-hr cap, paywall drop list, pub-date verification gate, bullet format contract, or the Step A.4 anchor FRESHNESS GATE (never ship a silently stale close).
- DO NOT change send_at from 9 AM, cron from `15 8 * * 1-5`, Stage 1 recipients (AI_Interns only), the [TEST] subject prefix (current test phase), or Stage 2 (filings@) HELD-by-default-pending-confirmation.
- DO NOT change Step D order from Performance → Sector News → Ticker News → New-ticker flags → Deals.
- DO NOT generate sector keywords / sources without showing them to the user first.
- DO NOT register the scheduled task in any state other than enabled, exact cron `15 8 * * 1-5`.
- DO NOT add new sections, footers, or "improvements" to the template.
- DO NOT preserve the triple YAML-frontmatter artifact from the existing 5 sector briefs.

## DEPRECATED PREDECESSOR

This skill SUPERSEDES `sector-watch` (depr