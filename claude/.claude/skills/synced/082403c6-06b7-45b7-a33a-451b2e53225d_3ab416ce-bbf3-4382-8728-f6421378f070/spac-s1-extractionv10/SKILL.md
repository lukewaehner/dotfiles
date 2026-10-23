---
name: spac-s1-extractionv10
description: "Meteora's primary SPAC S-1 IPO extraction (v10) — a 'Read on top, lean facts below' workup. Trigger on any SPAC S-1/S-1A/F-1 or prospectus PDF, or 'extract', 'run the S-1', 'analyze this S-1', 'pull the terms', 'S-1 review', 'run the guide', 'new S-1', 'just filed', 'desk read', or a filing dropped with no instructions. Leads with a Snapshot and sponsor-first Desk Read benchmarking the team against a NAMED gold-standard Tier 1-5 ladder (dMY/Harry You, Gores, Cantor/Lutnick, Cohen-Columbus Circle, Eagle/Sagansky-Sloan, Inflection Point, Spring Valley, CC Capital/Chinh Chu; Tier 2 Yorkville, M3-Brigade) and names who the sponsor is a 'poor man's version of', then bombs, anchor/sponsor, underwriting, sector fit, then a lean figures-only extraction. Tiers and the five axes use a calibrated rule set; prior-vehicle outcomes are graded per the OUTCOMES-RUBRIC and cited from the FRANCHISE-OUTCOMES-LEDGER. Grades are one number 1-5, 1=best. The firm's standard S-1 tool."
---

# SPAC S-1 Extraction (v10 — Read on top, lean facts below)

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
4. Run the four mandatory protocols below — anchor LOCATE, person-level research, citation discipline, tier ledger. They feed the Anchor & Sponsor section and the tier matrix.
5. Write THE READ, then print in the canonical order. One response if length allows; else stop at a break and say "continue."

## The four mandatory protocols
**1 — Anchor LOCATE.** The house rule is that a non-negligible portion of founder shares syndicated to a third party IS an anchor. It gets missed when the sponsor discloses it once, deep in the document, rather than on page 1 — so sweep, don't skim. Search the full filing text for: `"non-managing"`, `"membership interests in our sponsor"`, `"economic rights attributable to"`, `"other third-party investors"`, `"anchor investor"`, `"founder shares"`. Do the managing-versus-non-managing arithmetic explicitly and give a **cost per share for BOTH classes** — where outside money comes in at the same price as the managers, unsweetened, that equivalence is the read and it is invisible without the arithmetic. A disclosed unit-purchase commitment is NOT required for the anchor label and its absence is not grounds to withhold it. Where the split is not disclosed anywhere, write `undetermined` and name every section checked — never infer "no".

**2 — Person-level research.** For every named principal: EDGAR full-text by surname; a Form ADV / Form D **existence check** for any fund or advisory entity they claim; and a check for prior **withdrawn registrations (Form RW)**. A withdrawn prior SPAC registration is filed, public and material. Report findings as facts with source tags.

**3 — Citation discipline.** Every non-obvious figure carries an inline source class: `[S-1 §x]`, `[13D date]`, `[ledger]`, `[spac-details]`, `[web: publication, date]`, `[desk estimate — assumption]`. **A figure that cannot be tagged does not go in the output.** Third-party AUM or fund size requires a filing, an ADV/Form D, or a dated statement attributed to a named person — absent that, omit it. No marketing figure enters an extraction. Estimates are labelled with their assumption, never bare.

**4 — Tier ledger.** Write the tier, the five axis grades and the two deciding axes to the shared tier ledger (`references/tier-ledger-format.md`) so tiers stay comparable between names rather than being re-derived per run.

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
- **Anchor** — Yes / No / undetermined + who; a non-managing sponsor member is an anchor (name them, % of sponsor economics, ultimate beneficial owner, lock-up/vote posture). Resolve with the Anchor LOCATE protocol and give the **cost per share for both the managing and the non-managing class**.
- **Auditable negatives** — any "no X" names what was checked. `"no anchor"` is not a finding; `"no anchor named — swept the six LOCATE phrases across the full 424B4"` is.
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
Both the **Tier** and the **five axis grades are a single number from 1 to 5, where 1 = tier-1-equivalent (gold standard) and 5 = weakest.** Write the grade as a bare number (`1`, `2.5`, `4`) — **not** "out of 5," no `/5`. Half-points (`2.5`) are fine. Every axis clips to the range 1.0–5.0.

## THE CARDINAL RULE — grade the SPONSOR, never the STAGE
A pre-deal SPAC has no PIPE, no announced deal and no completed acquisition **by construction**. Those absences are facts about where the vehicle sits in its life, not about the quality of the people running it. **Never mark a sponsor down for something no pre-deal vehicle could possibly have.**

**Use the whole scale.** Every axis below has a defined 1 and a defined 5 and both ends are meant to be used. If your five axis grades all land between 2.5 and 4 you have not graded, you have hedged. Do not manage to a target distribution — grade each name on its own evidence.

---
## AXIS 1 — STRUCTURE (compute it; do not judge it)
Structure measures **how much the sponsor had to give away to place the deal, how much runway it negotiated, and whose book it sold through.** A strong sponsor sells a clean unit, takes time, and commands a real bank.

**Step 1 — sweetener give-away, in share-equivalents per unit.**
`SE = rights_fraction + 0.15 × warrant_fraction`
A right converts to stock at close — certain dilution, 1.00 SE per unit of face. A warrant is a ~$11.50-struck option worth roughly 8% of a share at IPO, so it carries about a seventh of the weight. **Read the rights first, then the warrant** — warrant size only discriminates *within* the no-rights family.

| SE | Grade | Typical structure |
|---|---|---|
| 0.000 | **1.0** | naked share — no warrant, no rights |
| ≤0.040 | **1.5** | ≤1/4 warrant, no rights |
| ≤0.055 | **2.0** | 1/3 warrant, no rights |
| ≤0.080 | **2.5** | 1/2 warrant, no rights |
| ≤0.110 | **3.0** | 1/10 right, or 3/4 warrant |
| ≤0.145 | **3.5** | 1/8 right |
| ≤0.220 | **4.0** | 1/5 right |
| ≤0.300 | **4.5** | 1/4 right |
| >0.300 | **5.0** | 1/4 right plus a full warrant, or worse |

**Step 2 — runway** (months from IPO to base deadline): ≤12m **+1.0** (could only sell a short fuse) · 13–14m **+0.75** · 15–17m **+0.5** · 18–20m **+0.25** · 21–23m **0** · 24–27m **−0.5** (negotiated real runway) · 28m+ **−0.75**

**Step 3 — underwriter tier**, graded on the lead / sole bookrunner:
- **Tier 1** — Goldman, BofA, Citi, Morgan Stanley, Barclays, Jefferies, UBS, Deutsche, Wells Fargo, Credit Suisse, Santander, TD Cowen, Leerink → **−0.25**
- **Tier 2** — Cantor, BTIG, Cohen & Company Capital Markets, Clear Street, Stifel, Needham, Roth, Oppenheimer, KBW, JonesTrading → **0.00**
- **Tier 3** — D. Boral, Maxim, AGP, EF Hutton, Chardan, B. Riley, ARC, Benchmark, Kingswood, Polaris, IB Capital, Bancroft, Dominari, Webull → **+0.75**

**Affiliated-book exemption:** where the lead bookrunner is owned by or affiliated with the sponsor, apply **no** tier-3 penalty. A sponsor placing through its own book is not being shopped by a weak bank; it is using distribution it controls, which Axis 5 treats as the strongest sourcing position there is.

**Step 4** — `structure = clip(SE_grade + runway_adj + underwriter_adj, 1, 5)`. Show the arithmetic.

## AXIS 2 — PEDIGREE
What the principals have **actually done**.
- **1** — PE titan / founder or CIO of a real fund / public-company CEO or CFO / a nationally-recognised operator in the mandate.
- **2** — senior institutional operators: MD-level at a bulge bank, C-suite at a mid-cap, partner at a credible fund.
- **3** — real but sub-institutional: VP/director level, a boutique founder with a genuine record, a credible single-vertical operator.
- **4** — thin: an advisory LLC with no assets, a consultant, a career that does not obviously qualify them to buy a company.
- **5** — first-time CEO with no relevant record; "founder of an advisory LLC" and little else.

**The test for a famous name is ECONOMICS, not title and not control.** Read the per-person split of sponsor membership interests in the S-1's "Our Sponsor" / "Founder shares" footnote — the Anchor LOCATE protocol already reads that section.
- A nationally-recognised principal holding **≥10% of sponsor membership interests counts as grade-1 pedigree regardless of title** — advisory board, director, officer, it does not matter. They forfeit that stake if no deal closes, and that alignment is what makes the name an asset.
- A famous name holding a token interest — a director's 25,000–50,000 shares, well under 10% — is **letterhead and does not lift pedigree**, whatever the title.
- Do not use "do they control the vehicle" as the test. It fails in both directions: a vehicle can have two advisory-board members holding 24% and 16% of the sponsor — the largest named holders in the deal — while the CEO's disclosed founder-share interest through the sponsor is zero.

Carry the same finding into Axis 5: a principal whose personal profile is itself the sourcing engine, and who holds material founder economics, is a grade-1.5 flow case.

## AXIS 3 — PRIOR SPAC OUTCOMES
Grades come from the **FRANCHISE-OUTCOMES-LEDGER**, which grades per the **OUTCOMES-RUBRIC** memory doc. Read both before grading; the rubric doc is desk-editable and supersedes anything written here. Cite the ledger label, its rationale line and its last-verified date, and never originate a grade the ledger lacks.

**The only five labels: `strong` / `good` / `mediocre` / `poor` / `failed`.** Use them verbatim — "catastrophic", "wipeout", "near-total value destruction" are not grades.

| Label | Meaning |
|---|---|
| **strong** | sustained ABOVE $10. Rare; the capital-formation overlay never manufactures it. |
| **good** | sustained $7–10. |
| **mediocre** | sustained $4–7. |
| **poor** | sustained below $4 **while remaining a viable, listed going concern.** A sub-$1 price by itself is Poor, NOT Failed. |
| **failed** | STRUCTURAL failure only: bankrupt, delisted for non-compliance, liquidated, receivership. **Failure is a status, not a price level.** |

Three governing rules from the rubric:
1. **Peak AND current, take the better** of the highest sustained post-close band and the current price.
2. **The capital-formation overlay only LIFTS, never drags.** A qualifying closing raise lifts one tier; a franchise-defining one (≥2 of: winter-era close, 90%+ redemption backdrop, marquee anchors, deal-carrying size, sponsor→newco board continuation) lifts two. A small or absent raise is neutral. **A pre-deal SPAC without a PIPE is never marked down for it.**
3. **Caps.** Structural-failed + any qualifying raise caps at **poor**. A realized deep-loss exit (<$4 crystallized) caps at **mediocre**. Every overlay lift caps at **good**.

**"Success" = strong OR good.** Mediocre and below are not successes. **Pending or live vehicles never enter a denominator**, including the vehicle being graded, which never counts against itself.

**The liquidation rule.** A SPAC that liquidated **without ever doing a deal** returned the trust at ~$10 and every holder was made whole. Read that as **discipline, not failure** — the team declined to force a bad deal. Rank severity: dealless liquidation (near-neutral) < a completed de-SPAC that traded mediocre or poor < a completed de-SPAC that went bankrupt or delisted. **Dealless liquidations alongside real wins cost nothing** — this is the Cohen/Columbus Circle doctrine, *"a strong franchise despite frequent liquidations — a lot of at-bats, real hits."* A dealless liquidation can never produce a 4, 4.5 or 5.

- **1** — 3+ ledger-verified successes, clearly outnumbering the rest. One bankruptcy inside a long record does not cost the 1. *(Eagle: 6 strong across 8 vehicles with one 2013-era failure = 1.)*
- **1.5** — 2 successes with no material disaster, or a deep record where wins modestly outnumber failures.
- **2** — 1 success, or several mediocre with no blow-up.
- **3** — **no prior vehicle at all**, or dealless liquidations only. Unproven, but nobody was harmed. Also where the sponsor changed hands and the current principals have no completed record.
- **3.5** — three or more vehicles, every one liquidated dealless, nothing ever completed.
- **4** — a mediocre/poor de-SPAC with nothing strong beside it, or a withdrawn registration (RW) and little else.
- **4.5** — zero successes and two or more POST-deSPAC structural failures.
- **5** — a graveyard: 3+ post-deSPAC bankruptcies or delistings.

**Whose record is it?** Count only vehicles run by principals who **control this sponsor**. A record belonging to an independent director, an unpaid advisory-board member, or a departed team is *adjacent* — name it as context and grade toward the neutral 3, never as this sponsor's record.

## AXIS 4 — CAPITAL ACCESS (two sources; neither present = 4)
Not how big the IPO was — a large raise through a good bank is the *bank's* achievement. **Whose money stands behind this sponsor, and have these people ever pulled committed capital into a deal?** Grade the better of two sources; only one is needed.

**Source A — available capital (a balance sheet the sponsor controls).** Grade the SCALE and whether it is filing-confirmed; existence alone is not a 1.
- **1** — the sponsor is or owns a **bank or broker-dealer** that can place and hold paper, FINRA-confirmed.
- **1.5** — principals run an **investment fund**, confirmed by Form ADV, Form D, or 13F/13D.
- **2** — a bank/BD affiliation is clear but not filing-confirmed.
- **2.5** — a fund is claimed but ADV/Form D could not be confirmed, or the check was never run; **or** corporate/family-office capital, filing-confirmed.
- **3** — corporate or family-office capital, claimed but unconfirmed.
- none — no captive pool. Go to Source B.

**Source B — demonstrated capital formation (prior vehicles only).** A qualifying raise is real, committed, identifiable institutional capital that funded a close — a PIPE, forward-purchase agreement, non-redemption book, or sponsor-affiliated committed equity. Token, unnamed or purely-retail arrangements do not qualify. Count only vehicles run by principals who control this sponsor.
- **1** — 3+ prior closes with a qualifying raise, at least one $250mm+. · **1.5** — 3+ raises, or 2 with one $250mm+. · **2** — 2 raises, or 1 at $250mm+. · **2.5** — 1 raise of $50mm+. · **3** — 1 small raise. · none — no prior vehicle ever closed with committed capital.

**Combining.** Either source present → take the better grade. **Both present → subtract a further 0.5.** A material anchor on this vehicle → subtract 0.25. **Neither source present → 4**; with a disclosed FPA or committed equity on this vehicle, 3.0; with only a material anchor, 3.5. Deal size adjusts last and only slightly: $400mm+ −0.5, $250mm+ −0.25, sub-$100mm +0.5.

**Book-quality floor.** A sponsor with genuine capital access does not sell through a tier-3 sole book: where the lead book is tier 3, capital access cannot be graded better than **3.0**; tier 2, no better than **1.5**; a tier-1 book leaves the grade unconstrained. **The floor does not apply to an affiliated book** — a sponsor owning its own distribution is evidence of capital access, not a substitute for it.

**Never mark a pre-deal sponsor down for having no PIPE on this vehicle.** Source B asks about prior vehicles only.

## AXIS 5 — DEAL-FLOW EDGE
What makes a target land on this team's desk rather than a banker's?
- **1** — an in-house broker-dealer or bank that manufactures and places its own paper, **or** a serial franchise whose name alone generates inbound.
- **2** — a standing proprietary network in the mandate: a fund with a live portfolio, an operator with a sourcing seat.
- **3** — real relationships but no structural edge; would compete for any process.
- **4** — no visible sourcing; the process will be banker-shopped.
- **5** — banker-shopped with no sourcing and no relationships named anywhere.

Repeat-franchise depth is the most reliable observable here — the desk's best names average roughly five prior vehicles and its weakest closer to none. Count vehicles run by principals who control this sponsor, on the same "whose record is it" test as Axis 3.

## MODIFIER — VERTICAL FIT (not an axis)
Applies only as a penalty, and only where the mismatch is egregious:
- team's domain clearly matches the mandate → **+0.0**
- the mandate is generalist, so fit is **not assessable** → **+0.0**. A generalist mandate is neither a match nor a mismatch — never treat it as evidence of fit.
- a theme with no operator behind it → **+0.25**
- flagrant mismatch (a restaurant team buying steel; a crypto pivot with no crypto operator) → **+0.5**

## SHELL TAKEOVERS — check before grading
Some vehicles IPO under one sponsor and are later sold: the sponsor entity changes hands, officers and directors turn over, and the people running it today are not the people in the S-1. Where the pack shows a post-IPO change of sponsor control — a sponsor-interest purchase, wholesale officer turnover, a new controlling member — **grade the CURRENT sponsor** from post-IPO evidence (8-K, 13D, Forms 3/4), say plainly that the S-1 no longer describes the operator, and mark tier confidence **low**. Never silently grade the original team and present it as a read on the vehicle.

## THE COMPOSITE — compute it, don't eyeball it
```
base = 0.30·pedigree + 0.30·structure + 0.20·prior_outcomes + 0.15·capital_access + 0.05·deal_flow_edge
tier = round_to_nearest_half( clip(base + vertical_fit_modifier, 1, 5) )
```
Pedigree and structure carry most because both are fully visible in the filing and both track the desk closely. Show the arithmetic. **Do not adjust the computed tier because it feels high or low** — if the arithmetic gives 1.5, the answer is 1.5. Overriding the composite is what produces a ladder that never awards Tier 1.

## The Tier ladder (1 = gold standard … 5 = banker-shopped shell)
- **Tier 1 — Gold standard.** Repeat wins + real (often committed/structured) capital + proprietary deal flow. The named franchises below. **This grade is reachable and is meant to be used.**
- **Tier 2 — Strong platform, still proving the SPAC record.** A real capital-markets or operating edge and some credible deals, but not yet a marquee de-SPAC track record. (e.g. Yorkville, M3-Brigade.)
- **Tier 3 — Credible operators, first-time dealmakers.** Genuine vertical credibility and real sourcing, but no completed de-SPAC and no financing machine.
- **Tier 4 — Thin or deal-fragile.** Weak pedigree, or a structure that had to be sweetened hard to place.
- **Tier 5 — Banker-shopped shell.** First-time CEO / "founder of an advisory LLC," tier-3 sole book, rights-laden unit, no anchor, no record. **Reserve Tier 5 for names that unambiguously meet every part of that description.**

Half-tiers are encouraged (Tier 2.5) — say the tier, then name the two axes that decided it. **A half-tier must be earned by a discriminating fact, not by hedging.**

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

## Output the matrix
`Axis | Subject sponsor | Tier-1 comp (archetype match) | Grade (1–5, 1=best)` across pedigree, structure, prior outcomes, capital access and deal-flow edge, with each Grade a bare number, then three lines:
1. **Tier + distance:** which tier and how far off — e.g. "Tier 3: genuine sector operators (Pedigree 2, Structure 2) but first-time dealmakers with no captive capital (Prior outcomes 3, Capital access 4); above a Tier 5 shell, short of a franchise that could fund and close."
2. **Poor-man's-of:** the one-liner placing them against the archetype — "≈ [comp]" if genuinely equivalent, else "a poor man's [comp] — shares [X], lacks [Y]."
3. **Superstar flag (reported, never scored):** `yes` only where BOTH hold — a principal whose personal public profile is itself a sourcing and capital asset at national scale, AND that same person holds ≥10% of sponsor founder-share economics. Log the person and the percentage. **This flag never moves the tier**; it is recorded so the desk can review firings.

# Appendix B — The Vik Brain (voice + framework)
Write the Read as Vik Mittal would: a 20-yr SPAC operator/sponsor/PIPE-investor who knows the teams. Calibrated from his Absolute Return podcast appearances (#219, #249, #257).
**Keep judgment and facts separate:** the Read is where assessment lives; the FACTS are lean, figures-only. Don't let opinion bleed into the facts; don't let the Read re-list the facts.
**Order of operations:** tape first → sponsor second (the differentiator) → structure third → narrative last (the target story is a selling document; read against the grain).
**Sponsor-first doctrine:** for each principal — what have they actually done (PE/hedge fund/public-co C-suite/vertical operator, or just "founder of an advisory LLC")? Prior SPAC outcomes? Can they write a real (even structured) PIPE? What's the edge? If you can't name the edge, that's the finding. Then benchmark to the archetype-matched comp on the Tier 1–5 ladder; grade in half-tiers; and name who they're a poor man's version of.
**Our own deals:** when the sponsor is Meteora (or a Meteora affiliate — e.g., a Samara Acquisition Sponsor entity), say so up front and frame the Read as a platform/vehicle assessment, not a skeptical third-party check; the "bombs" that are our structural choices (sponsor public-unit interest + complete-without-majority features, variable/holder-aligned deferred fees, multi-vehicle team seats) are features to explain, not red flags.
**Recurring tells:** sponsor-wired "independents"; soft/uncapitalized PIPE (an "intent" from a firm with ~no AUM = optical); promote off 25% (below is a positive); prior SPAC not closed + a priority clause (attention conflict); a prior de-SPAC that went bankrupt (the résumé's most important line); underwriter tier/switches; fee-stack leakage; a CEO with no pedigree or edge (the most important tell).
**Prior-interaction search:** when Outlook is available, search the mailbox for the sponsor entity + each principal before the Snapshot; surface prior deals/wall-crosses/PIPEs/passes and any internal signal (memory doc, quality-bucket, position). Real hits only. If the note goes out as an email, match the vik-voice register and follow the Delivery section (HTML, sent as vik@, in-thread).
