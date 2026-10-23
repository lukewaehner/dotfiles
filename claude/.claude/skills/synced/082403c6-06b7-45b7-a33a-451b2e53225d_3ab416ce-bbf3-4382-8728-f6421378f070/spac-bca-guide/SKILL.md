---
name: "spac-bca-guide"
description: "Meteora's primary SPAC BCA extraction — a 'Read on top, lean facts below' workup. Trigger on any BCA, merger 8-K, press release, or investor deck — or 'run the BCA guide', 'extract the BCA', 'pull the BCA terms', 'BCA review', or a filing dropped with no instructions. Leads with a Snapshot + deal-quality Desk Read written as terse trading-desk bullets (not narrative prose), then a decision-useful lean extraction ordered so valuation, earnout, financing, and termination risk sit up top and governance boilerplate at the bottom. For full S-4/proxy extraction (financial statements, projections, going concern) use spac-s4-extraction instead."
---


# SPAC BCA Extraction (Read on top, lean facts below)

## Overview

Two halves, printed top-down so a PM gets the judgment first and the record last:

- **THE READ** — Snapshot + Desk Read. Opinionated; the value-add. Assessment and verdict are *wanted* here.
- **THE FACTS** — lean, reordered extraction. Figures and verbatim clauses only, each stated **once**, no assessment, no fluff.

Output in chat unless asked for email or document.

**Canonical print order** (write the Read last, print it first):
1. Snapshot
2. Desk Read
3. Overview *(deal identity)*
4. Transaction Structure
5. Valuation & Consideration *(the money)*
6. Earnout / Contingent Consideration
7. Trust & Redemptions
8. PIPE & Financing
9. Termination Rights & Fees
10. Governance & Lockups *(detail)*
11. Warrants & Rights *(detail)*
12. Target Business Summary *(detail)*

Why this order: the old guide followed the BCA's own TOC — buried valuation, earnout, and termination risk behind structural boilerplate. This order says each fact once and leads with what the desk actually reads first.

## THE #1 RULE: THIS IS A TRADING DESK NOTE, NOT A REPORT

This is read by someone who needs to make a trading decision in the next five minutes, not someone settling in with a coffee. Every sentence in THE READ must survive the cut test: if you can delete a clause and lose no information, delete it.

- **Bullets and fragments, not paragraphs.** Default to short bullets. If a paragraph is unavoidable, cap it at 2 sentences.
- **No throat-clearing.** Never open a line with "It's worth noting," "Importantly," "The Company believes," or similar filler. State the fact or the read.
- **Lead with the number or the verdict, not the setup.** "$45mm MCC not covered by the $35mm PIPE alone" beats "There is a minimum cash condition that the parties have agreed to, and it is worth examining whether the PIPE proceeds are sufficient to cover it."
- **One idea per bullet.** Don't chain three observations into one flowing sentence — three bullets.
- **Cut adjectives that don't carry data.** "significant," "robust," "compelling" — either quantify it or cut it.
- **This applies to the ENTIRE Desk Read, every subsection, no exceptions.** A subsection that reads like a paragraph from an equity research report has failed, no matter how accurate its content.

## Workflow

1. **Locate the source.** BCA is typically Exhibit 2.1 to the announcement 8-K.
   - Uploaded PDF → `pdftotext -layout`
   - No file → `edgar-filings` (8-K, date ≈ announcement) → `edgar-filing-index` for EX-2.1 → `edgar-filing-text`. For the 8-K body use `extract-8k` (Item 1.01 = deal summary; 9.01 = exhibit list).
   - Deck or press release in chat → work from context directly.
2. **Pull internal context.** Run `spac-details` for trust balance, per-share trust, positions, warrant/rights composition, deadline. Pull the Meteora memory doc if one exists — this is also usually the fastest source for target business description and named CEO/principal bios, since it's already been vetted.
3. **Assemble THE FACTS** — strictly from the filing.
4. **Write THE READ** — go beyond the four corners; cite what you pull. Draft it, then re-read it once specifically hunting for anything you can cut — assume the first draft is 30% too long.
5. **Print in canonical order.** One response if length allows; else stop at a break and say "continue."

## Output discipline — applies to THE FACTS, not the Read

- **Report, don't assess.** State the figure; characterization belongs only in the Read.
- **Verbatim for legal clauses.** Termination triggers, breakup/RTF provisions, earnout conditions, PIPE conditions, minimum cash — quote directly. Never paraphrase a legal commitment.
- **Figures over sentences.** A dollar amount, share count, ratio, or date should be that, not prose.
- **Say each fact once.** Snapshot is the only headline digest; the detail sections add new granularity.
- **Omit empty fields; don't report the absence of a term.** Reserve "Not disclosed." for fields where absence is itself a fact (minimum cash condition, breakup fee, named PIPE investors).
- **Don't infer or extrapolate.** If the filing doesn't say it, it doesn't go in.

## Delivery — chat vs. email are different render targets

The markdown this skill produces (`#` headers, `===` dividers) renders in **chat** but shows up as raw text in an email body. So:

- **In chat:** markdown is fine — print as above.
- **In an email:** render as **HTML** — real `<h2>` section headers, `<ul>/<li>` bullets, `<table>` for structured data. Set `body_is_html=true` / `content_type=HTML`. **Never** send the raw markdown/`===` version as a plain-text email.
- **Sender identity:** send internal desk notes from the intended person's own mailbox (Vik's Outlook / send-as-me = `vik@`), **not** a shared/relay account. If a send connector reports "not signed in," re-verify (`whoami`/retry) before concluding it's down — never silently send under a different identity; if you can't send as the intended sender, stop and confirm.
- **Thread:** post as a **reply on the existing internal chain** (reply-all to Filings@), keeping the thread; don't start a new one.
- **Pre-send self-check:** (1) sender = intended identity, (2) body is HTML, (3) replying in-thread.

---

# THE READ (write last, print first)

## Snapshot

One tight block — the five-second read. Every line is a fragment, not a sentence.

- **[SPAC Name] · [Tickers: Common | Warrants | Rights] · BCA signed [M/D/YYYY] · [Domicile] · [Underwriter]**
- **Target:** [Target Name] · [jurisdiction] · **EV:** $[upfront]mm upfront + $[earnout]mm earnout = $[total]mm · **Structure:** [merger type in one clause]
- **What they do:** [one line, plain language — what the target actually sells/builds/operates. No jargon, no mission statement.]
- **CEO of target:** [Name] — [one line: background, one credential or red flag, nothing else]
- **CEO/Chairman of SPAC:** [Name] — [one line: prior SPAC track record or "first-time sponsor"]
- **Trust:** $[balance]mm · $[per share]/share · [N]mm shares outstanding · **Deadline:** [date]
- **PIPE:** $[size]mm ([instrument — e.g. "Series A 12% pref + 100% warrant coverage"]) · Committed / Soft · **Min cash condition:** $[X]mm ([does / does not] clear on PIPE alone — one clause)
- **Outside date:** [date] · **Expected close:** [quarter]
- **Prior Meteora interactions:** [memory doc / Outlook hits on target or sponsor — or "none found / not checked"]
- **Verdict:** [one line — the call and the single thing not to credit]

## Desk Read

Voice per `references/vik-brain.md`: plain, skeptical, specific, `=` for "which means," real-vs-optical, no laundering the sponsor's framing. Bullets, not paragraphs — see "THE #1 RULE" above. Target length: fits on one screen without scrolling. If it doesn't, cut, don't shrink the font.

1. **Who's this deal.** Bullets only:
   - Sector heat check — one line: is this sector hot right now (capital flowing in, comps re-rating — name the comp move) or tired (post-hype, multiple compression, name the tell)? This context changes how much premium the market will tolerate.
   - Sponsor capability — one line: prior SPAC track record (named deals, outcomes) or "first-time sponsor, 0-for-0."
   - Execution complexity flag — one line, only if cross-border/FDI/multi-jurisdiction: name the specific risk, don't just say "complex."

2. **The financing picture.** Bullets only:
   - Trust vs. deal size — one line with the raw numbers.
   - **Trust is a redemption-contingent number, not cash in hand** — state what the deal actually needs to close (MCC, PIPE) against what's *likely* retained after redemptions, not the full headline trust balance. A $300mm trust does not mean $300mm shows up at closing.
   - PIPE quality — one line: committed/soft, sized vs. the gap, investor quality (named institution vs. "unnamed").
   - Extension/outside-date mismatch — one line, only if it exists, with the date math.

3. **The tells.** 3–5 bullets, each ONE line, format: **[Tell name]:** what it is → why it matters → real or optical. Do not write paragraphs here — this section has been the single biggest complaint on prior output. Example format:
   - **No breakup fee:** §8.02 voids all liability except willful breach/fraud = symmetric clean walk, no deterrent either side.
   - **Founder felony conviction:** [name], 2016 IRS-fraud plea, kept off the board = economic control without governance accountability.
   Cover only what's actually present: non-standard termination triggers, earnout aggression vs. stage, asymmetric fees, antitrust/FDI jurisdiction count, cheap walk rights, governance red flags.

4. **Net.** 2-4 bullets max. What to credit, what to discount, the actionable lean. End with the trade, not a summary of the read. "Own common near trust for yield, don't touch warrants until PIPE clears the MCC" is the target format — one line, not a paragraph.

---

# THE CALL (decision-useful; lean)

### Section 1: Overview

- **SPAC** — full legal name · domicile (two-letter code) · common ticker · warrant ticker · rights ticker (omit absent classes)
- **Target** — full legal name · jurisdiction of organization
- **ListCo / PubCo** — name and jurisdiction if a new holding entity is formed; else omit
- **BCA signed** — M/D/YYYY
- **Announcement** — 8-K / press release date
- **Parties** — SPAC, Target, Merger Sub, ListCo; any additional named entities

### Section 2: Transaction Structure

Numbered steps in execution order. Use the filing's own language for each step's legal character. Flag any non-standard structures (multi-step exchange → merger, Dutch N.V. conversion, share contribution rather than direct merger).

- **Step sequence** — numbered; label each step's type (exchange, merger, conversion, contribution, amalgamation)
- **Surviving entity** — which entity survives / is the listing vehicle
- **Securities conversion at Merger Effective Time** — how each class of SPAC shares converts; SPAC warrants; SPAC options/rights
- **Tax treatment** — stated intended treatment (§351, §368(a)(F), etc.) — quote verbatim

### Section 3: Valuation & Consideration

- **Total deal value** — upfront + earnout = total, as stated
- **Upfront EV** — $; note pre/post-money if disclosed
- **Consideration form** — shares, cash, or mix; per-share deemed value if stated
- **Share Consideration** — MANDATORY, always compute even if the filing only states a dollar figure: total shares issued to target holders = deal value ÷ deemed price/share (show the math, e.g. "$4.0bn ÷ $10.00 = 400.0mm shares"). State what % of pro forma shares outstanding this represents if the PF share count is derivable (target shares ÷ [target + SPAC public + sponsor promote + PIPE]). This is a top-line number a PM will ask for first — never bury it or omit it because the filing only gave the dollar figure.
- **Exchange Ratio** — stated formula; quote verbatim if formula-based
- **Sources & Uses** — if disclosed, reproduce as bullet lines (Sources / Uses must balance); if not: "Not disclosed."
- **Super-voting / dual-class** — Yes/No; if Yes: class, ratio, holders
- **Minimum cash condition** — exact figure and source — quote verbatim; if absent: "Not disclosed. ⚠️ Confirm in BCA exhibit."

### Section 4: Earnout / Contingent Consideration

Omit section if no earnout.

- **Total earnout value** — $
- **Deemed share value** — $/share

Per tranche (label Tranche 1 / 2 / 3):
- $ value · implied shares (= $ ÷ deemed price)
- Trigger — quote verbatim (operational milestone, EBITDA threshold, stock price, date)
- Deadline
- Forfeiture — what happens if missed

- **Acceleration** — change-of-control vesting — Yes/No; quote if present
- **Recipients** — which shareholders participate
- **Earnout share lock-up** — per tranche if differs from general lock-up

⚠️ Flag: targets denominated in non-USD currency; milestones requiring rapid commercialization by an early-stage business; no forfeiture mechanic.

### Section 5: Trust & Redemptions

Pull live figures from `spac-details`.

- **Trust balance** — $; source
- **Per-share trust** — $/share
- **Class A shares outstanding** — count
- **SPAC liquidation deadline** — date; flag if shorter than BCA outside date
- **Redemption mechanics** — quote the BCA clause; flag full-redemption survival language or redemption cap
- **Extension status** — extensions used; deposit per extension if applicable

⚠️ Flag if trust deadline predates BCA outside date — the SPAC must extend before the deal can close.
⚠️ Flag in the Read (Section 2 of Desk Read), not just here: trust balance is pre-redemption. Don't let the headline number imply that's what closes with the deal.

### Section 6: PIPE & Financing

If no PIPE: "No PIPE disclosed." and omit sub-items.

- **Total PIPE size** — $
- **Committed / soft** — state which; quote any "subject to investor's IC" hedge

Per tranche / investor class:
- **Investor** — named or "unnamed institutional investor"
- **Instrument** — common, preference (state series), convertible notes, PIPE Warrants
- **Amount** — $ · share count · price or stated value per share
- **Key terms** — coupon (if pref), conversion terms, warrant coverage %, strike
- **Conditions** — quote any closing conditions on the PIPE

- **Sponsor loan conversion** — amount, instrument, and terms if applicable
- **Sponsor share transfer** — count and recipient if applicable
- **Backstop / FPA** — Yes/No; if Yes: counterparty, amount, structure

⚠️ Flag: structured pref + full/near-full warrant coverage = expensive paper; soft/uncapitalized PIPE; PIPE smaller than trust gap; PIPE + assumed trust retention that doesn't clear the minimum cash condition (do the arithmetic explicitly — this is the single most common gating risk on these deals and must never be left implicit).

### Section 7: Termination Rights & Fees

- **Termination triggers** — numbered list; for each: which party may terminate + triggering event. Quote verbatim for non-standard triggers.
- **Outside date** — date; extension mechanism; who controls it
- **Bespoke / unusual triggers** — flag and quote (shareholder-undertaking deadline, state-fund consent obligations, regulatory-clearance hard walk rights)
- **Breakup fee** — $ · who pays · triggering condition (quote verbatim); if none: "No breakup fee; parties liable for willful breach or fraud only."
- **RTF** — $ · who pays · triggering condition (quote verbatim); if absent: "Not disclosed."
- **Other fees** — additional obligations (consent-failure fees, etc.); amount and trigger
- **Survival on termination** — what survives beyond standard confidentiality; quote anything non-standard

⚠️ Flag: breakup fee < 2% of upfront EV; asymmetric fee structure; bespoke triggers giving a cheap walk before shareholder vote.

---

# THE FACTS (reference detail — bottom)

### Section 8: Governance & Lockups

**8.1 Board**
- Post-close board size
- Seat allocation — by party (target / SPAC / sponsor / independents)
- Sponsor rights — board seats vs. observer-only; nominating rights

**8.2 Voting Agreements**
Per agreement (Sponsor Support, Shareholder Support, etc.):
- Parties · key commitments (vote in favor, waive anti-dilution, forfeit warrants, etc.)
- % of shares covered if stated
- Shareholder Undertaking — threshold and delivery deadline

**8.3 Lock-ups**
Per class or party:
- Exempt shares — % not subject to lock-up
- ODA holders — daily volume cap, price floor, duration
- Hard lock-up — tranche-by-tranche: [N months post-Closing] or earlier if [N]-day VWAP > $[X]
- Earnout share lock-up — per tranche if different
- Parties covered

### Section 9: Warrants & Rights

- **Public warrants** — count (from S-1/10-K if not in BCA); conversion at Merger Effective Time; strike; expiry
- **Private warrants** — count; treatment (surviving, forfeited, converted); quote if forfeited
- **PIPE Warrants** — count; coverage ratio; strike; expiry if stated
- **Rights** — count; conversion ratio; timing; dilution
- **Total warrant dilution** — implied shares on full exercise (only if counts are disclosed)

### Section 10: Target Business Summary

Facts from the BCA only — do not import external knowledge, except the Meteora memory doc if one exists (cite it as the source).

- **Business description** — one line; quote the Recitals or "Information About" section where possible
- **Stage** — quote or paraphrase the closest filing phrase ("early-stage company with a history of financial losses," "revenue-generating," "pre-commercialization")
- **HQ** — city / country
- **Key assets** — named facilities, IP, licenses, customer contracts disclosed in BCA
- **Existing convertible notes / debt** — if disclosed; treatment at close
- **Consent holders** — any named third party with consent or veto rights (state-fund, strategic partner); quote the BCA provision
- **Antitrust / FDI jurisdictions** — list as stated in the BCA
- **Management named in BCA** — signing parties, key employees, earnout recipients only; Name · Title · Role in transaction. Do not fabricate bios from external sources.

---

## Edge Cases

- **No BCA exhibit yet (only 8-K Item 1.01):** Work from the 8-K body; note the full BCA exhibit is unread and flag fields that require it.
- **Foreign private issuer / F-4:** Same extraction; note F-4 status in Section 1.
- **Deck or press release only:** Extract what is disclosed; mark every field requiring the BCA as "Requires BCA exhibit."
- **Large BCA PDF (>40,000 lines):** Use grep anchors + sed ranges; do not read end-to-end.

```bash
grep -n -iE "enterprise value|equity value|upfront consideration" /tmp/bca.txt | head -20
grep -n -iE "earn.?out|contingent consideration|milestone" /tmp/bca.txt | head -20
grep -n -iE "minimum cash|minimum available cash" /tmp/bca.txt | head -20
grep -n -iE "PIPE|subscription agreement|backstop|forward purchase" /tmp/bca.txt | head -20
grep -n -iE "termination|outside date|break.?up fee|reverse termination" /tmp/bca.txt | head -20
grep -n -iE "lock.?up|transfer restriction|orderly disposition" /tmp/bca.txt | head -20
sed -n 'START,ENDp' /tmp/bca.txt
```

- **Multi-step structure:** Number and label each step in Section 2; do not collapse.
- **Output too long:** Stop at a natural section break and tell the user to say "continue."

## Revision Log (why the format looks the way it does — read before deviating)

- **Brevity is not optional.** Earlier drafts of this skill produced Desk Read sections that were accurate but written like textbook/equity-research prose — multi-sentence paragraphs per point. Feedback from the desk: this is unusable for fast trading decisions. Every Desk Read subsection must be short bullets. If you catch yourself writing "which is important because" or stringing three clauses together with commas, stop and break it into bullets.
- **Snapshot must answer "who's running this" and "what do they do" without a follow-up question.** Missing the target's one-line business description and the two CEOs' one-line backgrounds was a recurring gap — always include them, even briefly.
- **Trust ≠ cash at closing.** Always caveat headline trust balances against redemption risk, both in Section 5's facts and explicitly in the Desk Read's financing bullet.
- **Share Consideration is not optional in Section 3**, even when the BCA/8-K states the deal only in dollar terms — always back out the implied share count and, where derivable, the resulting ownership split.

