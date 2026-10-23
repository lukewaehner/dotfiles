---
name: spac-s1-extraction
description: "Full S-1 extraction and summary for SPAC IPO filings. Trigger whenever the user uploads an S-1 PDF (or references one already in context) and asks to 'extract', 'run the S-1', 'do the extraction', 'analyze this S-1', 'pull the terms', 'run the guide on this', 'S-1 review', or any request to systematically extract SPAC IPO terms from a registration statement. Also trigger when user says 'new S-1', 'just filed', or drops an S-1 PDF without further instructions — the default action is to run the full extraction + summary. This skill supersedes ad-hoc S-1 analysis. Always use this skill for S-1 extractions — do not attempt the extraction without it."
---

# SPAC S-1 Extraction & Summary Skill

## Overview

This skill extracts the full legal and economic terms from a SPAC S-1 registration statement, then produces a concise investment summary with bombs/deviations flagged. Output is delivered **in the chat body as structured prose** — not as a Word document or artifact.

## Workflow

1. **Read the S-1 PDF** using `pdftotext -layout` and targeted `grep`/`sed` to locate all required sections. The S-1 is typically 150–300 pages. Extract text first, then systematically search for each data point.
2. **Run Part 1: Full Extraction** — output all 9 sections in the chat.
3. **Print a clear divider** between Part 1 and Part 2.
4. **Run Part 2: Investment Summary** — output the condensed summary with bombs, anchor/sponsor, fees, and management table.

## Critical Rules

- **Do not summarize, paraphrase, infer, or assume** in Part 1. If a specific detail is not disclosed, state: "Not disclosed."
- **Do not hallucinate.** If you cannot find information after thorough search, say so explicitly.
- **Output everything in chat** — no Word documents, no artifacts, no file creation. Plain structured text with markdown headers and bullets.
- **Run both parts in a single response** if token limits allow. If you hit the limit, stop and tell the user to say "continue" to get the remainder.
- **Use the SEC EDGAR tools** (MeteoraMCP-AWS:edgar-filings, MeteoraMCP-AWS:edgar-filing-text, etc.) only if the user asks you to cross-reference or if the uploaded PDF is incomplete. The primary source is always the uploaded PDF.

## PDF Reading Strategy

```bash
# Step 1: Extract full text
pdftotext -layout "/mnt/user-data/uploads/[filename].pdf" /tmp/s1_text.txt

# Step 2: Systematic section hunting
grep -n "keyword" /tmp/s1_text.txt | head -20
sed -n 'START,ENDp' /tmp/s1_text.txt
```

Key sections to locate (search terms):
- Cover page / pricing table: "Public offering price", "Underwriting discounts"
- Sponsor Information: "Sponsor Information", "sponsor.*LLC"
- The Offering: "THE OFFERING"
- Trust Account: "trust account", "Continental Stock Transfer", "trustee"
- Private Placement: "private placement warrants", "private placement units"
- Founder Shares: "Founder shares", "Class B"
- Underwriting: "UNDERWRITING" (standalone section, usually near end)
- Legal Matters: "LEGAL MATTERS"
- Management: "Management", "Officers and Directors", "Committees of the Board"
- Proposed Business / Target: "PROPOSED BUSINESS", "Business Strategy", "Acquisition Criteria"
- Conflicts of Interest: "Conflicts of Interest"
- Lock-up / Transfer Restrictions: "lock-up", "Transfer Restrictions"
- Use of Proceeds: "USE OF PROCEEDS"
- Dissolution: "dissolution expenses"
- Trust Overfunding: "$10.0", "per Unit", "deposit.*trust", "overfunded", "in excess of \$10.00"
- Excess Working Capital: "working capital", "outside.*trust", "available to us", "Sources and Uses", "promissory note", "Sponsor.*loan"

## Part 1: Full Extraction

Output all 9 sections below. Use markdown headers (##) for sections and bold labels for fields. Use bullet points for multi-item fields.

---

### Section 1: Overview — [SPAC Name]

Extract from "Summary — The Offering" or equivalent:

- **SPAC Name**
- **SPAC Tickers** — Unit, Share, Warrant, Rights tickers
- **SPAC Counsel** — (i) U.S. counsel to the SPAC, (ii) non-U.S./jurisdictional counsel (e.g., Cayman Islands), (iii) underwriter's counsel. Include law firm names and specific legal functions. Found in "Legal Matters" section near end of filing.
- **Domicile of SPAC** — KY, DE, Cayman, BVI, etc.
- **SPAC Description** — Purpose, sector focus, sponsor platform background
- **Exchange** — Nasdaq Global Market, Nasdaq Capital Market, NYSE, etc. Include tier.
- **When Do Units Split** — Typically 52nd day, but check for variations
- **Publicly Traded Warrants/Rights** — Number of public warrants, number of private placement warrants (and who holds them). If rights, specify. If none, say "None."

### Section 2: Offering

- **Structure** — Unit composition (e.g., 1 share + 1/2 warrant)
- **Units Offered** — Total units, price per unit, warrant strike and terms
- **Timeline** — Duration to complete IBC, extension mechanics (auto vs. vote vs. deposit)
- **Over-Allotment Option** — Size and expiration

### Section 3: Trust Account

- **Total Amount Held in Trust** — Aggregate trust deposit at IPO (with and without OA)
- **Trust Per-Share Funding** — Exact per-share amount placed in trust at IPO ($10.00, $10.025, $10.05, $10.10, etc.). **FLAG PROMINENTLY IF > $10.00 (overfunded).** When overfunded:
  - State the excess per share (e.g., "$10.025 → $0.025/share overfunded")
  - State the aggregate dollar excess (e.g., "$0.025 × 25M units = $625K above $10.00 floor")
  - Identify the source of the overfunding deposit (typically a slice of PP proceeds, anchor commitment, or sponsor contribution)
  - Quote the source disclosure verbatim
  - Overfunding directly raises the redemption floor and IRR — it is a structurally positive feature and must be called out, not buried.
- **Trust Investment** — Quote the specific disclosure (Treasuries vs. demand deposit, maturity, money market fund conditions, ICA mitigation language)
- **Trustee Name**
- **Permitted Withdrawals** — Full permitted uses (taxes, working capital, dissolution). Include annual caps and rollover provisions.
- **Dissolution Expenses** — Maximum amount reserved
- **Redemption Mechanics** — Redemption rights, pricing formula, 15% cap, trust contribution terms
- **Extensions and Conditions** — Auto-extension, deposit-based, vote-based, BCA-triggered. Be specific.

### Section 4: Private Placement, Promote and Anchor Investors

**4.1 Private Placement:**
- Number of units/warrants
- Price per unit/warrant
- Total proceeds
- Participants (sponsor, underwriter, others)
- Sponsor purchase (units and dollar amount)
- Underwriter purchase (units and dollar amount)
- Non-managing sponsor investors (yes/no, details)
- Participant breakdown — For each purchaser: "[Name] — [X PP units/warrants @ $Y = $Z] — [N founder shares or 'indirect interest in N founder shares']"

**4.2 Anchor Investors:**
- Anchor status (yes/no)
- Investor identity
- Economic participation structure
- Terms (founder share economics, PP rights, lockups, preferences)
- Passive or active role

**4.3 Promote:**
- Promote size (number of founder shares)
- Promote % (Class B as % of post-IPO shares)
- Quote the anti-dilution / conversion formula verbatim
- Class B to A conversion ratio and terms

### Section 5: Sponsor / Admin Fees

- **Sponsor Name** — Full legal name
- **Sponsor Legal Structure** — LLC, LP, Fund
- **Founder Shares** — Total number held
- **Cost Basis** — Typically $25,000 / ~$0.003–$0.004 per share
- **Excess Working Capital** — Total cash available to fund operations, diligence, and the deal search outside the trust at IPO. Break into components:
  - (i) Portion of IPO proceeds NOT deposited into trust (typically used for offering expenses, UW upfront fee, initial WC)
  - (ii) PP proceeds in excess of any trust overfunding deposit (the bulk of usable WC at IPO)
  - (iii) Sponsor working capital loan / promissory note capacity — quote the cap and the conversion mechanic (often convertible into PP-style warrants at $1.00 at IBC)
  - (iv) Aggregate dollar figure and any post-offering-expenses net WC the issuer discloses
  
  Quote the disclosure verbatim from "Use of Proceeds" or the liquidity discussion. **Excess working capital is one of the strongest sponsor-quality signals in an S-1.** More excess working capital correlates with higher probability of a successful outcome — it lets the sponsor absorb one or more failed deal processes without having to replenish the budget mid-search. Thin WC frequently forces sponsors to raise external capital mid-search (sponsor promissory notes, anchor top-ups, related-party loans), which compromises deal terms. Always flag light excess WC explicitly.
- **Forfeiture/Vesting Terms** — OA-linked forfeiture, earn-outs, other restrictions
- **Sponsor Ownership** — Beneficial owners, controlling entities
- **Sponsor Domicile** — Jurisdiction of sponsor entity (not the SPAC)
- **Sponsor Affiliation** — Identify if affiliated with broader platform (Aries, Meteora, Cantor, Consellium, Quadro, etc.)
- **Sponsor Rights and Restrictions** — Lockups, voting commitments, redemption waivers, transfer restrictions on membership interests
- **Management Compensation (Founder Shares)** — List each officer and their share allocation
- **Independent Director Compensation** — List each director, shares, cash retainers, ownership mechanism
- **Administrative Fees** — Monthly amount, paid to whom, covering what
- **Conflicts of Interest** — Prior/concurrent SPAC involvement, overlapping roles, affiliated entities, related-party transactions

### Section 6: Underwriter and Fees

- **Underwriter(s)** — Lead book-running manager
- **Joint Bookrunner(s)** — If any
- **Upfront Fee** — Per-unit fee and total dollar amount, payable at closing. Quote the exact sentence.
- **Deferred Underwriting Fee** — Per-unit and total. Break into fixed, variable, and discretionary portions if applicable.
- **Business-Combination Marketing Fee (BCMA)** — Quote verbatim if present. If not found, state "Not disclosed."
- **Other Underwriter Consideration** — PP warrants, expense reimbursements, representative shares, legal fees, advisory roles
- **Discounts and Commissions** — Full pricing table (per-unit and total, with and without OA). Quote footnotes.
- **Total Underwriter Compensation** — Aggregate number if provided

### Section 7: Lockup

- **Lockup Duration** — Length in months or condition-based (e.g., 1 year post-IBC or $12.00 early release)
- **Parties Subject to Lockup** — Sponsor, directors, officers, anchors, etc.
- **Transfer Restrictions** — Details on restrictions and permitted transfers (affiliates, estate planning, FPAs, pro rata distributions, etc.)
- **Lockup Exceptions** — Early release provisions

### Section 8: Target

- **Target Sector** — Named industries, sub-sectors, geographic focus
- **Target Size and Criteria** — EV range, revenue/profitability thresholds
- **Strategic Rationale** — Why sponsor is pursuing this space
- **Technology Focus** — AI, digital assets, or other emerging tech explicitly mentioned

### Section 9: Sponsor Team

- **Sponsor Team Members and Independent Directors** — Each individual's full name, title, and concise professional biography covering: relevant expertise, notable prior roles, SPAC experience (names, roles, outcomes), institutional affiliations
- **SPAC Track Record** — Each team member's past SPACs with names, roles, and outcomes
- **PIPE Capital Intentions** — Any disclosed intent to raise a PIPE
- **Business Combination Criteria** — Stated criteria for evaluating targets
- **Affiliated Business Combination Disclosure** — Intent or possibility to merge with affiliated entity
- **Board Advisors** — Name and background of each advisor
- **Board Committee Memberships** — Audit, Compensation, Nominating committees with chairs identified

---

## DIVIDER

After Part 1, output:

```
---
---
# PART 2: INVESTMENT SUMMARY
---
---
```

## Part 2: Investment Summary

This is the analytical layer. Synthesize — do NOT just repeat Part 1. Use your judgment. Write in concise narrative or bullet form. Flag what matters.

### Header Block

One-liner fields:
- **SPAC Name**
- **Ticker**
- **Jurisdiction**
- **Offering** — [units × $10.00 = proceeds, unit composition, OA]
- **Trust Funding** — [per-share trust amount; if > $10.00 flag prominently as "OVERFUNDED +$0.0XX/share = $X.XM aggregate above $10.00 floor", with funding source]
- **Excess WC** — [aggregate dollar figure outside trust, components, qualitative assessment: "deep" / "adequate" / "light, likely needs mid-search raise"]
- **Private Placement** — [amount, instrument, who participates]
- **Timeline** — [base term + extension mechanics]

### Bombs / Key Deviations

Flag only **material deviations** from standard SPAC terms. Each bomb should be a bold "**Bomb:**" prefix followed by a concise explanation of what's non-standard and why it matters.

**Include if present:**
- Permitted withdrawals beyond standard taxes (working capital access from trust interest, excise tax withdrawals, operating cost funding)
- Timeline modifications (automatic extensions, milestone-based, deposit-based without vote)
- Automatic extensions without shareholder vote
- Founder promote above 25% of post-IPO shares
- Early access to trust principal or non-standard interest mechanics
- Sponsor controlled by offshore/opaque entity
- CEO/key officer with zero SPAC experience
- Prior SPAC from same platform that liquidated
- Sole bookrunner (no co-manager) with excessive total compensation
- Non-standard redemption mechanics
- Affiliated business combination risk
- **Light excess working capital outside trust** — flag if aggregate WC (PP excess + IPO retention + sponsor loan capacity) is materially below peer norms. Thin WC correlates with higher probability of failed search, mid-search capital raises (which compromise deal terms), or outright liquidation. Quantify the gap.
- **Trust overfunding** — flag prominently as a **positive structural feature** if CIT > $10.00. Note the per-share excess, aggregate dollars above the $10.00 floor, the funding source (PP slice, anchor, sponsor), and the yield-enhancement implication (overfunding raises the redemption floor and the IRR at any given purchase price).
- Any other provision that a sophisticated SPAC investor would flag as non-standard

**Exclude (these are standard, do not flag):**
- Standard dissolution expense language ($100K for liquidation)
- Standard 15% redemption cap
- Standard $100K annual working capital withdrawal cap (unless rollover or other enhancement makes it non-standard)
- Standard anti-dilution provisions

After bombs, list clean items with a checkmark prefix (✓) to confirm standard provisions that were reviewed and found clean.

### Anchor & Sponsor

- **Anchor Deal:** Yes/No + investor names and purchase details
- **Anchor Price:** $10.00/unit or discounted, with structure (IPO units vs. FPA vs. pre-IPO founder shares)
- **Sponsor:** Entity name + managing/non-managing members
- **Affiliations:** Related funds, prior SPACs, institutional connections
- **Sponsor Liquidity:** Excess working capital outside trust ($X.XM aggregate, broken into PP excess / IPO retention / sponsor loan capacity). Qualitative read on whether the sponsor can absorb a failed deal cycle without an external raise.

### Underwriting

- **Underwriter(s):** Names
- **Upfront Fee:** $/unit
- **Deferred Fee:** $/unit
- **Notes:** Discretionary/variable components, BCMA fee, PP warrants as additional compensation, effective total take rate

### Management & Board

Output as a markdown table:

| Name | Role | Background | Prior SPAC / Affiliation |
|------|------|-----------|--------------------------|

Include all officers, directors, and advisors. Keep backgrounds concise but informative. Always note prior SPAC outcomes (merged, liquidated, pending, delisted).

After the table, add a brief **Sector Fit Assessment** paragraph evaluating how well the team's background aligns with the stated target sector.

---

## Edge Cases

- **If the S-1 is an S-1/A (amendment):** Proceed normally. Note the amendment number in the header.
- **If the filing is an F-1 (foreign private issuer):** Same extraction, but note F-1 status.
- **If unit composition includes rights:** Extract right terms (conversion ratio, exercise conditions) in Section 2.
- **If there are multiple underwriters:** List all in Section 6 with individual fee allocations if disclosed.
- **If anchor investors are present:** Fully populate Section 4.2 with names, amounts, price per unit, and structure.
- **If the document is too large for a single response:** Stop at a natural section break, tell the user where you stopped, and ask them to say "continue."
