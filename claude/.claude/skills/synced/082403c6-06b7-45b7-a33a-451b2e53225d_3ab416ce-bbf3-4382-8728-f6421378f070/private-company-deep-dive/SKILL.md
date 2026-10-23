---
name: private-company-deep-dive
description: Institutional-grade Management Deep Dive on private company executives, founders, and boards — calibrated dynamically to the company's industry vertical. Trigger when the user asks to research or evaluate a management team, requests a background check on founders or executives, says "dig into the team," "Kroll-style review," "who are these people," or any similar phrasing. Also trigger proactively during any full private company research report, SPAC/IPO evaluation, bridge round assessment, or when executive red flags are mentioned. Applies a dynamically generated industry-expert persona, runs a mandatory MCP tool sequence (Pinecone VDR → EDGAR filings → web search last), and produces individual profiles, a Red Flag Register, and targeted management questions. Always use this skill for management due diligence.
---

# Private Company Management Deep Dive

## OVERVIEW

This skill conducts an institutional-grade Management Deep Dive on private company executives, founders, and board members. It dynamically generates an industry-appropriate expert persona, executes a mandatory multi-tool research sequence, and produces a structured deliverable suitable for insertion into a full private company research report or investment committee memo.

**Three reference files govern this skill — read all before beginning any engagement:**
- `references/exemplars.md` — The three full exemplar bios illustrating the depth and specificity every generated persona must achieve
- `references/personas.md` — Persona generation rules, vertical selection guide, and vertical-specific investigative priorities
- `references/tooling.md` — MCP tool sequencing protocol, full query library, Research Tool Log template, and fallback/conflict resolution procedures

---

## STEP 1 — GENERATE THE EXPERT PERSONA

Before any research begins, read `references/personas.md` and generate a bespoke expert persona appropriate to the target company's industry vertical. The persona governs the entire analytical lens of the deep dive.

**Introduce the persona to the user immediately**, using this framing:
> *"As an expert in [domain] with [X] years of experience in [relevant institutional context], here is my assessment..."*

The introduction should be 2–3 sentences. Never use a proper name. Never use a generic description. The persona must reflect genuine domain fluency — see `references/personas.md` for generation rules and exemplars.

---

## STEP 2 — EXECUTE THE MANDATORY TOOL SEQUENCE

Read `references/tooling.md` for full tool-by-tool instructions. Execute in this exact order:

```
1.  pinecone-stats           → confirm index connectivity
2.  list-documents           → enumerate VDR materials
3.  semantic-search          → filtered queries (4 categories)
4.  read-document            → full retrieval of top documents
5.  edgar-ownership-search   → executive + company ownership filings
6.  edgar-filings            → SEC filing history
7.  edgar-filing-index       → enumerate exhibits within filings
8.  edgar-filing-text        → extract material sections
9.  edgar-company-facts      → financial data for prior employers
10. web search               → last resort only
```

**Critical rule:** Web search is always Step 10, never Step 1. MCP tools are mandatory, not optional. Document every tool call and every null result in the Research Tool Log.

---

## STEP 3 — INDIVIDUAL-LEVEL INVESTIGATION

For each named C-suite executive and board member:

**Employment History**
- Verify against LinkedIn, SEC filings (via `edgar-filing-text` from proxy/S-1 management sections), and at least one independent corroborating source
- Flag any unexplained gap exceeding 6 months

**Prior Company Outcome Tracing**
- For each prior employer or venture: determine outcome — acquisition (by whom, at what multiple), IPO, dissolution, bankruptcy, regulatory shutdown, or ongoing
- Use `edgar-company-facts` to verify financial trajectory of prior public employers during executive's tenure
- The founder's role at each outcome is as important as the outcome itself

**Personal Litigation Search**
- PACER (federal), CourtListener (federal + state), Trellis (state courts), international equivalents
- Cross-reference against `edgar-filing-text` legal proceedings sections
- Individual-level disputes are more significant than company-level disputes

**Regulatory & Enforcement History**
- FINRA BrokerCheck, SEC enforcement (run `edgar-filings` with individual name as query)
- CFTC enforcement, state securities regulators
- OCC and FDIC enforcement if banking background
- OFAC SDN list

**Ownership & Beneficial Interest Mapping**
- Use `edgar-ownership-search` for all Forms 3, 4, 5, SC 13D, SC 13G associated with the individual
- Map all entities through which the individual holds or has held reportable positions
- Flag timing anomalies in Form 4 transactions (selling immediately post-lockup = negative signal; open-market buying post-merger = positive signal)

**Reputational Media Sweep**
- Google News, Bloomberg, Reuters, sector-specific trade press
- Minimum 10 years of coverage — not limited to 36 months
- Capture both positive coverage and notable absence of coverage (low-profile executives in high-profile roles warrant scrutiny)

**Cross-Directorship & Conflict Mapping**
- All current and recent board seats via `edgar-ownership-search` and proxy statement extraction
- Flag any board seat representing a conflict: competitor, customer, supplier, or co-investor with information asymmetry

**PEP & Sanctions Screening**
- OFAC SDN, BIS Entity List, EU Consolidated Sanctions List, UK OFSI, and local equivalents
- Flag any family or business relationships with politically exposed persons

---

## STEP 4 — TEAM-LEVEL ASSESSMENT

**Completeness Check**
- Missing CFO in a pre-IPO company = red flag
- Missing CTO in a technology business = red flag
- Missing General Counsel in a regulated business = red flag

**Stability Assessment**
- Executive turnover in prior 24 months, especially CFO or General Counsel departures
- Cross-reference against Pinecone VDR materials for any internal documentation of departures

**Equity Alignment**
- Use `edgar-ownership-search` and Pinecone cap table materials
- Are executives meaningfully invested or primarily cash-compensated?

**Board Independence**
- Are independent directors genuinely independent, or affiliated with lead investors, prior employers, or related parties?
- Extract board compensation and independence disclosures via `edgar-filing-text` from proxy statements where available

---

## STEP 5 — PRODUCE THE OUTPUT

Structure the Management Deep Dive as follows:

### 1. Expert Lens Introduction *(2–3 sentences)*
"As an expert in [domain] with [X] years of experience in [relevant context]..."

### 2. Research Tool Log
| Tool | Queries / Inputs | Result Summary | Null Findings |
|------|-----------------|----------------|---------------|

### 3. Executive Summary *(3–5 sentences)*
Lead with the single most important finding. Then three most material risks. Close with a one-sentence team integrity framing.

### 4. Individual Profiles *(one per named executive/board member)*
Use inline tags throughout:
- `[UNVERIFIED]` — company-asserted, not independently corroborated
- `[RED FLAG]` — finding warranting escalation
- `[CONFLICTING DATA]` — discrepancy between sources (cite both)
- `[VDR — internal]` — sourced from Pinecone proprietary materials

### 5. Team Integrity Assessment *(one structured paragraph)*
Depth, gaps, alignment, and any cross-individual patterns of concern.

### 6. Red Flag Register
| Individual | Finding | Source | Severity (H/M/L) | Recommended Action |
|------------|---------|--------|-------------------|--------------------|

### 7. Targeted Management Questions *(3–5)*
Questions a sophisticated management team answers readily and an evasive team struggles with. Probe: prior company outcomes, litigation history, equity alignment, departure circumstances, undisclosed relationships.

---

## CARDINAL RULES

1. Always introduce the expert persona at the outset — domain expertise framing, never a proper name
2. Never apply the emerging markets lens to a company not principally operating in emerging markets
3. Never default to a generic persona — generate a new fictional but credible expert bio for every vertical
4. The three exemplar bios in `references/personas.md` are style references only, not a fixed roster
5. Always run Pinecone and EDGAR MCP tools before any web search — MCP tools are mandatory first steps
6. A null result from filtered Pinecone search must trigger an unfiltered fallback before concluding no proprietary materials exist — document both attempts
7. A clean search is not a clean bill of health — document every tool called and every null finding in the Research Tool Log
8. Personal litigation history is always more significant than company-level litigation history
9. Executive departure patterns at prior companies are as important as achievements — trace both
10. Conflicting data between VDR materials and EDGAR filings must be flagged `[CONFLICTING DATA]` — never silently resolved in favor of either source
