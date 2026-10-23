# Sector Watch — Keywords & Tickers

Meteora Capital's tagging doc for the `sector-watch` skill. Each top-level
heading (`## `) is a **sector**. Each sector has three subsections:

- `### Tickers` — explicit public-company universe to pull price performance
  for. One ticker per bullet. Add a short label after the ticker for clarity.
- `### Keywords` — phrases the skill runs through `bdata search --type news`
  for the past 24–48 hours of news. One phrase per bullet. **The skill's
  focus is SPAC / event arbitrage** — phrase keywords toward deals, IPOs,
  M&A activity, financings, and material catalysts in each vertical, not
  ambient industry chatter.
- `### Notes` *(optional)* — context for the Claude composing the narrative.

## Pausing a sector

To **pause** a sector (keep it in the file but skip in rotation), prefix the
`## ` heading with `[PAUSED] ` — e.g. `## [PAUSED] Regulatory & Market Structure`.
The parser flags it; the rotation skips it; nothing else changes. To unpause,
remove the `[PAUSED] ` prefix. Currently paused sectors below: SPAC IPOs,
SPAC Deals, Structured Equity, and Regulatory & Market Structure.

## Rules

- One sector per `## ` heading.
- Use quoted phrases for literal multi-word matches: `"definitive agreement"`.
- `site:` operators are allowed inline: `SPAC merger site:bamsec.com`.
- Negative terms are allowed: `"biotech merger" -recall`.
- Lines starting with `#` other than sector headings are comments.
- Empty sectors / empty subsections are skipped.
- Order sectors by importance — the rotation hits them Monday-Friday in
  document order. With N sectors, the cycle takes N weekdays.

## How to add or remove a sector

**Add:** insert a new `## Sector Name` heading anywhere in the file with at
least `### Keywords` populated (Tickers + Notes optional). Save. The next
run picks it up. The rotation extends by one weekday automatically.

**Remove:** delete the `## ` heading and its content. Save. The rotation
contracts.

**Reorder:** move the `## ` heading. New position = new slot in the cycle.

Example — adding a new "Defense Technology" sector:

```
## Defense Technology

### Tickers
- KTOS — Kratos Defense
- AVAV — AeroVironment

### Keywords
- "defense SPAC merger"
- "defense IPO"
- "going public" defense
- defense tech acquisition

### Notes
- Focus on the wave of defense-tech deSPACs and IPOs in 2026.
```

Save the file. Next run rotates through.

---

## [PAUSED] SPAC IPOs & New Filings

### Tickers
- (no fixed universe — universe shifts every IPO. Rely on auto-discovery flags
  to surface new names mentioned in the past 24–48 hours' news.)

### Keywords
- "SPAC IPO" priced
- "blank check company" S-1
- "trust account" overfunded
- new SPAC sponsor team
- SPAC right-only structure
- "unit IPO" Nasdaq
- "blank check" 424B4 filed

### Notes
- We're tracking unit structure aggressively — flag any deviation from
  standard 1S+1/2W+1/10R. New SPAC IPOs are the universe-discovery feed for
  the broader sector-watch rotation; tickers discovered here often become
  positions later.

## [PAUSED] SPAC Deals & Business Combinations

### Tickers
- (no fixed universe — populate with SPAC tickers we're actively positioned
  in. Auto-discovery flags catch deal announcements that aren't yet on the
  list.)

### Keywords
- SPAC merger announced
- "business combination agreement" SPAC
- "definitive merger agreement"
- de-SPAC closing
- "S-4" filed SPAC
- "F-4" filed SPAC
- SPAC PIPE investor
- SPAC redemption deadline
- "trust extension" SPAC vote
- "shareholder vote" SPAC

### Notes
- The core daily section for our event-arb book. Prioritize deals being
  announced or closing this week.

## Autonomous Trucking

### Tickers
- AUR  — Aurora Innovation
- KDK  — Kodiak AI (formerly Kodiak Robotics)
- UBER — Uber Technologies (Uber Freight — adjacent exposure)
- EH   — EHang Holdings (adjacent eVTOL, not pure trucking)

### Keywords
- "autonomous trucking" merger
- "self-driving freight" acquisition
- AV trucking IPO
- Aurora Innovation deal
- Kodiak AI financing
- "freight technology" SPAC
- TuSimple Embark Plus.ai deal

### Notes
- Active sector with real commercial deployments (AUR + KDK both running
  Dallas-Houston). Watch for further consolidation, OEM partnerships, or
  failed-AV-co reverse mergers as event-arb opportunities.

## Crypto / Stablecoins

### Tickers
- CRCL — Circle Internet Financial (USDC issuer)
- COIN — Coinbase Global
- HOOD — Robinhood Markets (crypto trading)
- MSTR — Strategy (BTC treasury — legacy DAT name)
- SBET — SharpLink Gaming (ETH treasury)

### Keywords
- stablecoin IPO
- "stablecoin" SPAC merger
- "stablecoin issuer" public listing
- "GENIUS Act" stablecoin
- Circle IPO USDC
- Tether public listing
- "crypto exchange" IPO
- "crypto custody" deal
- "digital asset treasury" company financing
- bitcoin treasury PIPE

### Notes
- Pivoting from pure DAT focus to stablecoin-first per the May 2026 surge in
  stablecoin issuer activity (Circle IPO, Tether speculation, regulatory
  clarity via GENIUS Act). DAT names retained but secondary.

## Software

### Tickers
- CRWD  — CrowdStrike (recent acquirer: Seraphic Jan 2026)
- ZS    — Zscaler (recent acquirer: SquareX Feb 2026)
- PANW  — Palo Alto Networks (active consolidator)
- NET   — Cloudflare (potential target)
- CSCO  — Cisco (acquirer: Astrix Security May 2026)

### Keywords
- "software acquisition" announced
- "SaaS" going private
- "cloud software" merger
- "cybersecurity" acquisition
- enterprise software IPO
- "software" definitive agreement
- "going private" software
- vertical SaaS take-private
- PE acquires software company

### Notes
- Focus on take-private deals from PE (the dominant exit path for sub-scale
  SaaS in 2025-2026). Surveillance for reverse mergers when shell SPACs find
  software targets.

## Healthcare

### Tickers
- BIIB  — Biogen (acquirer: Apellis closed May 2026)
- MRK   — Merck (rumored $70B target hunt)
- GILD  — Gilead Sciences (active acquirer)
- PFE   — Pfizer (patent cliff buyer)
- LLY   — Eli Lilly (active buyer)

### Keywords
- "biotech acquisition" announced
- "pharma" definitive agreement
- "medical device" SPAC merger
- biotech IPO priced
- "biotech merger" tender offer
- "going public via SPAC" healthcare
- "reverse merger" biotech
- pharma acquires biotech
- "going private" healthcare
- "tender offer" pharmaceutical

### Notes
- Biotech is highly deal-driven (M&A is the dominant exit). Reverse mergers
  via shell SPACs are a recurring event-arb playbook. Filter aggressively
  for genuine deal announcements vs ambient pipeline news.

## Consumer Discretionary

### Tickers
- SBUX  — Starbucks (activist target speculation)
- CMG   — Chipotle (sector reference)
- WING  — Wingstop (deal-active franchise model)
- DPZ   — Domino's Pizza (franchise consolidation)
- MCD   — McDonald's (sector anchor)

### Keywords
- "restaurant chain" IPO
- "retail merger" announced
- "DTC brand" acquisition
- "consumer SPAC" business combination
- "going private" retail
- "consumer goods" definitive agreement
- restaurant SPAC merger
- DTC IPO priced
- "private equity" restaurant acquisition

### Notes
- Consumer is broad and uneven. Restaurant chains, DTC brands, and luxury
  retail are the most deal-active sub-verticals. Many take-privates here.

## [PAUSED] Structured Equity & Micro-cap Financings

### Tickers
- (no fixed universe — universe shifts weekly. Rely on auto-discovery flags.
  Add tickers as we end up in positions.)

### Keywords
- "standby equity purchase agreement"
- SEPA financing micro-cap
- "equity line of credit" Nasdaq
- "convertible note" exploding warrant
- "exploding unit" offering
- Maxim Group offering 424B4
- Nasdaq deficiency notice
- "going concern" 424B4

### Notes
- Universe is wide and shifts weekly. Auto-discovery is primary. Filter for
  Meteora-relevant structures (sponsor-friendly convertibles, SEPA
  agreements, exploding units).

## [PAUSED] Regulatory & Market Structure

### Tickers
- (no tickers — this is a context section, news only)

### Keywords
- SEC SPAC rules update
- Nasdaq listing standards SPAC
- "Reg M" SPAC blackout
- "Crescent Term" warrant
- SEC stablecoin rules
- GENIUS Act implementation

### Notes
- News-only section. No performance table needed; render this sector as a
  brief context paragraph + bullets. Watch for rule changes that affect
  SPAC mechanics or our other sectors' deal structures.

---

# How the skill uses this file

1. Parse each `## ` heading as a sector name.
2. Under each sector:
   - `### Tickers` bullets → ticker universe for that sector's perf table.
   - `### Keywords` bullets → news search queries (past 24–48 hours).
   - `### Notes` body → context Claude considers when writing the narrative.
3. Run **general** news search for every keyword (past 48 hrs).
4. Run **deal-focused** news search by combining the sector context with
   universal deal keywords (see `config.json` → `news.deal_keywords`).
5. **Dedupe** today's results against the past 7 days of links the skill
   already emailed for this sector (state file at `~/.sector-watch/sent-state.json`).
6. Pull 1D/1W/1M/6M/YTD/1Y Yahoo Finance performance for each ticker.
7. Scrape article bodies for the top news items.
8. Synthesize narrative + Deals section + per-ticker briefs + performance
   table.
9. Render and email. After successful send, append today's URLs to the
   state file under today's date.
