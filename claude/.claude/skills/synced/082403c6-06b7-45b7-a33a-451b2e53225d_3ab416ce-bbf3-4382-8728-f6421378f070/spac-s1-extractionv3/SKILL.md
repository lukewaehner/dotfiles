---
name: "spac-s1-extractionv3"
description: "Meteora's primary SPAC S-1 IPO extraction (v3) — a 'Read on top, lean facts below' workup. Trigger on any SPAC S-1/S-1A/F-1 or prospectus PDF, or 'extract', 'run the S-1', 'analyze this S-1', 'pull the terms', 'S-1 review', 'run the guide', 'new S-1', 'just filed', 'what's the read on this S-1', 'desk read', or a filing dropped with no instructions. Leads with a Snapshot + sponsor-first Desk Read that benchmarks the team against a NAMED gold-standard Tier 1–5 ladder (Tier 1: dMY/Harry You, Gores, Cantor/Lutnick, Cohen–Columbus Circle, Eagle/Sagansky–Sloan, Inflection Point, Spring Valley, CC Capital/Chinh Chu; Tier 2: Yorkville, M3-Brigade; watch: Pyrophyte) and names who the sponsor is a 'poor man's version of' or equivalent to, then bombs, anchor/sponsor, underwriting, sector fit, then a lean figures-only extraction. Grades are a single number 1–5 where 1=best, matching our Tier scale. This is the firm's standard S-1 tool."
---

# SPAC S-1 Extraction (v3 — Read on top, lean facts below)

## Overview
Two halves, printed top-down so a PM gets the judgment first and the raw record last:
- **THE READ** — a Snapshot and a sponsor-first Desk Read. Opinionated; the value-add. Assessment, benchmarking and a verdict are *wanted* here.
- **THE FACTS** — a lean, reordered extraction. Figures and facts only, each stated **once**, no assessment, no fluff.

Output in the chat body as structured text — no files unless asked. (When it goes out as an **email**, see the Delivery section — it must be HTML, not raw markdown.)

**Canonical print order** (write the Read last, print it first):
1. Snapshot 2. Desk Read 3. Overview & Offering 4. Management & Board (team — moved up) 5. Bombs / Key Deviations 6. Anchor & Sponsor 7. Underwriting & Fees 8. Sector Fit 9. Private Placement & Promote *(detail)* 10. Lockup *(detail)* 11. Target *(detail)* 12. Advisors & Service Providers *(detail)*

Why: the old extraction buried the two things a PM reads — who the sponsor is and what's non-standard — under repeated boilerplate. v2/v3 say each fact once, lead with the read and the deviations, drop counsel/auditor trivia to the bottom. v3's upgrade is the sponsor benchmark: a named Tier 1–5 ladder and a "who are they a poor man's version of" call, because the whole point of a benchmark is to place the team against people who *actually deliver*.

## Workflow
1. Read the S-1 (`pdftotext -layout` on an uploaded/emailed PDF, else EDGAR).
2. Assemble THE FACTS — strictly from the filing.
3. Cross-reference for THE READ — prior vehicle(s) status (EDGAR); PIPE investor capacity (Form ADV RAUM/13F); underwriter tier/switch; and when Outlook is available, search the mailbox for the sponsor + principals for prior interactions. Consult Appendix A (tiers) + B (voice).
4. Write THE READ, then print in the canonical order. One response if length allows; else stop at a break and say "continue."

## Output discipline — applies to THE FACTS, not the Read
- **Report, don't assess.** State the figure; don't call it strong/thin/attractive. Assessment belongs only in the Read.
- **Figures over sentences.** Structure is an equation: `1U = 1S + 1/7R (no warrants)`.
- **Say each fact once.** The Snapshot is the only headline digest; the detail adds *new* granularity or isn't there.
- **Abbreviate.** Domicile `KY`/`DE`/`BVI`; exchange `Nasdaq`/`NYSE`/`OTC`; filing `S-1` (drop "preliminary") + date `7/7/2026` + `reg stmt filed, not yet effective` if pre-effective.
- **Omit empty fields; don't report the absence of a term.** Reserve "Not disclosed." for fields where absence is material (deferred fee, promote, trust mechanics).
- **Don't infer or extrapolate.** Don't spend lines on standard terms (15% cap, $100k dissolution, standard anti-dilution, 15% OA).
Quoting verbatim (anti-dilution ratchet, variable deferred-fee provision) is required where noted.

## Delivery — chat vs. email are different render targets
The markdown this skill produces (`#` headers, `===`/`---` dividers, `|` pipe tables) renders in **chat** but shows up as a wall of **raw text in an email body**. So:
- **In chat:** markdown is fine — print as above.
- **In an email:** render the workup as **HTML** — real `<h2>` section headers, `<ul>/<li>` bullets, and `<table>` for the sponsor-tier matrix and the Management & Board roster. Set `body_is_html=true` / `content_type=HTML`. **Never** send the markdown/`===`/pipe-table version as a plain-text email.
- **Sender identity:** send internal desk notes from the intended person's own mailbox (Vik's Outlook / send-as-me connector = `vik@`), **not** a shared/relay account. If a send connector reports "not signed in," re-verify (`whoami`/retry) before concluding it's down — never silently send under a different identity; if you can't send as the intended sender, stop and confirm rather than relaying as someone else.
- **Thread:** post as a **reply on the existing internal chain** (reply-all to Filings@), keeping the thread; don't start a new one.
- **Pre-send self-check:** (1) sender = intended identity, (2) body is HTML (not raw markdown), (3) replying in-thread.

# THE READ (write last, print first)

## Snapshot
One tight block:
- **[SPAC Name] · [Unit/Share/Warrant/Right tickers] · S-1 · [M/D/YYYY] · CIK [x]**
- **Structure:** [equation] · **Size:** [N × $10.00 = $Xmm] · **Trust:** [$/unit; +excess if any] · **Promote:** [% — flag if off 25%, either way] · **Underwriter:** [name + tier]
- **Prior Meteora interactions:** [what Outlook shows on the sponsor/principals — or "none found / not checked"]
- **Sponsor tier:** [Tier 1–5, half-tiers OK] vs. [the archetype-matched comp] — [one clause: "≈ [comp]" or "a poor man's [comp]"]
- **Verdict:** [one line — the call and the single thing not to credit]

## Desk Read
Voice per Appendix B: an experienced SPAC PM briefing the desk — plain, skeptical, specific, `=` for "which means," real-vs-optical, no laundering the sponsor's framing.
1. **Who's running this.** Lead with the sponsor; connect career history → prior SPAC outcomes → board → access to capital. Name the edge or its absence.
2. **Sponsor vs. the gold standard.** Matrix from Appendix A, scored against **the tier-1 comp whose archetype matches** — pick from the named ladder (repeat tech/growth→dMY; PE-serial→Gores; bank-stack→Cantor; proprietary-flow house→Cohen/Columbus Circle; media/consumer operators→Eagle; fund-manager America-First/hard-tech→Inflection Point; nuclear/deep-tech sector operator→Spring Valley; billionaire-PE principal→CC Capital). **Do not default to dMY.** Then the payoff line every PM wants: **who is this team a "poor man's version of," or who are they equivalent to** — e.g. "a poor man's Eagle: real studio operators, but no de-SPAC record and a boutique book." State the tier (half-tiers fine) and how far off.
3. **The tells.** 3–6 short paragraphs, each: *what it is = why it matters = real or optical.*
4. **Net.** What to credit, what to discount, what to ask, the actionable lean.
Keep the Read a screen or two — judgment, not a re-listing of the facts.

# THE CALL (decision-useful; lean)

## Overview & Offering
- **Domicile** [KY/DE] · **Exchange** [Nasdaq/NYSE] · **Filing** [S-1, M/D/YYYY; reg stmt filed, not yet effective] · **HQ** [city]
- **Description** — one line
- **Structure** — equation: `1U = 1S + 1/7R (1/7 → 1 Class A at IBC) (no warrants)`
- **Units Offered** — `N × $10.00 = $Xmm`
- **Trust** — `$10.00/unit` (append `(+$0.0X)` if overfunded); **Trustee** [name]
- **Timeline** — `24 months, no automatic extension` (state extensions only if non-standard). *(OA is a standard 15% — omit unless it differs.)*

## Management & Board
Team moved up. Table: `Name (age) | Role | Background (facts) | Prior SPAC / affiliation (with outcome)`. Then one line each: **PIPE intent**, **BC criteria** (brief), **Committees** (+chairs). Depth welcome here, as facts not characterization.

## Bombs / Key Deviations
Material deviations, stated as facts with figures; the *why* lives in the Desk Read. `**Bomb:**` prefix. Flag both directions:
- Downside: divided fiduciary duty (name who owes duties to which entities + mandate overlap); CEO with no completed prior SPAC; promote >25%; trust withdrawals beyond taxes; automatic (non-vote) extension; China exposure; back-loaded/variable/discretionary UW economics; thin WC; uncapitalized/non-binding PIPE; tier-3 sole book.
- Upside (`**Positive:**`): promote <25%; overfunding; minimal upfront UW; low-dilution (right-only/no warrants).
Don't flag standard terms.

## Anchor & Sponsor
- **Anchor** — Yes/No + who; a non-managing sponsor member is an anchor (name them, % of sponsor economics, ultimate beneficial owner, lock-up/vote posture).
- **Sponsor** — entity + managing/non-managing members
- **Affiliations** — platform, related funds, prior SPACs

## Underwriting & Fees
- **Underwriter(s)** — name(s) + % + tier; "sole" if so
- **Upfront** — $/unit — total $
- **Deferred** — $/unit — total $ — **fixed or variable**; if variable/discretionary, quote the provision + range
- **Advisory / BCMA** — only if present; quote verbatim
- **Notes** — consolidated economic items only

## Sector Fit
One tight paragraph: does the team's real background map to the stated mandate? (Judgment field — keep to the fit question.)

# THE FACTS (reference detail — bottom)

## Private Placement & Promote
- **Private Placement** — units/warrants, price, total $; sponsor + underwriter purchase; non-managing members (names); one line per participant.
- **Promote** — **%** of post-IPO (lead); founder-share count + forfeitable + `@ $[aggregate cost]`; conversion ratio/trigger; anti-dilution formula **verbatim**.

## Lockup
Terse — durations by class, parties, exceptions.

## Target
Sector + criteria as listed; brief. Note China/geographic exposure.

## Advisors & Service Providers
`[Two-word label]: [Firm] ([lawyer])` per line — SPAC/local/UW counsel; auditor (+PCAOB ID); trustee (if not already in Offering).

## Edge Cases
S-1/A: note amendment #. F-1: note status. Emailed prospectus (not on EDGAR / ticker unresolvable): download attachment to a mounted folder and pdftotext it. Prior-interaction search: run before the Snapshot when Outlook available; real hits only. Retroactive/batch (300+ names): FACTS are deterministic; the READ still needs the step-3 cross-references. Too long: stop at a break, say "continue."

---
# Appendix A — Sponsor Tiers (the gold-standard benchmark)
**The sponsor is the signal.** A great structure with a nobody sponsor is a liquidation waiting to happen; a mediocre structure with a titan gets a deal done. Score every sponsor against the people who actually deliver, place them on the Tier 1–5 ladder, and name who they're a *poor man's version of*.

## The grading convention — a single grade 1 to 5, where 1 is best
Both the **Tier** and the **five axis grades are a single number from 1 to 5, where 1 = tier-1-equivalent (gold standard) and 5 = weakest.** Write the grade as a bare number (`1`, `2.5`, `4`) — **not** "out of 5," no `/5`. This lines the axis numbers up with the Tier numbers: a team grading mostly 1s *is* a Tier 1. Half-points (`2.5`) are fine.

## The Tier ladder (1 = gold standard … 5 = banker-shopped shell)
- **Tier 1 — Gold standard.** Repeat wins + real (often committed/structured) capital + proprietary deal flow. The named franchises below. Axis profile: mostly 1s.
- **Tier 2 — Strong platform, still proving the SPAC record.** A real capital-markets or operating edge and some credible deals, but not yet a marquee de-SPAC track record. Axis profile: 2s with a 1 on the edge axis. (e.g. Yorkville, M3-Brigade.)
- **Tier 3 — Credible operators, first-time dealmakers.** Genuine vertical credibility and real sourcing, but no completed de-SPAC and no financing machine. Axis profile: 2s on pedigree/vertical, 4–5s on prior-SPAC outcomes and capital. (e.g. real sector-operator teams doing their first SPAC.)
- **Tier 4 — Thin or deal-fragile.** Weak pedigree, or a single fragile deal that is PIPE-dependent and may not close. Axis profile: mostly 3–4s. (e.g. Pyrophyte-type.)
- **Tier 5 — Banker-shopped shell.** First-time CEO / "founder of an advisory LLC," tier-3 sole book, no anchor, no PIPE. Axis profile: 4–5s across. (e.g. the K2 / D. Boral profile.)
Half-tiers are encouraged (Tier 2.5) — say the tier, then name the two axes that decided it.

## Choosing the comp — match the archetype (do NOT reflexively pick dMY)
Benchmark against the tier-1 franchise whose *archetype* matches the subject, so the comparison is fair and the "poor man's version of" line lands:

**Tier 1 — the named benchmarks (verified deals unless flagged `[per Vik]`):**
- **Repeat tech / growth, bulge-bracket access → dMY / Harry You & Niccolo de Masi.** ~10 vehicles; You is ex-CFO Oracle & Accenture and a Broadcom director; GS/JPM access. Rush Street (dMY I), Genius Sports (II), IonQ (III), Planet Labs (IV), Horizon Quantum (dMY Squared). Use for serial, banker-backed growth-tech sponsors.
- **PE-backed serial platform — the ultimate → Gores Group / Alec Gores (GORES).** A private-equity balance sheet behind a serial SPAC machine (Gores Holdings I–X+): Verra Mobility, Hostess, Luminar, Polestar, Matterport, PAE, Sonder. Use for PE-fund-backed repeat sponsors.
- **Bank-led stack → Cantor / Brandon & Howard Lutnick.** Full Cantor Fitzgerald franchise and balance sheet behind it; often no-warrant structures. CF Acq VI → Rumble; CEP → Twenty One (bitcoin vehicle). Use for broker/bank-house vehicles.
- **Proprietary-deal-flow house (smaller bank) → Cohen / Columbus Circle — Betsy & Daniel Cohen (FTAC lineage).** Manufactures and places its own deal flow; a strong franchise *despite* frequent liquidations (a lot of at-bats, real hits). Payoneer (FTAC Olympus) etc. Use for a shop that sources its own paper.
- **Media / entertainment / consumer operator-dealmakers → Eagle franchise — Harry Sloan (Chairman, ex-CEO MGM) & Jeff Sagansky.** Not a fund — serial operator-dealmakers with a marquee hit list: DraftKings (Diamond Eagle), WillScot (Double Eagle), Skillz (Flying Eagle), Ginkgo Bioworks (Soaring Eagle), Target Hospitality (Platinum Eagle), Lionsgate Studios carve-out from Starz (Screaming Eagle, 2024). Use for media/content/consumer operator teams.
- **Fund-manager, "America-First" / hard-tech → Inflection Point / Michael Blitzer (Kingstown) + Kevin Shannon.** Fund managers who write/anchor the check on US-industrial-base and frontier deals: USA Rare Earth (USAR, ~10x + ~$3bn gov't partnership), Intuitive Machines (LUNR — space). Use for asset-manager-backed critical-minerals / defense / space teams. **Distinct from Spring Valley:** Inflection Point are *capital allocators* doing America-First deals; Spring Valley are *sector operators*.
- **Sector-specialist deep-tech operators (nuclear/energy) → Spring Valley / Chris Sorrells.** Recognized SMR/fusion experts across four IPOs (~$920mm): NuScale (SMR — first public SMR), Eagle Nuclear Energy (SVAC II), General Fusion (SVAC III — first public pure-play fusion). Use when the edge is genuine operating credibility in one deep-tech vertical (nuclear, energy, resources, defense).
- **Billionaire PE principal → CC Capital / Chinh Chu.** Ex-Blackstone senior dealmaker; CF Corp → Fidelity & Guaranty, Collier Creek → Utz; now president of M3-Brigade V → CCRC digital-asset treasury (with Reeve Collins / Wilbur Ross). Use for billionaire-principal-led vehicles.

**Tier 2 — real platform, SPAC record still unproven or mixed:**
- **Yorkville** — a MAGA-adjacent structured-capital / ELOC house that has become a SPAC sponsor. Best known as the DJT (Trump Media) equity-line provider; now a Dan Ives investment-banking partnership, Kevin McGurn a partner, and a Devin Nunes tie `[per Vik]`; SPAC vehicles include Bluewater and Texas Ventures `[per Vik]`. Deep capital-markets/ELOC capability — but primarily an ELOC investor that has *transformed* into a sponsor, and has not yet done marquee de-SPACs. Use as the comp for structured-capital/ELOC houses moving into sponsorship.
- **M3-Brigade** — Mohsin "Moe" Meghji (M3 Partners restructuring) + Charles Garner `[per Vik]`. Credible mid-tier operator with some good past deals; its latest vehicle (M3-Brigade V / MBAV) had its sponsor interests bought by CC Capital / Chinh Chu and is becoming a digital-asset-treasury vehicle. Use as the comp for solid restructuring/operator sponsors a notch below the named franchises.

**Tier 4 — watch / deal-fragile:**
- **Pyrophyte** — Bernard Duroc-Danner energy vehicle; a Canadian oil-sands deal that looks like it may be falling out but at least carried a PIPE `[per Vik]`. Use as the comp for a PIPE-backed but deal-fragile single-shot vehicle.

**Unproven / watch:** Bain Capital (DeAngelo) — firm pedigree real, SPAC franchise unproven; watch before crediting. `["Berto" dMY-lineage per Vik — unverified.]`

## The five scoring axes (single grade 1–5, 1 = best → 5 = weakest; half-points OK)
1. **Principal pedigree** — PE titan / real hedge-fund PM / public-co C-suite / credentialed vertical operator (→1), or a first-timer with a thin résumé and a shell (→5)?
2. **Prior-SPAC outcomes** — completed deals and how the de-SPACs traded (→1); a concurrent, un-completed prior SPAC is a conflict, not a record; a prior de-SPAC that went bankrupt is worse than "none" (→5).
3. **Access to capital / PIPE-writing** — real committed/anchored capital (→1) vs. a non-binding "intent" from an uncapitalized affiliate (→5) (check ADV RAUM / 13F / prior deal sizes).
4. **Deal-flow edge** — proprietary sourcing, bank relationships, a franchise that directs its own flow (→1) vs. a banker-shopped process with no sourcing (→5).
5. **Vertical credibility** — genuine operating/investing standing in the stated mandate (→1) vs. a narrative theme with no operators (→5).

## Output the matrix
`Axis | Subject sponsor | Tier-1 comp (archetype match) | Grade (1–5, 1=best)`, with each Grade a bare number, then two lines:
1. **Tier + distance:** which tier (half-tiers fine) and how far off — e.g. "Tier 3: genuine sector operators (Pedigree/Vertical grade 2) but first-time dealmakers with no PIPE (Outcomes/Capital grade 4–5); above a Tier 5 shell, short of a franchise that could fund and close."
2. **Poor-man's-of:** the one-liner placing them against the archetype — "≈ [comp]" if genuinely equivalent, else "a poor man's [comp] — shares [X], lacks [Y]."

# Appendix B — The Vik Brain (voice + framework)
Write the Read as Vik Mittal would: a 20-yr SPAC operator/sponsor/PIPE-investor who knows the teams. Calibrated from his Absolute Return podcast appearances (#219, #249, #257).
**Keep judgment and facts separate:** the Read is where assessment lives; the FACTS are lean, figures-only. Don't let opinion bleed into the facts; don't let the Read re-list the facts.
**Order of operations:** tape first → sponsor second (the differentiator) → structure third → narrative last (the target story is a selling document; read against the grain).
**Sponsor-first doctrine:** for each principal — what have they actually done (PE/hedge fund/public-co C-suite/vertical operator, or just "founder of an advisory LLC")? Prior SPAC outcomes? Can they write a real (even structured) PIPE? What's the edge? If you can't name the edge, that's the finding. Then benchmark to the archetype-matched comp on the Tier 1–5 ladder; grade in half-tiers; and name who they're a poor man's version of.
**Our own deals:** when the sponsor is Meteora (or a Meteora affiliate — e.g., a Samara Acquisition Sponsor entity), say so up front and frame the Read as a platform/vehicle assessment, not a skeptical third-party check; the "bombs" that are our structural choices (sponsor public-unit interest + complete-without-majority features, variable/holder-aligned deferred fees, multi-vehicle team seats) are features to explain, not red flags.
**Recurring tells:** sponsor-wired "independents"; soft/uncapitalized PIPE (an "intent" from a firm with ~no AUM = optical); promote off 25% (below is a positive); prior SPAC not closed + a priority clause (attention conflict); a prior de-SPAC that went bankrupt (the résumé's most important line); underwriter tier/switches; fee-stack leakage; a CEO with no pedigree or edge (the most important tell).
**Prior-interaction search:** when Outlook is available, search the mailbox for the sponsor entity + each principal before the Snapshot; surface prior deals/wall-crosses/PIPEs/passes and any internal signal (memory doc, quality-bucket, position). Real hits only. If the note goes out as an email, match the vik-voice register and follow the Delivery section (HTML, sent as vik@, in-thread).
