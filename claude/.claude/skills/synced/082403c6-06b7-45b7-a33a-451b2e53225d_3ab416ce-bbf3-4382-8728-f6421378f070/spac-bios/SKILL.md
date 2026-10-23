---
name: spac-bios
description: Skeptical reconstruction of every named principal on a SPAC team — CEO, CFO, IDs, co-sponsors. Trigger on "team diligence on [TICKER]", "team deep dive", "bios on [SPAC]", "team quality on [SPAC]", "individual diligence on [SPAC] team", "are these guys real", "can they raise a PIPE". Also trigger proactively when (a) user pastes an S-1/A and bull case rests on team quality, (b) headline credential is a single recognizable name doing heavy work, (c) structure looks banker-shopped (tier-3 UW, no anchor, no PIPE, mandate scrub), or (d) any pre-deal SPAC analysis. Produces single copy/paste chat output: long-bullet executive summary per person covering exits / fund AUM / billionaire status / PIPE-raise capability, then 9-section per-person deep dive, network map, red flag register, open questions. Always use for SPAC team diligence — ad-hoc analysis launders S-1 copy and misses loaded credentials, undisclosed network bridges, and Bloomberg-confirmed tenure value destruction.
---

# SPAC Team Bios — Individual Due Diligence Framework

Reconstruct every named principal on a SPAC team the way a 20-year SPAC arb analyst would: **the S-1 frames credentials in marketing copy; granular sourcing either confirms or refutes that framing.** Most B3-B5 SPAC teams do not survive granular reconstruction. This skill exists because the default LLM reasoning mode on a SPAC team is to repeat the S-1 bio language back to the user. **That produces wrong answers** in a market where 30-70% of SPACs liquidate, where "Co-founder of [unicorn]" hides minority-CMO equity participation, where Bloomberg-confirmed tenure performance can be -67% under the same person framed as a "successful operator," and where ID slates routinely include uncompensated members whose true allegiance lies with another principal entirely.

The skill produces a single copy/paste-ready chat output (no separate document) following a fixed structure that maps the four investor questions that actually matter — exits, fund AUM, billionaire status, PIPE-raise capability — onto each named principal, then drills into 9 sections per person, plus a network map, red flag register, and open questions.

---

## Core Principles (Load These Into Working Memory Before Writing Anything)

1. **Bloomberg historical price data is the single highest-signal data source for any operating credential.** "Ex-CEO of [public co]" is flat S-1 language. The actual stock chart during their tenure is dispositive — peak-to-trough drawdown during tenure, ROA during tenure, post-departure rally. Always pull `get-price` for any public-co operating role of any team member before writing their §2.

2. **Forbes is the canonical billionaire check.** PRC / Indian / Southeast Asian crypto and tech founders are routinely labeled "billionaire" in regional industry press without independent wealth verification. If the person is not on the Forbes Real-Time Billionaires list, say so explicitly and note the source of the puffery. Compare to verified billionaire comparators in their cohort (e.g., the other co-founder of the same business who is on Forbes).

3. **Marketed AUM ≠ deployed AUM.** Funds routinely market $400M, $1B, $2B targets and deploy 10-30% before quietly abandoning Phase II. A 10% deployment ratio + abandoned Phase II is strong evidence external LPs declined to back the principal at marketed scale. Always pull both numbers and quote the gap.

4. **The S-1 absence of an anchor + PIPE indication after N months of registration is the operative test for PIPE-raise capability**, regardless of headline credentials. If the team had real institutional capital relationships, the deal would not be naked sponsor + public + UW. The structure tells you the answer; the bios are after-the-fact rationalization.

5. **The "who is the co-founder doing now" comp is decisive.** For any name framed around a single recognizable association (Huobi co-founder, ex-Twitter exec, etc.), find what the other co-founder or peer is doing now. If they are doing institutional-scale deals at $1B+ scale and your subject is doing a $100M tier-3 UW SPAC, the institutional capability gap is the cleanest single signal in the entire framework.

6. **Loaded credentials hide in the S-1's omissions.** "Chairman of [foreign insurer]" reads as a clean credential — the actual record may include the chairmanship coinciding with a $10B fraud at the parent company. "Founder of [VC fund]" hides Phase II abandonment. "Ex-CEO of [HKEx co]" hides 5x post-departure stock rally. Always reconstruct the operational context of every disclosed credential before accepting the framing.

7. **Western institutional LPs flag adjacency regardless of formal case status.** A Trump-era SEC dismissal does not clean a Justin Sun / TRUMP / WLFI adjacency. House Democrats letters (Casten/Waters/Sherman, Sept 2025) are the operative diligence flag because they signal next-administration enforcement risk. Apply analogously to other regulatory-uncertainty-era adjacencies.

8. **Mandate scrubs and right-economics richening mid-registration are tells.** Compare the original S-1 to the most recent amendment. Geography target removed, industry focus broadened, right ratio richened (1/10th → 1/4) all signal weak demand requiring re-papering. The disclosed mandate is what cleared SEC review; the realistic mandate is what the team can actually source.

9. **Uncompensated IDs taking a seat for free are doing it for a reason.** The reasonable answers are (a) relationship favor to a specific person on the team, (b) implicit post-IBC equity expectation, or (c) alignment with another principal whose interests diverge from the SPAC. Option (c) is the highest-impact diligence flag — a "Leon Li surveillance presence on Du Jun's SPAC" pattern.

10. **The realistic IBC pipeline is the sponsor's own portfolio in 80%+ of B3-B5 cases.** Vernal Group / ABCDE Capital / family office portfolios are where the deals come from. Any IBC sourced from these networks is an insider rollup transaction with related-party scrutiny risk. The Audit Chair is the principal conflict-screening role — if the Audit Chair is encumbered by a network bridge, the conflict screening is decorative.

---

## Step 1 — Pull the Roster and Structural Facts (Before Anything Else)

Non-negotiable first step. Pull and tabulate before writing any bios.

```
MeteoraMCP:spac-details(ticker="<TICKER>")
MeteoraMCP:edgar-filings(ticker="<TICKER>", form_type="S-1", limit=20)
MeteoraMCP:edgar-filings(ticker="<TICKER>", form_type="S-1/A", limit=20)
MeteoraMCP:get-price(tickers=["<TICKER>", "<TICKER>R", "<TICKER>U", "USGG3M Index"])
MeteoraMCP:emsx-blotter(ticker="<TICKER>")
```

Then read the most recent S-1/A. Extract:

- **Roster** — every officer, director, ID, and co-sponsor with full name, role, residency, citizenship, and S-1 disclosed bio
- **Sponsor structure** — sponsor entities (BVI / Cayman / Delaware), founder share splits, PP unit allocations, related-party admin fees
- **Filing track** — DRS confidential, S-1, every S-1/A with date, offering size, right/warrant economics. **Compare original S-1 to most recent S-1/A** — flag any mandate scrub, right richening, auditor change, structural change
- **Structural facts** — trust amount, extension mechanism, underwriter, counsel, any anchor or PIPE indication

The roster determines who needs a bio. The structural facts feed the §2 transaction context and the §9 synthesis.

---

## Step 2 — Build the Output

The output is a single chat response. Render in this exact section ordering. Do NOT produce a separate file — the user wants copy/paste-ready chat output.

### Section 0 — Header

```
# [TICKER] — [Full SPAC Name]
## Individual Due Diligence — Team Deep Dive
```

### Section 1 — EXECUTIVE SUMMARY: Key Points Per Person

This is the single most important section. The user reads this first; if the bear case is correct, this section alone makes it.

For each named principal, produce 5-8 long bullets in this order:

1. **Prior SPAC roles** — every prior or concurrent SPAC affiliation, with **EXPLICIT role title** (CEO, CFO, Executive Chair, sponsor manager, Director, IID, target-co operator, FPA provider, anchor LP). For each, list: ticker, role title, tenure dates, outcome category (completed deSPAC → public-co ticker + post-deal performance %; still-in-deal → vote/deadline status; liquidated → redemption date and per-share amount; still pre-deal → trust size). **Role title is MANDATORY and must be the first word of each line, not buried in a career-arrow chain.** Format: *"CEO of SKGR (2021-2025) → deSPAC'd to Webull (BULL) 2025; BULL -27% post-deal, warrants $2.34"* — NOT *"SKGR (2021-2025, deSPAC)"*. If zero prior SPAC roles, say so explicitly: *"First SPAC role; no prior SPAC track record."* This bullet always appears FIRST in every person's section. CEO and sponsor-manager roles carry the most diligence weight; director-only roles are still mandatory but are weaker signal. The reader's first question for any SPAC principal is "what did they do on prior SPACs and how did those end" — answer that question first.

2. **Exits (non-SPAC)** — every documented sale event, IPO, M&A, PE buyout, or capital event NOT covered above. For each: deal name, approximate size, role (founder/GP/minority/advisor), outcome. **If zero non-SPAC exits, say so explicitly.** If only one, count it and frame it ("ONE participation in his entire career").

3. **Operating track record post-exit (if applicable)** — for any public-co operating role, pull Bloomberg historical for their tenure window. Quote peak-to-trough drawdown during tenure, post-departure rally, ROA / EBITDA / revenue trajectory. **This is the most informative single signal.** Pre-tenure baseline vs. tenure performance vs. post-tenure performance is the structure. Bold the tenure drawdown.

4. **Fund affiliations + AUM** — every fund / family office / asset manager. For each: name, vehicle type, role, **marketed AUM, actually deployed AUM** (always quote both). Note Phase I vs Phase II, abandoned funds, dormant vehicles. Pull SEC EDGAR `filer_cik` for any U.S.-registered Form ADV / 13F / 13D-G to verify offshore-vs-U.S. registration footprint. **No SEC-registered fund is itself a signal.**

5. **Billionaire status** — Forbes Real-Time Billionaires list check. Quote rank and net worth if listed; if NOT listed, say so explicitly and note the source of any "billionaire" framing in industry press. Compare to verified billionaire comparators in their cohort.

6. **PIPE-raise capability** — assess ability to bring institutional anchor / FPA / PIPE capital to a $X SPAC. Distinguish between (a) U.S. / Western institutional (T. Rowe, Fidelity, hedge funds), (b) Asia institutional (HashKey, Fenbushi, sovereign wealth), (c) crypto-native LPs (HTX, exchange treasuries), (d) PRC HNW family offices. **The S-1 absence of an anchor + PIPE indication after N months of registration is the operative answer**, regardless of headline credentials.

7. **Loaded reputational adjacencies** — board seat, advisory role, or business relationship with sanctioned / indicted / regulatory-flagged person or entity. Distinguish formal resolution status from live diligence flag status — Western LPs flag the adjacency regardless of formal case status.

8. **Career / credentials one-liner** — one sentence summarizing the career arc in the order it actually happened (origin → first job → ascent → current). Note loaded credentials the S-1 obscures by omission.

After each person's bullets, end Section 1 with an **aggregate team-level summary** as a markdown table covering: **prior SPAC roles by title** (e.g., "Chin: CEO of SKGR; Boehner: ID of SKGR; Payne: ID of SKGR + ID of HCAR-liquidated"); total SPAC deSPAC completions on team (with role specificity); total SPAC liquidations on team record (with role specificity); total verified non-SPAC exits across all team members combined (count them); total fund AUM actively deployed (not marketed); verified billionaires on team (Forbes-listed); combined PIPE-raise capability for the realistic target universe.

### Section 2 — Per-Person 9-Section Deep Dive

For each principal, produce the 9-section framework from Meteora's Individual Due Diligence Research Prompting Guide. Use these section headers verbatim:

- **§1 Identity & Career Foundation**
- **§2 Transactions & Exits**
- **§3 Fund Affiliations & AUM**
- **§4 Board Seats & Advisory Roles**
- **§5 Academic & Professional Credentials**
- **§6 Public Footprint & Media**
- **§7 Legal & Regulatory Background**
- **§8 Network & Association Mapping**
- **§9 Synthesis**

Within each section, render the prompt question as a markdown blockquote (`>`) above the answer. This makes the framework visible and the output self-documenting.

Section-specific drill-downs:

- **§1 Identity** — beyond standard bio, always include: Romanized Asian name disambiguation flag (Wikipedia / English version often a different person — note explicitly); hometown / origin (often telling); teenage wealth source; year of first completed undergraduate degree (note retroactive completion in late 30s if applicable); any university discrepancy across sources (S-1 vs Crunchbase vs MarketScreener).

- **§2 Transactions** — ALWAYS pull Bloomberg historical for any public-co operating tenure. Quote marketed AUM vs deployed AUM for any fund. Do not accept "founder of [fund]" framing without deployment figures. **For prior SPAC roles, role title (CEO, CFO, Executive Chair, sponsor manager, Director, IID, target operator) MUST lead each line — never bury inside a career-arrow chain.** Format: *"CEO of SKGR (2021-2025) → deSPAC'd to Webull/BULL 2025; BULL trades $7.32 today vs $10 deal price = -27% post-close. Warrants $2.34."* — NOT *"SK telecom Americas → SK hynix → SKGR → BULL"*. Distinguish target-operator roles ("Representative of East Asia Operations at USAR which deSPAC'd via IPAB 2025") from sponsor/director roles — operating roles at a target are weaker SPAC credentials than sponsor/director roles. For each prior SPAC, also report: was the deal completed within original term or after extensions? was the trust drawn down by redemptions before the deal closed (track redemption %)?

- **§3 Funds** — Always run SEC EDGAR `filer_cik` search on the SPAC CIK + on the person's name. Note absence of any SEC-registered investment vehicle. Offshore-only fund structure is itself a signal.

- **§7 Legal & regulatory** — Distinguish (a) personally clean from (b) institutionally entangled adjacency. Pull SEC litigation releases, Congressional concern letters, Trump-era settlement softenings.

- **§8 Network** — Always do a comp set positioning. For Asian crypto/AI sponsors, the "what is the co-founder of the same business doing now" comp is decisive.

- **§9 Synthesis** — End with explicit "Warrants further investigation" bullets. These feed Section 4.

Use bold lead-in fragments for parallel-structure bullets in §9 ("**Career trajectory**: …", "**Transaction history**: …", etc.) so readers can scan across people.

### Section 3 — Network Map & Cross-Person Linkages

Identify every undisclosed network bridge connecting two or more people on the team. For each bridge:
- Name the connection
- Describe time/place overlap
- Explain how it relates to the SPAC
- Note whether the S-1 discloses or obscures it

Look specifically for:
- **Cohort overlaps** — MBA / DBA programs, regional industry committees, professor-student relationships, ex-colleagues at multinational firms (e.g., AIA group 2013-2018; HKU DBA 2024+; NUS EMBA program)
- **Family office / fund affiliations** that connect IDs to the sponsor's network (e.g., ID employed at related family office of another principal — the highest-impact bridge type)
- **Underwriter cohort** — D. Boral / Maxim / AGP / EF Hutton each have characteristic SPAC cohorts following similar patterns

End with a **conflict landscape** paragraph: assess whether the realistic VECA target universe is sourced from the sponsor's own portfolio (Vernal Group / ABCDE Capital / family office), and whether the Audit Chair's independence is structurally compromised by network bridges.

### Section 4 — Red Flag Register

Markdown table (Category | Specific finding) covering all hits on the SPAC-extended red flag checklist (see Reference section below).

### Section 5 — Open Questions

8-12 prioritized questions for further investigation. Format as bullets. Cover:
- Why undisclosed transitions happened (departures, takeovers, mandate scrubs)
- Sources of personal capital sufficient to fund SPAC sponsorship without external anchor
- Recruitment pathway for each ID (which network bridge)
- Side-letter agreements (FPA, ROFR, transfer rights) that could surface at IBC announcement
- Short tenure flags at major institutions (planned vs terminated)
- Compensation expectations for non-equity, non-cash-pre-IBC ID seats
- Whether the realistic IBC target is sourced from the sponsor's own portfolio (insider rollup conflict)

---

## Output Format Conventions

- **Single chat response, copy/paste-ready, no separate file.** The user has been explicit about this.
- **Bold lead-in fragments** for parallel-structure bullets across people (lets the reader scan across §9 conclusions).
- **Blockquote (`>`)** to render the prompt question above each answer in the 9-section deep dives — this makes the framework visible.
- **Markdown tables** for: red flag register, Bloomberg performance summaries, ROA history, deployment ratios, aggregate team summary.
- **Italicize direct quotes** from interviews / industry press / X posts.
- **Always disambiguate Romanized Asian names** at the top of the relevant person's section if the Wikipedia / English-language version is a different person.
- **Section headers as `## H2`**, person headers within Section 2 as `## N. ROLE — NAME`, sub-sections as `### §N — Title`.
- **Bold the headline negative datapoint** in each person's bullets (e.g., **NOT on Forbes**; **-67% during tenure**; **Phase II abandoned at 10% deployment**).

---

## Tips for Better Results

**Always pull Bloomberg historical for any public-co operating tenure.** Single most informative signal in the framework. Use `MeteoraMCP:get-price` with the relevant ticker (e.g., 1611 HK Equity for Sinohope) and a date range covering the tenure window. Compute peak-to-trough during tenure + post-departure rally explicitly.

**Check Forbes for billionaire claims.** Search "[name] Forbes billionaire net worth" and check the actual Forbes Real-Time list, not Wikipedia. PRC crypto founders are routinely labeled billionaire in PANews / ChainCatcher / CoinLive without verification.

**Cross-reference universities across S-1 / Crunchbase / MarketScreener / Bloomberg / The Org.** PRC-citizen sponsors often have university disclosure inconsistencies (typical because formal degrees were completed retroactively). Note these explicitly without overstating.

**Compare original S-1 vs most recent S-1/A for mandate scrubs.** Geography target, industry focus, right/warrant economics. Mid-registration mandate dilution + right richening = weak demand requiring re-papering.

**Find the co-founder comparator.** For "Co-founder of [X]" framing, search "[other co-founder name] current role". The institutional gap between the two trajectories is often the cleanest signal.

**Probe HKU DBA / NUS EMBA / regional industry program networks.** Common recruitment pathways for ID slates that the S-1 doesn't disclose. Search "[Person A] [Person B] HKU DBA classmate" and similar.

**For uncompensated IDs**, ask why they took the seat. Document the most plausible recruitment bridge in §8 and the implication in §9.

**For "engineered CFO credential" pattern**, check whether the CFO's immediately prior role was taken in the 3-12 months before the S-1 was filed. A small-startup CFO appointment 5 months before S-1/A No. 3 is highly suggestive.

**For Asian sponsors**, the Justin Sun / TRUMP / WLFI / SEC adjacency is currently the highest-impact reputational live wire. House Democrats letter (Casten/Waters/Sherman, Sept 2025) is the operative flag, not the formal SEC dismissal.

**Memory-doc integration.** After producing the output, append the synthesis as an entry to the SPAC's memory doc via `MeteoraMCP:update-memory-doc` (tag: `diligence`). The Executive Summary section (1) is the most-quoted section in subsequent work — make it scannable.

---

## Reference: SPAC-Extended Red Flag Checklist

Standard checklist (from firm's Individual Prompting Guide):
- Unexplained career gaps >12 months
- Firms that no longer exist with no explanation
- Claimed deal credits that don't appear in public records
- AUM figures inflated relative to team size or strategy
- FINRA, SEC, or court records (personal)
- Board roles at companies that subsequently failed or faced fraud allegations

SPAC-specific extensions:
- Material undisclosed mandate change (compare original S-1 vs most recent amendment)
- Auditor turnover during pre-IPO registration (especially with going-concern carryover)
- Material undisclosed entity transition (rebrandings, name changes, post-departure ownership changes)
- Prior public-co operating tenure with verifiable shareholder value destruction (Bloomberg-confirmed, especially with post-departure rally)
- **Prior SPAC role obscured by ambiguous title** — e.g., "served on the board of [SPAC]" where the person was actually the CEO; "advisor to [SPAC]" where the person was actually the sponsor manager. Always cross-reference the prior SPAC's S-1 / proxy / 8-K to verify role title.
- **Prior SPAC liquidation on team record** — flag every team member who was on the board (any role) of a SPAC that liquidated, with explicit role title.
- **Post-deSPAC underperformance on prior SPAC** — for any team member with a prior completed deSPAC, pull current Bloomberg price and report % from $10 deal reference. >20% drawdown is a flag; >50% is a severe flag.
- Missing operating responsibilities (e.g., Layer 1 / fund / portfolio company launched under their tenure that subsequently went to zero — and is absent from the S-1)
- Material undisclosed network conflict (ID employed at related family office / fund of another principal)
- Forbes-list absence despite "billionaire" framing in industry press
- AUM marketed vs deployed gap >50% (Phase II abandonment signal)
- Mid-registration right/warrant economics richening (>2x value of embedded option)
- D. Boral / Maxim / AGP / EF Hutton sole UW with offshore PRC-tied team (cohort signal)
- Sponsor admin fee structure routing material cash flow to a CEO-controlled entity over the IBC window
- Single-class founder share concentration where one principal holds >75% of founder pool

---

## What This Skill Replaces

This skill replaces ad-hoc team writeups, S-1 bio paraphrasing, and "looks credible to me" SPAC team analysis. The framework is the entire point — it forces a reckoning with Bloomberg-confirmed operating performance, Forbes verification, deployed AUM, and S-1 omissions that ad-hoc analysis routinely misses.

Always use this skill for SPAC team diligence — do not produce ad-hoc bios. Consistent framework application across deals is what makes the comparison set useful.
