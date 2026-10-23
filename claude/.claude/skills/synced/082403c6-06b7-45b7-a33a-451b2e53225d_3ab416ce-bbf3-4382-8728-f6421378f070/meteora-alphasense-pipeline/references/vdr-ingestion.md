# VDR ingestion (DEFERRED - turn on after POC)

The POC is **local download only**. When the team is ready to ingest into the Pinecone vector DB, this
is the add-on. Do NOT run it until the user confirms the Google Drive target folder - the VDR pipeline
keys off Drive metadata, so the docs must live in the synced Google Drive research folder.

## Tooling (Meteora MCP)
- `list-indexes` / `pinecone-stats` - indexes: **investment-team** (default, ~461k vectors) and **ethm**.
- `process-document` - chunks (800 words / 100 overlap), embeds (ada-002), upserts to Pinecone with
  rich metadata. Takes `content` (the full document **text**, not a path), plus metadata.

## Flow (per downloaded PDF)
1. Extract text from the archived PDF (pdftotext / pdfplumber).
2. Call `process-document` with `content` + metadata:
   - `document_type` (Sellside Note / Initiation of Coverage / Desk Notes / ...), `document_category`
     (Equity/Debt/Sector/Macro), `sector` (GICS), `industry`, `sentiment`.
   - `report_title`, `publication_date`, `author_institution`, `analyst_names`, `primary_company`,
     `primary_ticker`, `secondary_tickers`, `key_themes`.
   - Most of these are already in the AlphaSense filename (`YYYYMMDD - Firm - Title - N pages`) + the
     alert row; fill the rest from the doc text.
   - `index_name`: `investment-team`. Use a dedicated `namespace` (e.g. `alphasense`) at first so it's
     easy to isolate/roll back.
3. Confirm with `pinecone-stats` that vector count grew.

## Sequencing note
Keep this OFF in TEST MODE. When enabling, do a small batch first (one sector) and have the user verify
retrieval via `semantic-search` before ingesting the full daily flow.
