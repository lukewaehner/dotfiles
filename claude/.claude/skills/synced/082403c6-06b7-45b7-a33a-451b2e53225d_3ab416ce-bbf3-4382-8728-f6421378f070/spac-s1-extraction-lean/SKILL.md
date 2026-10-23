---
name: "spac-s1-extraction-lean"
description: "Lean, no-fluff S-1 extraction for SPAC IPO filings — reports the filing as figures and facts, no AI commentary or narrative. Leads with the Desk View (header snapshot, one-line bombs, Prior SPACs, and a Deal-Doing Capability chain connecting career seat → prior SPAC record → board reach → access to capital), then Extraction Terms (Sections 1–8). Resolves named principals' prior SPACs via EDGAR / spac-details when the filing leaves them unquantified. Trigger whenever the user uploads an S-1/S-1A/F-1 (PDF or .htm) or references one in context and asks to 'extract', 'run the S-1', 'do the extraction', 'analyze this S-1', 'pull the terms', or 'S-1 review'. Also trigger on 'new S-1', 'just filed', or an S-1 dropped without instructions. Prefer over the verbose spac-s1-extraction when the user wants terse output, says 'no fluff', 'keep it tight', 'just the figures', or 'don't editorialize'. Always use this skill for lean S-1 extractions."
---

# SPAC S-1 Extraction (Lean)

## Overview

Produce a short desk-level synthesis of a SPAC S-1 that flags material deviations from standard SPAC terms and establishes whether the sponsor group can actually get a deal done, then report the full legal and economic terms as figures and facts. Output goes **in the chat body as structured text** — no Word docs, no artifacts, no files.

Output order is fixed: **Desk View first, Extraction Terms second.**

## Output discipline — this is the point of the skill

The reader is a SPAC analyst who already knows what standard terms look like. They want the filing's numbers, not an interpretation of them. Every word that isn't a fact from the filing costs them time.

So:

- **Report, don't assess.** State the figure. Do not characterize it as strong, thin, attractive, favorable, aggressive, investor-friendly, or notable. If a number is unusual, the analyst will see that from the number.
- **No peer comparisons or benchmarking.** Do not write "above peer norms", "typical for this size", "in line with the market". The analyst has the comparison set in their head.
- **No lead-ins or wrap-ups.** No "Here is the extraction", "Below you'll find", "In summary", "Overall this appears to be". Start with the Desk View header block. End with the last field of Section 8.
- **No hedging or narration.** Not "It appears that the trust is funded at $10.10" — just `$10.10`.
- **Prefer figures to sentences.** A field that can be a number, a ratio, or an equation should be that, not a sentence describing it.
- **The field lists below are the complete set to report.** Do not add extra line items just because the filing mentions them — no deferred-underwriting line in the trust section, no sponsor promissory notes or working-capital/extension loans in the sponsor section, no trust investment policy or projected interest estimates. If a fact belongs to a listed field, put it there; if it doesn't, leave it out.
- **Omit empty fields entirely.** If a field isn't disclosed and the field is a simple fact (ticker, auditor, lawyer name, joint bookrunner, BCMA), leave the line out rather than writing "None" or "Not disclosed." Reserve "Not disclosed." for fields where absence is itself meaningful (deferred fee terms, promote, trust mechanics).
- **Do not report the absence of a term.** "No cash retainer", "no monthly admin fee", "no working-capital withdrawal from trust" are non-facts — say nothing.
- **Do not infer or extrapolate.** If the filing doesn't say it, it doesn't go in. Do not compute implied figures unless the field explicitly calls for one. One carve-out: prior-SPAC resolution, below.

Quoting the filing verbatim is not fluff — it is the highest-fidelity form of reporting, and is required where noted below.

## Prior-SPAC resolution — the one permitted outside lookup

S-1s name a principal and then leave their SPAC history unquantified: "a founding investor of 10 SPACs", "has served as an officer of several blank check companies", "sponsored two prior special purpose acquisition companies". A bare name attached to an unquantified claim is not usable on a desk. Resolve it.

- **The filing remains the sole source of truth for terms** — offering, trust, promote, fees, lock-up. Never override a filing figure with an outside source.
- **Resolve for named principals only** — officers, directors, director nominees, advisors, sponsor managing members, and any *named* non-managing sponsor investor. Use `spac-details` and `edgar-filings` / `edgar-ownership-search` to get: SPAC name, IPO year, IPO size, the person's role, and outcome (merged with target / liquidated / pending / withdrawn).
- **Do not resolve an unnamed party.** An anonymous "institutional investor" or "sponsor non-managing member" cannot be researched — report it as the filing describes it and stop.
- **Tag every resolved line** `[EDGAR]` or `[spac-details]`. Filing-sourced facts carry no tag. The analyst must be able to see at a glance which facts came from outside the four corners.
- **If a claim cannot be resolved, mark it `unresolved`** and report it as the filing states it. Do not silently drop it, and do not launder the filing's own count as though it were verified.
- **Do not web-search** bios, fund AUM, net worth, or reputation. That is `spac-bios` territory — hand off if the user wants it.

## Workflow

1. **Read the filing** — if PDF, `pdftotext -layout`; if HTML, strip tags to text. Then targeted `grep`/`sed` to locate sections. S-1s run 150–300 pages; extract text first, then hunt each data point.
2. **Extract every field** — Sections 1–8 — before writing anything.
3. **Resolve prior SPACs** for every named principal per the section above. Do this before writing the Desk View; the sponsor capability chain depends on it.
4. **Run Part 1: Desk View.**
5. **Print the divider.**
6. **Run Part 2: Extraction Terms** — Sections 1–8 in the chat.

Run both parts in one response if length allows. If you hit the limit, stop at a section break, say where you stopped, and ask the user to say "continue."

The uploaded filing is the primary source. EDGAR tools are for prior-SPAC resolution, and for cross-reference if the user asks or the upload is incomplete.

## Filing Reading Strategy

```bash
# PDF
pdftotext -layout "[path]/[filename].pdf" ./s1.txt

# HTML (.htm from EDGAR) — strip tags, keep table cell breaks
python3 -c "
import html,re
raw=open('[filename].htm',encoding='utf-8',errors='replace').read()
raw=re.sub(r'(?is)<(script|style).*?</\1>',' ',raw)
raw=re.sub(r'(?i)</(p|div|tr|h1|h2|h3|table)>','\n',raw)
raw=re.sub(r'(?i)<br[^>]*>','\n',raw); raw=re.sub(r'(?i)</td>',' | ',raw)
t=html.unescape(re.sub(r'<[^>]+>','',raw)).replace('\xa0',' ')
open('s1.txt','w').write(re.sub(r'\n\s*\n+','\n',re.sub(r'[ \t]+',' ',t)))"

grep -n "keyword" s1.txt | head -20
sed -n 'START,ENDp' s1.txt
```

Search terms by section: "Public offering price", "Underwriting discounts", "THE OFFERING", "trust account", "Continental Stock Transfer", "PCAOB ID", "EXPERTS", "LEGAL MATTERS", "private placement", "Founder shares", "Class B", "UNDERWRITING", "Officers and Directors", "Conflicts of Interest", "lock-up", "USE OF PROCEEDS", "automatically extended", "deposit.*trust", "Sponsor Information", "non-managing member", "blank check compan", "special purpose acquisition", "advisory fee".

---
---
# PART 1: DESK VIEW
---
---

Synthesize. The Extraction Terms below carry the full field detail — do not duplicate them verbatim here. Same voice rules: this section flags deviations and states track record, it does not opine on them.

## Header Block

One bullet per field, one line each. No sub-bullets, no sentences — except the Sponsor line, which may run to two.

- **SPAC Name**
- **Ticker**
- **Jurisdiction**
- **Offering** — units × $10.00 = proceeds; unit equation (e.g. `1U = 1S + 1/2W + 1/4R`); over-allotment `(X%)`. Do not state the over-allotment unit count or the exercise window.
- **Trust Funding** — $/unit figure, with excess over $10.00 if any
- **Private Placement** — amount, instrument, participants
- **Timeline** — base + extension, terse form
- **Anchor** — `Yes/No` + name(s) + size (units and $, or % of sponsor economics if a non-managing member). One line total; the Anchor & Sponsor block below carries the detail.
- **Sponsor** — entity name + jurisdiction; managing members with the day-job seat that sources deals (name the seat: "ex-Lionsgate Corporate President", "Founder/MP of Nile Capital Group"); platform if any; **prior-SPAC count across the managing members with the aggregate resolved outcome** (e.g. `3 prior SPACs — 2 merged, 1 liquidated [EDGAR]`, or `no prior SPAC among managing members`); and any named non-managing sponsor investor who carries SPAC track record.
- **Underwriter** — name(s) with % in brackets; upfront $/unit; deferred $/unit tagged `fixed` or `variable`; all-in comp as % of gross if there is a fee outside the underwriting discount

## Bombs / Key Deviations

Flag material deviations from standard SPAC terms.

**One line per bomb. Bold `**Bomb:**` prefix, the deviation, its figures, stop.** No second sentence, no subordinate clause explaining why it matters, no quoted filing language unless the wording itself is the deviation. If a bomb runs past roughly 20 words, cut it. If there are no bombs, write `None` and move on.

Flag if present:
- **Permitted withdrawals from trust beyond standard taxes** — working-capital or operating draws on trust interest, excise-tax withdrawals from trust.
- **Underwriter economics above the standard 2% + 3.5% stack** — a separate advisory / success / M&A fee to the underwriter on top of the deferred commission, a deferred fee not reduced pro rata for redemptions, or a deferred fee reallocatable to another FINRA member at management's discretion. State the fee, the % of gross, and the non-standard mechanic.
- **Divided fiduciary duty** — an officer or director owing fiduciary duties to another SPAC or blank-check vehicle. Name who, and to which entities.
- **China exposure** — management, operations, assets, or intended target in China (incl. Hong Kong and Macau). Name the exposure and any disclosed VIE / enforceability / PRC ownership limitation.
- **Early access to trust principal or non-standard interest mechanics** — only if genuinely non-standard.
- **Non-standard redemption mechanics.**

Do NOT flag (standard or immaterial — these are not bombs):
- **Fees payable out of trust at closing.** Deferred underwriting, advisory fees, and transaction expenses are routinely funded from trust and reduce the cash the target receives; they do not reduce the redemption price. Do not construct a bomb out of "$X/unit of the trust is encumbered" or out of trust-available-for-BC sitting below the headline trust figure. The *size* and *mechanics* of an off-market fee stack is the bomb (above); the mere fact that fees sit in trust is not.
- **A team with no completed prior SPAC** — a first-time CEO, Co-CEO, CFO, or full team. Report SPAC history in the Prior SPACs block, Section 7, and the management table; it is not a bomb.
- A standard vote-based extension structure, including a base term (e.g. 12 months) extendable by shareholder vote with a redemption opportunity. Flag the timeline only if it is genuinely non-standard — an automatic extension the sponsor triggers without a vote, or a base term materially shorter than peers.
- Sole bookrunner / no co-manager.
- Standard founder-share lock-up, including a $12.00 20/30-day early release.
- The sponsor being a single individual or single-member vehicle rather than an institutional platform.
- Officers, directors, sponsor, or assets located outside the U.S., absent China exposure.
- Rights conversion mechanics (ratio, round-down of fractions, must-convert-if-not-surviving).
- Offshore / non-U.S. sponsor entity.
- Affiliated business combination permission (the divided-fiduciary-duty bomb above is a distinct, narrower thing).
- Standard dissolution expense language ($100K), standard 15% redemption cap, standard $100K annual WC withdrawal cap absent a rollover, standard anti-dilution provisions.
- Trust overfunding — already captured as a figure in the Extraction Terms trust section.
- Convertible working-capital loans at $10.00/unit up to a stated cap.

## Prior SPACs

The question this block answers: **has this group closed a SPAC before, and what happened.**

Cover the sponsor entity, the platform, the managing members, the officers, the directors, and any *named* non-managing sponsor investor. Resolve per the prior-SPAC resolution rules. One line each, factual, no assessment:

`[SPAC name] ([IPO year], $[size]) — [person, role] — [outcome: merged with [target] [date] / liquidated [date] / pending / withdrawn] [source tag]`

Rules:
- **Never leave a name dangling.** A line that says only "X — described as a founding investor of N SPACs" is not a Prior SPACs entry; it is an unresolved claim. Resolve it into named SPACs, or move the sentence into the Anchor & Sponsor block as a filing disclosure and mark it `unresolved`.
- Order by relevance: managing members first (they run this vehicle), then officers and directors, then non-managing investors last.
- A prior liquidation is an outcome to be reported, not a bomb. State what happened.
- If nobody in the group has a prior SPAC, write `None — no prior SPAC among the sponsor, managing members, officers, or directors` and move on.

## Anchor & Sponsor

- **Anchor Deal:** Yes/No + names and purchase details. A deal with a non-managing sponsor member is an anchor deal — mark `Yes` and name the member (with its % of sponsor economics and the ultimate beneficial owner if disclosed).
- **Anchor Price:** $/unit and structure (IPO units vs. FPA vs. pre-IPO founder shares vs. non-managing sponsor economics)
- **Sponsor:** Entity name + managing/non-managing members, with the promote split between them (% of founder shares to managing vs. non-managing, with and without the over-allotment).
- **Affiliations:** Related funds, prior SPACs, institutional connections.
- **Deal-Doing Capability:** The one place in this skill where connective reasoning is wanted. Four short lines, each a chain of disclosed facts — no verdict, no adjectives, no probability estimate. Let the chain carry the conclusion.
  - **Sourcing seat** — what the managing members' current and most recent roles give them access to (sector, deal size, geography), tied to the stated acquisition criteria. Name the seat, not the sentiment.
  - **Prior SPAC execution** — closed / liquidated / pending record across the group, and the size range they have taken through a close. Pull from the Prior SPACs block; do not restate it in full.
  - **Board reach** — which directors bring a distinct sourcing or credibility channel vs. which are audit-committee fillers, by the entities on their fiduciary-duty table.
  - **Access to capital** — the concrete evidence of PIPE / equity capacity: named institutional non-managing sponsor members, anchor size, the underwriter's franchise, whether any principal runs a fund that could write the check, and the filing's stated PIPE intent. If the only evidence is a boilerplate "we may issue shares in PIPE transactions", say that.

## Underwriting

- **Underwriter(s):** Name(s) with % in brackets
- **Upfront Fee:** $/unit — total $
- **Deferred Fee:** $/unit — total $ — **and whether it is fixed or variable.** If variable, state the range and the condition.
- **All-in Economics:** Total underwriter compensation as a $ figure and as a % of gross IPO proceeds, itemized — upfront + deferred + any advisory / success / marketing fee. State which components survive redemptions.
- **Notes:** Consolidated economic items only — representative shares, cash advance, expense cap, financing tail. No BCMA line if none. No FINRA rule numbers or lock-up boilerplate.

## Management & Board

| Name | Role | Background | Prior SPAC / Affiliation |
|------|------|-----------|--------------------------|

All officers, directors, and advisors. Backgrounds as facts — roles and entities, not adjectives. Prior SPAC column states the SPAC and the outcome (merged, liquidated, pending, withdrawn) with its source tag. Write `None` where a person has no prior SPAC.

---
---
# PART 2: EXTRACTION TERMS
---
---

Use `##` headers for sections, bold labels for fields, bullets for multi-item fields.

## Section 1: Overview — [SPAC Name]

- **SPAC Name**
- **SPAC Tickers** — List the tickers only. No explanation before or after. Format: `Unit: XYZU | Share: XYZ | Warrant: XYZW | Right: XYZR`. Omit any class not present. If no tickers are in the filing, omit the field.
- **SPAC Counsel** — Firm name, and the individual lawyer's name if the filing names one. Nothing else — no description of what each firm does. Format: `[Firm] ([Lawyer])`. List SPAC counsel, local/jurisdictional counsel, and underwriter's counsel on separate lines with a two-word label only.
- **Auditor** — Firm name only. Add the PCAOB ID if disclosed.
- **Domicile** — DE, Cayman, BVI, etc.
- **Exchange** — Include tier (Nasdaq Global Market, Nasdaq Capital Market, NYSE American).

## Section 2: Offering

- **Structure** — Write as an equation, not prose. Common share = `S`, warrant = `W`, right = `R`, with the fraction from the filing:
  - `1U = 1S + 1/2W + 1/4R`
  - `1U = 1S + 1/20W`
  - `1U = 1S` (no attached securities)
  The letters and fractions come from the filing — do not carry over the examples above.
- **Units Offered** — Total units × price per unit = gross proceeds. Figures only.
- **Over-Allotment Option** — Size (units and %) and expiration window.
- **Timeline** — Terse. Base term plus extension structure, in months spelled `months` (not `MO`), no sentences:
  - `12 months + 0 extension`
  - `18 months + 2 × 3 months extension`
  - `24 months + 1 × 6 months extension (vote required)`

## Section 3: Trust Account

Report only these fields. Do not add a deferred-underwriting-in-trust line (that fee lives in Section 6), a trust investment policy, or a projected interest estimate.

- **Total in Trust** — Aggregate at IPO, with and without over-allotment.
- **Trust Per Unit** — The dollar figure only (e.g. `$10.10`). If above $10.00, append the excess as a figure only: `$10.10 (+$0.10)`. No source narrative, no commentary on what overfunding means.
- **Trustee** — Name.
- **Permitted Withdrawals** — Uses (taxes, working capital, dissolution) with annual caps and any rollover provision. Figures and terms only.
- **Dissolution Expenses** — Maximum reserved.
- **Trust Available for BC** — The filing's own stated net-of-fees figure, if given, with the components deducted. Figures only.
- **Auto-Extension** — Include this field only if the filing provides for an automatic extension. State the trigger, the extension length, and the per-share or aggregate deposit into trust. If there is no automatic extension mechanic, omit the field entirely — do not write "None" or describe the vote-based alternative.

## Section 4: Private Placement, Promote and Anchor Investors

**4.1 Private Placement**
- Number of units/warrants, price each, total proceeds
- Sponsor purchase (units, $)
- Underwriter purchase (units, $)
- Non-managing sponsor investors: yes/no + names
- Participant breakdown, one line each: `[Name] — [X units @ $Y = $Z] — [N founder shares]`

Do not describe the mechanics of the private-placement securities (redeemability, expiry, transferability) — those terms are not wanted here.

**4.2 Anchor Investors**

An anchor investor is an outside party who takes an economic stake in the deal at IPO. Two forms count, and both belong here:
- The classic anchor — an investor buying IPO units and/or receiving founder-share economics under an investment agreement.
- **A non-managing member of the sponsor.** A non-managing member holds sponsor economics without running the vehicle, so it is an anchor position by another name — an outside check written into the promote. Treat any non-managing-member deal as an anchor deal. Whenever the filing discloses a non-managing sponsor member (the same names captured in 4.1), list them here, and follow the ownership chain to the ultimate beneficial owner if the filing names one (e.g. the sole member of the non-managing-member entity).

If there are genuinely no anchor investors and no non-managing sponsor members, write `None` on the same line as the 4.2 heading and stop — no bullets. Otherwise list, one line per investor:
- Name — units purchased and $ committed, or the % of sponsor economic interest held if a non-managing member
- Founder share economics received
- Lockup / transfer terms attached to the anchor allocation
- Prior SPAC record if the investor is named and resolvable, with source tag

**4.3 Promote**
- **Promote %** — Class B (or founder shares) as % of post-IPO shares. Lead with this.
- **Promote size** — Founder share count.
- **Promote split** — % of founder shares to managing members vs. non-managing members, with and without over-allotment.
- **Conversion** — Class B to Class A ratio and trigger.
- Quote the anti-dilution formula verbatim.

## Section 5: Sponsor / Admin Fees

Report only these fields. Do not add sponsor promissory notes, working-capital notes, or extension loans as line items.

- **Sponsor Name** — Full legal name
- **Sponsor Structure** — LLC, LP, Fund, exempted company; formation date if disclosed
- **Founder Shares** — Count held, class, and forfeitable portion, with cost basis appended using `@` — e.g. `12,458,333 Class B (up to 1,625,000 forfeitable) @ $25,000`. Cost basis is the aggregate $ only; no per-share price, and no separate Cost Basis line.
- **Forfeiture / Vesting** — Over-allotment-linked forfeiture, earn-outs, other restrictions
- **Sponsor Ownership** — Beneficial owners, controlling entities, and the managing / non-managing split of founder-share economics
- **Sponsor Domicile** — Jurisdiction of the sponsor entity
- **Sponsor Affiliation** — Platform, if any
- **Officer Founder Shares** — Each officer and their share count. No per-share price.
- **Independent Director Compensation** — Each director's founder share count. No per-share price, and do not note the absence of a cash retainer.
- **Administrative Fees** — Monthly $, payee, what it covers. If none, omit the field.
- **Conflicts of Interest** — Prior/concurrent SPAC involvement, overlapping roles, affiliated entities, related-party transactions. State the relationships and the entities; do not assess their severity.

## Section 6: Underwriter and Fees

- **Underwriter(s)** — Name(s), each with its % of units underwritten in brackets — e.g. `D. Boral Capital LLC (100%)`. Note "sole" if it is the sole bookrunner. Do not list unit counts.
- **Joint Bookrunner(s)** — Include only if there is one. If none, omit the field.
- **Upfront Fee** — $/unit and total $. Quote the sentence.
- **Deferred Fee** — $/unit and total $. **State explicitly whether the deferred fee is fixed or variable.** If variable or discretionary, quote the provision verbatim and give the range. State whether it is reduced pro rata for redeemed shares and whether the payee can be reallocated. This is the single most important field in the section — a deferred fee the underwriter can waive, scale, or hand to another FINRA member is a materially different instrument from a fixed one.
- **Advisory / Success Fee** — Include only if the underwriter or an affiliate receives a fee outside the underwriting discount (advisory, M&A, success, placement). Quote verbatim. State the % of gross, whether it sits in trust, and whether it is adjusted for redemptions.
- **Business-Combination Marketing Fee (BCMA)** — Include only if present; quote verbatim. If there is no BCMA, omit the field.
- **Other Underwriter Consideration** — One consolidated line covering the economic items only: representative/advisory shares (count), cash advance against expenses, expense-reimbursement cap, and any financing tail. Omit FINRA rule citations, lock-up boilerplate, registration-rights language, and voting obligations.
- **Discounts and Commissions** — Pricing table, per-unit and total, with and without over-allotment. Quote footnotes.
- **Total Underwriter Compensation** — Aggregate $ and as a % of gross IPO proceeds, itemized.

## Section 7: Sponsor Team

Depth is wanted here — this is the one section where fuller, longer bullets are welcome. Capture everything the filing discloses about each person. Present it as facts, not characterization: no "seasoned", "highly regarded", "well-positioned", "strong". List the roles, dates, entities, and outcomes and let them speak.

For each officer, director, and advisor, one bullet per item, as many as the filing supports:
- Full name, age, title, board class and term expiry
- Every prior and current role: entity, title, dates
- Institutional affiliations
- Education
- Location, if disclosed
- **SPAC history** — SPAC name, role, IPO size, outcome (merged with [target] / liquidated [date] / pending / withdrawn), each line source-tagged where resolved outside the filing. If the person has no prior SPAC, say so in these words and stop — no disclaimer, no framing.

After the individual bios, add these team-level fields, each as its own labeled bullet:
- **PIPE Capital Intentions** — Any disclosed intent to raise a PIPE, plus any named institution with capacity to fund one
- **Business Combination Criteria** — Stated criteria, as listed in the filing
- **Affiliated Business Combination Disclosure** — Whether the filing contemplates a combination with an affiliated entity, and the terms
- **Board Committees** — Audit, Compensation, Nominating, with chairs

## Section 8: Lockup

Keep this tight — durations and parties, not the full contractual recital.

- **Duration** — Per class, terse. e.g. `Founder shares: earlier of 3 months post-close or a post-combination liquidity event; $12.00 for 20/30 days (90 days post-close) early release. Private units: until close. Rep shares: until close + 180 days.`
- **Parties** — Who is locked (sponsor, officers, directors, underwriter). Note any anchor or non-managing member that is *not* locked.
- **Exceptions** — Permitted transferees and early-release triggers, in a few words. Do not reproduce the transfer-restriction paragraph.

End the output here.

---

## Edge Cases

- **S-1/A:** Proceed normally; note the amendment number in the Desk View header block.
- **F-1:** Same extraction; note F-1 status.
- **HTML filing (.htm) instead of PDF:** Use the tag-stripping snippet above; everything else is unchanged.
- **Multiple underwriters:** List all in Section 6, each with its % in brackets and individual fee allocations if disclosed. In the header block, list each with its % on the single Underwriter line.
- **Unnamed anchor / non-managing member:** Report as disclosed. Do not attempt resolution, and do not speculate about identity.
- **Unresolvable SPAC claim:** Report the filing's language, mark `unresolved`, and do not treat the filing's own count as verified.
- **Response too long:** Stop at a section break, say where you stopped, ask the user to say "continue." If the break falls between the two parts, the Desk View must already be complete before stopping.

