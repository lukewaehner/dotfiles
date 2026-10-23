# spac-db-weekly-update (skill)

Keeps your local **SPAC Research database** current by re-pulling spacresearch.com's own native
exports and rebuilding the SQLite file cleanly — same steps every run.

## Install
Save `spac-db-weekly-update.skill` via the card in chat (or Settings → Capabilities → add skill).

## One-time setup
Open `SKILL.md` and set the two placeholders:
- **`TARGET_DB_PATH`** — where the rebuilt `spacresearch.sqlite` should live (placeholder for now).
- **`DOWNLOAD_DIR`** — the browser's download folder, connected to the session (default `Downloads`).

You also need **Claude in Chrome** connected to a browser **logged into the full spacresearch.com
account**.

## Run it
Say: **"update the SPAC database"** — or schedule it: **"run the weekly SPAC DB update every Monday
8am"** (cron `0 8 * * 1`).

## What it does
1. Downloads the "All SPACs" CSV (`/symbol?export-all=csv`).
2. Harvests the Sponsors grid (`/sponsor`) to JSON.
3. Runs `scripts/build_spac_db.py` — rebuilds `spacs` + `sponsors` + views, **atomically**
   (temp build → integrity checks → timestamped backup → replace).

If a run's data looks like a trial/partial pull, the build **aborts and leaves the old DB intact**.

See `reference/SCHEMA.md` for the resulting schema.
