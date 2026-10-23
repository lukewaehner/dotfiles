# Current Themes

This directory holds the persistent, living knowledge about the SPAC market state that the agent consults **unconditionally on every run** — before analogs are suggested, before recommendations are written.

## Why this exists

The precedent library approach (one file per closed deal) does not compound fast enough to be useful. What compounds faster is a small set of living theme files that capture:

- **What is live vs. dead as an investable pattern right now** — the agent otherwise pattern-matches to whatever is semantically closest in the vector DB, including stale 2024–2025 themes
- **Which sponsor franchises and playbooks are currently in market**
- **The macro regime for SPAC IPOs, deal announcements, and liquidations**

These files are read in Pillar 1 on every run. They are short by design — one page or less each. They are the "skeptical senior analyst muttering to themselves before reading any new deck" knowledge.

## The files

- `market-regime.md` — SPAC market macro state (IPO flow, deal-announcement rate, liquidation base rate, PIPE availability)
- `dead-trades.md` — what is explicitly off the table as a target/analog category. The agent must NOT propose an analog from these categories without a structural match, and must NEVER assume a pre-deal target will be from a dead category.
- `live-themes.md` — what is working post-close, where retail-memeability is currently earned, what structural features align with above-trust outcomes
- `serial-sponsors-active.md` — who is in market, their franchise pattern, their typical deal DNA

## Maintenance

- These are expected to be re-read and re-edited at least quarterly, and more often when a regime shift occurs (e.g., DAT trade collapsing in Q4 2025).
- When the agent cites a dead-trade category and is corrected by the user, the correction should be folded into `dead-trades.md` the same session.
- When a new serial sponsor is identified in desk conversation, add to `serial-sponsors-active.md`.

## What these files are NOT

- Not a comprehensive history of every SPAC ever
- Not a ticker-by-ticker precedent catalog (that lives in the vector DB + conversation history, not here)
- Not a replacement for Pillar 1 semantic search (that retrieves specifics; these files set context)
