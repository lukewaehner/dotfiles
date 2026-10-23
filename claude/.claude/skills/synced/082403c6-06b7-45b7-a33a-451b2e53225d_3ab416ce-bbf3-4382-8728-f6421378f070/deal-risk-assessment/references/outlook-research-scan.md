# Sell-Side Enrichment — Outlook Channel (Microsoft 365)

One of the sell-side channels that feed the two enrichment points of the deal-risk assessment (Phase 4 market structure, Phase 7 deal handicapping). This channel harvests the broker research that lands in the user's own **Outlook** inbox — initiation notes, deal-reaction notes, event-driven desk commentary — and normalizes it into the shared per-note schema so it merges with the uploaded deal-folder research and the Vector Database passes.

This is context that EDGAR cannot provide: named analysts' reads on the regulatory track, expected review timeline, precedent transactions they cite, remedy speculation, and market-structure estimates. Fold it in as attributed input to Meteora's own analysis — never as a substitute for reading the agreement and the filings.

## The blind wall applies here — read this first

Broker deal notes routinely lead with the spread, price targets, and "deal math." Those belong to Phase 8 (Tape Check), not to the blind fundamental work. When reading during Phases 4–7, extract ONLY the permitted content for the current enrichment point and quarantine everything price-shaped:

- **Enrichment point 1 (Phase 4 — market structure):** market-size, market-share, patient-pool, penetration, and competitive-positioning estimates; analyst views on barriers to entry and competitive dynamics. A named, dated analyst estimate satisfies the sourcing rule *as an estimate* — label it "analyst estimate (firm, date)" and note dispersion if analysts disagree.
- **Enrichment point 2 (Phase 7 — deal handicapping):** analyst views on regulatory risk and expected review track (clean vs. second request), timeline expectations, precedent transactions cited, and remedy speculation.
- **Deferred to Phase 8:** price targets, spread commentary, implied-probability calls, "deal math." If a note carries useful spread commentary, note that it exists and return to it in the Tape Check (where analyst spread views may be cited alongside the live tape). Do not carry a single price/spread figure into Sections 1–7.

The point of the blind wall is to form a completion view independent of the market's consensus. A leaked price target anchors the whole assessment to the spread — surface it only after Section 7 is written.

## Step 1 — Search Outlook

Tool: `outlook_email_search`. For each relevant ticker (target AND acquirer — brokers often title a note by the acquirer), search with `query=<TICKER>`, `order=newest`, `limit=25`. Page through with `nextOffset`/`offset` (or `nextCursor`/`cursor` if returned) **until the result set is fully exhausted — every page, not just the first**. Scope the window to roughly the deal's announcement date forward — older mail predates the transaction and is not deal handicapping. Do not cut the search short for speed: a note on page three can carry the decisive regulatory read.

- `query` matches subject, body, AND attachments — a recall-first net; Step 2 is the precision filter.
- Do NOT set `folderName` — the whole mailbox is wanted.
- **Capture is sender-agnostic.** These notes almost always arrive *forwarded internally* — the top-level From is a colleague (`@meteoracapital.com`), the To may be an individual or a distribution alias (`team@`, `filings@`), and the broker is buried in the quoted headers. Do NOT filter by sender or restrict to broker domains; that drops every forwarded note. The subject-line ticker is the capture key.

## Step 2 — Filter to genuine subject-line matches

Keep only emails whose **subject** contains a target/acquirer ticker as a standalone token. Match on word boundaries (case-insensitive), NOT substring — otherwise "V" hits "View", "MA" hits "Management", "ON" hits everything. A hit is valid when the ticker is delimited by start/end, whitespace, or punctuation (`$ : / - ( ) [ ]`). A leading `$` (`$JNPR`) is a strong positive. Deal notes routinely title both sides together — `CRNX-VRTX`, `CRNX/VRTX`, `CRNX / VRTX` — so a hyphen or slash joining two tickers is a strong positive; match on either. Morning-digest notes list many tickers comma-separated (`CRNX, ESI, FISV, GBTG`); keep them, then scope extraction to the deal's own block in Step 3 and ignore unrelated names.

Drop obvious non-research subjects even when they contain the ticker (out-of-office, calendar invites, internal Meteora threads) using sender/subject judgment.

## Step 3 — Read and extract each note

Fetch the FULL content with `read_resource` on the returned URI and read the note end to end — the search-result snippet is not enough, and the decisive detail (the precedent cited, the review-track call, the remedy thesis) is usually buried mid-body. Read every matching note in full rather than sampling a subset; truncating to save time defeats the purpose of the channel. Extract per note into the shared schema:

- **Firm** — from the sender domain / signature (jpmorgan.com → J.P. Morgan). If a syndicate desk relays third-party research, attribute to the authoring firm, not the relayer.
- **Analyst** — named author if present.
- **Date** — received / published date.
- **Channel** — `Outlook` (so the merged table can show where each note came from and de-dup across channels).
- **Market-structure content** (enrichment point 1) — any share/size/positioning estimate, quoted with the number and its basis.
- **Deal view** (enrichment point 2) — regulatory/antitrust read, expected review track, close-timing expectation, precedents cited, remedy speculation. **Tag any completion-sentiment line with its stage** — pre-announcement (was a deal likely to be *struck*, from the rumor window) vs. post-announcement (will the *signed* deal *close*). A note published on announcement day often relays pre-announcement sentiment ("buy-side ~50/50 on whether they'd do it," "a deal was largely expected"); that is deal-background, not completion risk on the signed deal, and must not feed the Phase 7 completion view as if it were.
- **Deferred-to-Phase-8 flag** — note (do not transcribe) whether the note also carries a price target / spread call, so the Tape Check knows to come back to it.
- **Quote** — one short verbatim thesis line, for precise attribution.

Never infer a firm's stance from its rating alone — a Buy on the acquirer is not a view on deal completion. Record a deal view only when the note expresses one; otherwise mark "deal view: not addressed".

### Real-world email shapes — attribute carefully

- **Forwarded chains.** Walk down the quoted `From:` headers to the innermost original sender and attribute the firm from that broker domain and desk signature (`randy.udell@ubs.com` → UBS, `david.connor@cantor.com` → Cantor Fitzgerald). Never attribute to the internal forwarder.
- **Internal wrapper commentary.** A colleague's own take on top of a forward is internal context, not a broker view — extract the research beneath it; don't count the colleague as a "firm".
- **Multi-deal digests.** Extract only the target deal's block; ignore other deals, the events calendar, and unrelated single-stock research.
- **Desk commentary vs. published Research.** Most are explicitly "sales & trading commentary — NOT a product of Research." Attribute to the desk ("UBS Special Situations", "Cantor CF Event Driven"). If the same email cites the firm's separate published-Research rating/PT, capture it labeled as published Research, distinct from the desk's arb view — and remember the PT itself is Phase-8 content.

## Step 4 — Hand off to the shared pipeline

Return the normalized notes to the enrichment merge in the SKILL body: de-dup against the uploaded deal-folder research and the Vector Database items (the same note often arrives by email AND sits as a PDF in the Project — collapse to one record, preferring the fuller copy, usually the uploaded PDF, and keep every channel tag), then attribute by firm + date at each enrichment point.

If Outlook is inaccessible (not connected / not signed in), state that the Outlook channel was unavailable and proceed — its absence widens the data-limitation disclosure in Section 7 but does not block the report.

## Sourcing note

Broker research is non-public, copyrighted third-party material. Use it to inform Meteora's own analysis and attribute views by firm; quote only short thesis lines, not whole notes. Do not reproduce broker notes verbatim at length in the deliverable.
