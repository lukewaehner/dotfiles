# In-Deal Executive Summary — Canonical Template + Target Research Methodology

This file is the **single source of truth** for the in-deal executive summary. It is shared, verbatim, by both paths that produce an in-deal doc:

1. **Seed Mode, in-deal stage** (doc does not exist; the SPAC is already in-deal when first seeded) — composed at Seed Mode Step 4.5.
2. **Deal Transition Mode** (doc already exists, was seeded pre-deal, and the SPAC has just announced a BCA) — composed at Phase D Step D.6.

Both paths read THIS file and compose the summary to THIS template. The only difference between them is mechanical: Seed builds the doc from scratch (Pillars 1–6 all fresh); Transition appends the in-deal pillars (4–6) to an existing pre-deal doc and rebuilds the summary wholesale. The content focus, section list, and research depth are identical. Do not maintain a second in-deal template anywhere; if the in-deal summary needs to change, change it here.

---

## Part 0 — The focus shift (why the in-deal summary is a different document)

A pre-deal summary answers: *is this a credible blank check, and can this sponsor source and close a deal?* Sponsor quality is the lede because the deal does not yet exist — deal-sourcing capability and PIPE-raising track record are both load-bearing.

Once a BCA is announced, the deal exists. Deal-sourcing capability is now spent history — it told us nothing we can still trade on. The summary re-centers on **the deal itself**: what the target is, what it is worth, what the terms are, and whether the numbers hold up. Per **Core Principle 20**:

- **The target is the lede.** What the company does, its history since inception, its financials, its funding history, its comparable companies, and the valuation the deal implies are the center of the document.
- **Sponsor coverage collapses to PIPE-raising track record only.** The only forward-looking sponsor question in-deal is: *can they raise / have they raised the capital to close this deal at the minimum-cash threshold?* Keep the sponsor's demonstrated PIPE / committed-financing / anchor track record (graded per CP16 / the OUTCOMES-RUBRIC memory doc). Drop deal-sourcing narrative, drop the full director-by-director slate (move it to a one-line board-composition note), drop network-map color that bore only on origination. The sponsor section becomes short and financing-focused.
- **Management diligence moves to the TARGET operating team.** Pre-deal, "management" meant the sponsor principals. In-deal, the people who matter are the operators who will run the public company. Bio the target's CEO/CFO/founders the way pre-deal bios covered sponsor principals.

Everything else that governs the pre-deal summary still applies: evergreen / no tape characterization (CP11, including sub-rules a/b), no editorial color (CP18), plain language with jargon defined on first use (CP19), standing-protocol restraint for unheld legs (CP17), 9.9% concentration threshold (CP15), bucket quoted verbatim from the sheet (CP9), and prior-deSPAC outcomes graded per the OUTCOMES-RUBRIC memory doc (CP16).

---

## Part 1 — Target Dossier research methodology (Pillar 6)

The in-deal summary's target-centric sections are only as good as the underlying research. Before composing the summary, build the **Target Dossier** (Pillar 6) by working the sources below in order. Capture findings as a tagged `diligence` entry (see SKILL.md Step 4.4d / Step D.5); the summary distills from it.

### 1.1 — Primary filings (always first)
- **S-4 / F-4** (if filed): the "Information About [Target]", "[Target]'s Business", "Management's Discussion and Analysis of [Target]", "Background of the Business Combination", "Certain Relationships and Related Party Transactions", and "Beneficial Ownership" sections are the spine of the dossier. Pillar 4 (`spac-s4-extraction`) already pulls deal terms and target operating financials; Pillar 6 goes deeper on company history, cap-table lineage, and the pre-deal ownership table. Locate the S-4/F-4 via the **CP22 3-pass discovery** - critically, for foreign-private-issuer / offshore targets (Cayman / BVI / PRC) the F-4 is filed under the new listing holdco or merger-sub registrant's CIK, NOT the SPAC's, so resolve that CIK from the BCA and search it before ever concluding the financials are unavailable. Treating a holdco-filed F-4 as "no F-4 / data gap" is the failure this methodology exists to prevent.
- **The BCA 8-K + investor presentation (Ex 99.1 / 99.2)**: when no S-4 is filed yet, this is the primary source. The investor deck is where management's own comps, projections, TAM framing, and funding-history timeline live — capture them, but treat projections and self-selected comps skeptically (they are the bull case, not a neutral valuation).
- **Target's own SEC history if any** (prior registrant, Reg A, S-1 that was withdrawn, 10-Ks if formerly public): pull via `MeteoraMCP-AWS:edgar-filings` on the target's CIK.

### 1.2 — Company since inception (filings + internet)
Reconstruct the company's history from founding to today. Source from the S-4 business section first, then web search to fill gaps:
- Founding year, founders, founding thesis / original product.
- Pivots, rebrands, name changes, M&A the target itself did.
- Key commercial milestones (first product, first major customer, regulatory approvals, key partnerships).
- Headcount / scale trajectory if disclosed.
- Web queries: `"<Target name>" founded history`, `"<Target name>" raises Series`, `"<Target name>" funding`, `"<Target name>" CEO`, `"<Target name>" competitors`, `"<Target name>" valuation`.
- This is the narrative backbone of the **Target overview** section — a reader should finish it understanding what the company is and how it got here.

### 1.3 — Past funding rounds (capital history)
Build the private financing history: each round by type (seed / Series A/B/C/… / venture debt / bridge), amount, date, post-money valuation if disclosed, and named lead/notable investors. Sources: S-4 "Background" + related-party + beneficial-ownership tables (which often name the VC/PE holders and their share counts), the investor deck, and web search (PitchBook/Crunchbase-style coverage, press releases, TechCrunch/Axios/Bloomberg round announcements). Two things matter most for the valuation read:
- **The last private round's post-money** vs. the deal's implied equity value — is the deSPAC a markup, a flat round, or a down round vs. the last private mark?
- **Which crossover/institutional investors are on the cap table** and whether they are rolling equity or being cashed out (rollover = conviction signal; full cash-out = the opposite).

### 1.4 — Comparable companies (comps)
Identify 4–8 public comparables on business model, sector, growth, and margin profile — NOT just the deck's hand-picked list (note where the deck's comps are flattering and add honest ones). For each comp capture the metric that matters for the vertical:
- Revenue-multiple businesses (software, marketplaces, pre-profit growth): EV / NTM revenue (and EV / LTM revenue).
- EBITDA businesses (industrials, services, mature): EV / EBITDA.
- Sector-specific where appropriate (EV / production for resources, EV / ARR for SaaS, price / book for financials, EV / reserves for energy).
- Pull live comp multiples via `MeteoraMCP:get-price` / `MeteoraMCP:get-company-info` where the comps are liquid tickers; otherwise web-source recent multiples and date them.
- The comp set defines the valuation envelope the deal should be measured against.

### 1.5 — Related companies / spin-out / carve-out lineage
Establish whether the target is independent or has a corporate parent / sibling lineage:
- Is it a **spin-out or carve-out** of a larger company (a division, a subsidiary, a university/lab spinout, a JV)? If so, name the parent, the carve-out terms, what IP / contracts / people came with it, and what dependency on the parent remains (TSAs, supply agreements, licensing-back).
- Are there **affiliated or sister entities** (common founder, common controlling shareholder, a SPAC sponsor that also holds the target privately, a holdco structure)? Related-party sections in the S-4 are the primary source.
- Are there **direct strategic relationships** with the comps (the target is a supplier to / customer of / former unit of a public comp)? This sharpens both the comp read and the conflict map.
- Spin-out lineage frequently explains the cap table, the funding history, and the IP position in one stroke — resolve it explicitly rather than treating the company as if it sprang up independently.

### 1.6 — Basic valuation (assemble the inputs, then frame)
The goal is not a precise DCF — it is enough to judge whether the deal is cheap, fair, or rich versus comps and versus the last private round. Assemble:
- **Implied deal valuation**: pre-money equity value, enterprise value (equity + debt − cash, pro forma for the trust + PIPE), and the implied per-share basis.
- **Target operating metrics**: last full-year and most-recent-interim revenue, gross margin, EBITDA / operating loss, cash burn, runway; plus the projection years management is selling (label them clearly as projections).
- **Implied multiples**: deal EV / (LTM and NTM) revenue or EBITDA as appropriate, set beside the comp envelope from 1.4.
- **The markup read**: deal implied equity value vs. last private post-money (1.3).
- **Frame in one paragraph**: where the deal prices relative to comps and to the last private round, and what has to be true (growth, margin) for the deal valuation to be reasonable. State it factually; do not cheerlead and do not editorialize (CP18). If projections are doing all the work to justify the multiple, say so plainly.

---

## Part 2 — In-deal executive summary template

Compose the summary to this exact section order. **The in-deal section list is closed** (this replaces the pre-deal closed list for in-deal docs — see CP11 sub-rule (b)): One-line view, Deal terms, Target overview, Company history, Funding history, Comparable companies, Related companies / lineage, Valuation, Pro forma capitalization, Target management, Sponsor — PIPE-raising track record, Relationships & Coverage, Structure (SPAC mechanics), Risk Factors / Atypical Features, Filing track, Position, Trade view, On the horizon. Do not add Verdict Block / At-a-glance / Snapshot / TLDR / warrant- or SPAC-cohort blocks / any extra wrapper (CP11 sub-rule (a)/(b)); brief compressions go in the One-line view.

```markdown
## Executive Summary

**[TICKER] — [Full SPAC Name] / [Target Name] business combination ([Exchange]; SPAC domicile [—]; SPAC CIK [10-digit]; in-deal; [BCA announced <date> / S-4 filed <date> / DEFM14A <date>]; [Pro forma ticker if announced])**

**One-line view:** Bucket [<sheet bucket from MeteoraMCP-AWS:spac-details, verbatim>] — [Target] ([one-clause description of what the company does]) via [SPAC]. Deal implies [~$X EV] at [~Y× metric] vs. comps at [~Z×]; [markup / flat / down] to last private round of [$P post-money]. [Durable one-phrase deal thesis — the desk's standing thesis when one exists (CP21: human view leads), else your synthesis — e.g. "rich to comps on projections that require a 3× revenue ramp; rights/common a sell into strength."] NO trading characterization here, even briefly (CP11).

**Deal terms:**
- Structure: [stock-for-stock / cash-and-stock / SPAC-merges-into-target]; pro forma [PubCo name + ticker].
- Consideration / exchange ratio: [equity value $; per-share basis; exchange ratio mechanics].
- Minimum cash condition: [$amount]; redemption backstop / non-redemption agreements: [terms]; current redemption exposure if known.
- Earnouts / contingent shares: [tranches, triggers, $ thresholds].
- Sponsor promote treatment in the deal: [forfeiture, earnout-conversion, vesting tied to price — note any sweetener given to close].
- Lockups: [target holders / sponsor — duration + early-release triggers].
- Termination / outside date: [date]; break fee; key closing conditions.
- [Define every non-obvious term inline per CP19.]

**Target overview:** [2–4 sentences: what the company does, the product, the business model, who pays it, what stage it is at (pre-revenue / scaling / profitable). The reader should understand the business before the numbers.]

**Company history:** [Founding year + founders + original thesis through to today — pivots, rebrands, milestones, regulatory approvals, key customers/partnerships. Sourced from S-4 business section + web per Part 1.2. Durable; no tape.]

**Funding history:** [Each private round: type, amount, date, post-money if disclosed, named lead/notable investors — per Part 1.3. Call out the last round's post-money explicitly and whether marquee holders are rolling vs. cashing out.]

**Comparable companies:** [4–8 honest comps with the vertical-appropriate multiple each, dated — per Part 1.4. Note where management's deck comps are flattering and what you added. Include desk-originated relative-value cross-reads WITH attribution per CP21 — e.g. "hardware OEM (Elroy) vs software autonomy (Merlin) is the live desk debate (Vik, 6/26)" — human framings are carried forward, not replaced by your comp set.]

**Related companies / lineage:** [Spin-out / carve-out parent + carve-out terms + residual dependencies; affiliated/sister entities; strategic relationships with comps — per Part 1.5. If genuinely independent with no lineage, say so in one line.]

**Valuation:** [Implied EV + implied multiples set beside the comp envelope; markup/down vs. last private round; target operating metrics (LTM/interim revenue, margin, EBITDA/loss, burn, runway) vs. the projections management is selling (labelled as projections); one-paragraph factual frame of cheap/fair/rich and what must be true — per Part 1.6.]

**Pro forma capitalization:** [Pro forma share count; ownership splits (target rollover %, SPAC public %, sponsor %, PIPE %); fully-diluted incl. warrants/earnouts; pro forma cash (trust net of redemptions + PIPE) and debt; implied pro forma EV.]

**Target management (substantive bios — the operators who will run the PubCo):** [One multi-sentence bullet per key operator — CEO, CFO, founders, key technical/commercial leads. Per person: role + tenure; prior operating track record (named companies, exits, public-co tenure with ticker/performance); domain credibility; red flag if any (litigation, prior blow-ups, related-party conflicts) or "clean." This is where management diligence lives for in-deal docs — give it the depth pre-deal bios gave sponsor principals. Cut color per CP18.]

**Sponsor — PIPE-raising track record:** [SHORT and financing-focused per CP20. The committed financing already raised for THIS deal (PIPE size, named anchors, FPAs/backstops, convertible) and the sponsor's demonstrated capital-formation track record graded per CP16 (named prior closing PIPEs + sizes + redemption backdrop + anchors; factual record only — no speculative capability ratings; `no prior closing PIPE on record` stated neutrally when that is the fact, per CP24). Board composition in ONE line ("board: N directors, [chair]; full slate in Pillar 3"). Do NOT restate the full director-by-director slate or deal-sourcing narrative — that lived in the pre-deal summary and the Pillar 3 entry; in-deal it is not the lede.]

**Relationships & Coverage:** [Per CP23. Deal / sell-side coverage: bank(s) that ran the SPAC, the target-side financial advisor / who reps the target, the PIPE placement agent, and which sell-side desks cover Meteora on the deal (StoneX / Cantor / Clear Street / BTIG / Jefferies / etc.). Named contacts — person, role/affiliation, email domain where known. Sponsor / cross-name linkage — other SPACs sharing this sponsor or a sponsor-adjacent contact set. Introduction / relationship status, dated. Underwriter/advisor come from the S-1 and the S-4 "Background of the Business Combination"; named-contact and intro intel come from desk IB exchanges and are attributed with name + date (CP21). Durable facts evergreen; workflow items dated; NO tape — coverage ("BTIG runs the SPAC and reps the target") belongs here, posture ("our offer at 10.90") does not (CP23 sub-rule (b)). Omit gracefully to a single line if nothing beyond the underwriter/advisor is known (CP23 sub-rule (c)).]

**Structure (SPAC mechanics):** [Condensed from the pre-deal structure section — unit composition, trust $/share, deadline + extension cadence, promote size. One compact block; the deal terms above carry the action.]

**Risk Factors / Atypical Features ([N]):** [Deal-specific, material, differentiating — per CP12/CP13. In-deal, the richest findings are deal-level: down-round vs. last mark, projection-dependent valuation, thin minimum-cash cushion vs. likely redemptions, related-party conflicts in the BCA, a sponsor sweetener given to close, IP/parent dependency from a carve-out, going-concern on the target beyond the SPAC norm. Each finding ends in "...unlike [norm / comp / prior sibling]." Universal SPAC features are not findings.]

**Filing track:** [BCA 8-K date → S-4/F-4 → S-4/A amendments → DEFM14A → vote date. Note redemption deadline and any extension proxies. EDGAR-verified S-4/F-4 count (3-pass: SPAC CIK + PubCo CIK).]

**Position:** [Common / rights / warrants share counts; ~% of public float (CP15 — flag only ≥9.9%); dollar mark omitted (lives in timestamped Pillar 2).]

**Trade view:** [Durable, thesis-driven, deal-aware view that survives a 6-month re-read. Standing-protocol restraint per CP17 — no rec on unheld legs. e.g. "Sell rights into strength; common a redeem-or-sell vs. thin minimum-cash cushion; no warrant position." No tape-dependent claims. This is the standing home for carried-forward human/desk theses (CP21): restate every live desk view with attribution and date — e.g. "desk view (Vik, 6/26): Elroy = hardware OEM vs Merlin = software autonomy; hardware may command more public-market value — bear cross-read asks why buy this when MRLN screens cheaper." Human argumentation leads; your synthesis follows it.]

**On the horizon:**
- [Next gating event — S-4 effectiveness, vote date, redemption deadline, outside date — define jargon inline.]
- [Open valuation/diligence questions to monitor — e.g. "confirm PIPE anchors named in next S-4/A"; "redemption level at vote vs. $X min-cash."]
- [Data gaps from this pass — e.g. "Pillar 4 deferred pending S-4 filing; refresh when filed."]
- [Bucket revision ONLY if the desk explicitly directed one in a transcript / email captured in the doc — recorded with attribution per CP9/CP21; Claude does not propose revisions.]
```

### Composition notes
- **CP21 carry-forward governs every composition and re-composition of this template:** before composing, inventory the human-authored content in the existing summary + entries (attributed desk views, theses, pair-trade framings, open debates); after composing, verify item by item that every live view landed in a canonical section with attribution. Retired views are logged in the transition/correction entry, never silently dropped. Human views outrank Claude synthesis on any disagreement.
- **Evergreen test still governs:** every section must read ~95% accurate in 6 months barring a new amendment or the vote. Live redemption levels, today's spread, current yield → Pillar 2, not here. Deal terms, valuation framing vs. comps, company history, funding history are all durable.
- **Length:** in-deal summaries run long because the target research is substantive — 2,000–3,000 words is normal and correct when the company has a real history, multiple funding rounds, and a populated comp set. Do not compress the target sections to one-liners; that is the in-deal analog of the pre-deal failure mode of compressing the sponsor track record.
- **Markdown → HTML email:** the in-deal section headers map to `<h3>` exactly as the pre-deal headers do (SKILL.md Step 4.6 conversion rules apply unchanged); the identifier line maps to `<h2>` + metadata `<p>`.
