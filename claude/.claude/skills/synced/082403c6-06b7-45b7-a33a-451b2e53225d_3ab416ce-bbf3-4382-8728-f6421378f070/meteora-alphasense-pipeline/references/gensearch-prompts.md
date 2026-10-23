# GenSearch / Agent instruction prompts

These are the recurring instructions for each sector's scheduled Agent (and for a live GenSearch run if
an agent doesn't exist yet). They are deliberately uniform: firm/analyst, thesis, rating/PT change,
sector + de-SPAC/acquisition implication, cite each source, and a graceful empty-day line. Keep
"broker research only" - validated on Nuclear that this scopes GenSearch to sell-side docs.

Common template (substitute `<SECTOR THEMES>`):
> Summarize the most important NEW sell-side broker research on `<SECTOR THEMES>` from the past 24 hours.
> For each key report give: firm and analyst, the central thesis, any initiation / rating change /
> price-target change, and the implication for the sector and for de-SPAC or acquisition-target dynamics.
> Use broker research only, and cite each source. If there is no material new broker research, say so
> briefly.

## Per-sector `<SECTOR THEMES>`
- **nuclear-energy** - nuclear power, small modular reactors (SMR), advanced reactors, and uranium
- **crypto-stablecoins** - crypto, stablecoins, digital-asset treasuries, crypto exchanges/custody
  (GENIUS/CLARITY Act, USDC/USDT, spot ETFs, tokenization, Circle/Coinbase/MicroStrategy)
- **software-cyber-networking** - software, cybersecurity, networking (Zero Trust, SASE, XDR, SIEM,
  endpoint security, AI networking, data-center networking; CrowdStrike, Palo Alto, Zscaler, Fortinet,
  SentinelOne, Arista, Broadcom, Cisco, Cloudflare)
- **healthcare-pharma** - pharma/biotech M&A, GLP-1/obesity, oncology & CNS readouts, FDA/CHMP/AdCom
  actions, drug pricing (Keytruda, Leqembi, ADCs)
- **consumer-disc-qsr** - restaurants/QSR: same-store sales, traffic, menu pricing, fast-casual
  (Chipotle, Sweetgreen, Cava, Wingstop, McDonald's, Starbucks); GLP-1 impact on restaurants
- **autonomous-trucking** - autonomous trucking & self-driving freight (Aurora, Kodiak, Uber Freight,
  Tesla Semi, SAE Level 4, robotaxi)
- **macro-rates-credit** - rates & credit: high yield / HYG, credit spreads, Fed/rate path, leveraged
  finance, IG spreads, issuance conditions
- **macro-spac-ipo** - SPAC / IPO issuance & ECM: new issues, IPO pipeline, equity capital markets
- **space-satellite** - space, satellite & space-telecom: launch (Rocket Lab, Firefly), LEO
  constellations & direct-to-cell / direct-to-device (AST SpaceMobile, Globalstar, Iridium, Starlink),
  satellite broadband (Viasat, EchoStar, SES, Amazon Kuiper), Earth observation / geospatial (Planet,
  BlackSky, Spire), and defense / national-security space (SDA, missile defense)

## SPAC Sector (state-of-the-market thematic) - `spac-sector`
Use this variant instead of the common template (it's about the SPAC market itself, not one ticker):
> Summarize the most important NEW sell-side broker research on the **state of the SPAC / de-SPAC market**
> from the past 24 hours - new SPAC issuance and trust terms, de-SPAC deal announcements and post-deal
> performance, redemption trends, sponsor economics and incentives, PIPE/financing conditions, and any
> regulatory developments. For each report give firm and analyst, the takeaway, and what it implies for
> SPAC arbitrage, prime de-SPAC/acquisition targets, and issuance conditions. Use broker research only,
> and cite each source. If there is no material new broker research, say so briefly.

*Validated 2026-07-01 on Nuclear: the agent returned a cited, broker-scoped synthesis across BTIG,
Cantor, Deutsche Bank, Longspur, and Hannam - incl. BTIG BWXT "Top Pick / PT $235", Cantor "OKLO OW $122
/ NuScale OW $20", DB "BWXT Buy $255", Longspur's HALEU bottleneck, and the de-SPAC "LOIs -> firm orders"
/ "technical -> fundamental execution" angle - with zero Claude tokens.*
