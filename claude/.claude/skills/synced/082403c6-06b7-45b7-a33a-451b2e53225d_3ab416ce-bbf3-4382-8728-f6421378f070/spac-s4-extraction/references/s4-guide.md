# S-4 Extraction Guide — Full Prompting Framework

## Instructions
- Tone: Spartan, factual, analytical.
- Do NOT respond in XML format.
- Source all information exclusively from the S-4 filing. Do not use external sources, prior knowledge, or web searches.
- Proceed section by section in order (1 through 12).
- For each item, present relevant information as disclosed in the S-4.
- Responses should accurately reflect the substance and details of the filing without adding interpretation or inference.
- Consolidate details that span multiple sections.
- Minimal bracketed context only to resolve genuine ambiguity.
- If a specific detail is not disclosed, write: **"Not disclosed."**
- Do not infer or assume anything beyond what is directly presented.
- Use tables for financial statements (balance sheet, income statement, cash flow, EBITDA reconciliation, debt schedule). Bullet points or clear section headers otherwise.

---

## Section 1: Fundamental Analysis – [Target Name]

### 1.1 Target Name
Full legal name of the target company. Match name in the Business Combination Agreement.

### 1.2 Business Model
What does the company do or provide? Is the business product-based, service-oriented, platform-driven, or asset-heavy? Recurring or transactional revenues?
- One-time sale vs. subscription/contractual
- Monetization method (data, licensing, physical services, advertising)
Provide a concise paragraph summarizing the model and its ability to capture value.

### 1.3 Stage of Development
Pre-revenue / early-revenue / commercial-stage / clinical-stage (biotech) / post-commercial / asset-only entity. Reference revenue, customers, product deployment, regulatory status, or commercial contracts.

### 1.4 Geography
- HQ location
- Countries of operation
- Revenue/geographic concentration risk
Note if tied to politically or economically unstable regions.

### 1.5 Sector / Subsector
Primary sector and relevant subsector (SPAC/VC taxonomy).
Examples: FinTech → Payments Infrastructure; Life Sciences → Diagnostics; Aerospace → Satellite Launch Services.
Classify with maximum specificity. Include "platform" or "infrastructure" if relevant.

### 1.6 Key Assets / Products / Services
Most important assets, contracts, or products owned or operated:
- Aircraft/fleet, software/IP, patents, regulatory licenses, data assets, operating subsidiaries
- Contracts or customers that materially support operations
Note owned vs. leased; call out mission-critical assets.

### 1.7 Go-to-Market Model
- Primary sales method (direct, agents, OEM)
- Primary customer base (individuals, enterprises, government)
- Disclosed customer concentration or retention metrics
Flag if >10% of revenue is concentrated in one client or if acquisition depends on specific marketing strategies.

---

## Section 2: General Deal Terms

### 2.1 Target Jurisdiction & Legal Structure
Legal jurisdiction of incorporation and likely tax domicile. C-Corp, Ltd., PLC, LLC, or other?
Include both incorporation and tax implications where possible.

### 2.2 Business Combination Terms

#### 2.2.1 Consideration Type
Form of consideration paid to target shareholders. 100% equity, any cash, seller notes, or hybrid? Flag contingent or discretionary components.

#### 2.2.2 Valuation
State equity value verbatim as disclosed (e.g., "$300,000,000 at $10.00 per share"). Separately extract any explicit enterprise value disclosure or derivation using clearly presented adjustments (net debt, cash). Do NOT substitute fairness opinion ranges unless they are the definitive transaction value. If enterprise value is not disclosed, state "Not disclosed."

#### 2.2.3 Sources and Uses
Extract sources and uses of capital. If no consolidated table, compile from narrative. If not disclosed, write "Not disclosed."

#### 2.2.4 Per-Share Exchange Ratio and Treatment of Existing Securities
- Exchange ratio mechanics or dollar-based value per share
- Treatment of in-the-money vs. out-of-the-money options
- Treatment of unvested equity or deferred plans

### 2.3 Transaction Structure
Identify each legal entity and its role:
- SPAC
- HoldCo / Pubco (post-close public company)
- Merger Sub(s)
- Seller(s) / Target(s)
Include full legal names and jurisdictions of each entity.

### 2.4 Termination
Conditions under which the BCA may be terminated:
- Who may terminate (SPAC, target, mutual)
- Key triggers (drop-dead date, shareholder approval failure, breach of reps/warranties)
- Termination fees or reverse termination fees (if any)
Quote termination language verbatim if short and definitive.

### 2.5 Earnout / Contingent Consideration
If applicable:
- Structure (stock-based, cash-based, milestone-based)
- Triggers (revenue, EBITDA, stock price targets)
- Time horizon / measurement period
- Total potential value or share count
- Recipient(s) (target shareholders, management, sponsor)
If no earnout: "Not disclosed."

### 2.6 Minimum Cash Condition
If applicable:
- Dollar amount required
- Sources counted toward the condition (trust proceeds, PIPE, backstop, FPA)
- Waiver provisions
- Flag if no PIPE or external financing exists to meet condition
If not mentioned: "Not disclosed."

### 2.7 Warrant Overhang
- Number of public and private placement warrants outstanding
- Percentage of pro forma company on a fully diluted basis
- Strike price and redemption terms
Highlight if warrant overhang is significant relative to float or equity value, or could pressure stock post-close.
If no warrants: "No warrants outstanding."

### 2.8 Rights Conversion
- Number of SPAC rights outstanding and conversion ratio
- When do rights convert (automatically at closing?)
Include sponsor-held rights if disclosed. Flag meaningful dilution.
If no rights: "No rights outstanding."

---

## Section 3: Capitalization and Ownership Post-Combination

### 3.1 Pro Forma Ownership
Extract post-close ownership under:
- No redemption scenario
- Maximum redemption scenario

Include for each scenario:
- Target shareholders
- SPAC public shareholders
- Sponsor and related parties
- Other named groups (PIPE investors, anchor investors)
- Total shares outstanding
State clearly if public shareholders are fully redeemed in max scenario.

### 3.2 Dilution Sources
Identify and quantify all dilution sources at or after closing:
- Public warrants
- Private warrants (Sponsor, anchor, affiliates)
- Founder shares / sponsor promote
- PIPE or forward purchase shares
- Earnout shares
- Convertible notes, SAFEs, debt-to-equity structures
If any category not applicable or not disclosed, explicitly say so.

### 3.3 Voting Control
Will the post-close company be a "controlled company" under Nasdaq/NYSE rules (>50% voting power held by one party)? Identify controlling shareholder and ownership vehicle.

### 3.4 Lock-Ups & Vesting
Summarize for Sponsor, Sellers, and insiders:
- Duration (6 months, 1 year, etc.)
- Performance-based earnouts (stock price triggers)
- Exceptions or early release conditions
Flag if terms are in an exhibit rather than the body.

---

## Section 4: Financials, Cash Needs & Liquidity Analysis

**Present all financial statements in clean, structured table format. Preserve original order, labels, and reporting periods. No bullet lists for financial tables.**

### 4.1 Target Company Balance Sheet
Full balance sheet as it appears in the S-4.
- Include balance sheet date and audited/unaudited designation
- Preserve column headers exactly
- Two-column table format
- Exact order and wording of line items
- Faithful reproduction — do not interpret, reword, or omit

### 4.2 Target Company Income Statement
Full income statement as filed.
- Include reporting period and audited/unaudited designation
- Preserve all column headers and line items
- If multiple periods shown, include all in labeled tables
- Verbatim tabular reproduction

### 4.3 Target Company Cash Flow Statement
Full cash flow statement as filed.
- Include reporting period and audited/unaudited designation
- All sections: Operating, Investing, Financing Activities
- All subtotals and totals
- Verbatim tabular reproduction

### 4.4 Adjusted EBITDA Reconciliation
If disclosed: reproduce full reconciliation table exactly as presented.
If not disclosed: "Adjusted EBITDA not disclosed in S-4."
Include period covered and whether historical or projected. Note partial disclosures.

### 4.5 Debt Schedule
Extract from notes to financial statements only (not balance sheet totals).
Present as structured table with columns:

| Instrument | Principal | Rate | Maturity | Secured/Unsecured | Related Party | Notes |

If not disclosed: "Debt details not disclosed."

### 4.6 Going Concern
Determine whether management or auditor raised substantial doubt:
- Explicit "substantial doubt" or similar going concern language
- Key financial indicators (working capital deficit, accumulated losses, negative operating cash flow)
- Dependence on raising capital
- Auditor commentary (emphasis-of-matter or qualification)
- Management's mitigation plans

Quote directly if "substantial doubt" or similar phrase used. If no concern: "Not disclosed."

### 4.7 Projections
If disclosed:
- Revenue, Adj. EBITDA, net income, FCF, or key operating metrics
- Projection period and frequency (annual/quarterly)
- Use in valuation (fairness opinion, DCF, investor materials)
- Key assumptions
- Disclaimers

If not disclosed: "Not disclosed."

### 4.8 Post-Closing Liquidity

#### 4.8.1 Expected Cash at Close
- SPAC trust cash post-redemptions
- Less: transaction expenses
- Net cash to combined company
Note whether PIPE, backstop, or other external funding contributes.

#### 4.8.2 Use of Funds
- Working capital
- Transaction/legal expenses
- Debt repayment
- Capex or R&D
- Operating runway / corporate overhead
- Minimum cash condition (if applicable)
Summarize stated or implied capital allocation.

---

## Section 5: PIPE / Forward Purchase Agreement / Other Financing

### 5.1.1 Committed Amounts
Total committed proceeds from PIPE, FPA, or other financings. Include firm and conditional commitments.

### 5.1.2 Pricing and Terms
Purchase price per share or unit and any preferential rights:
- Equity or debt?
- Discount to $10.00?
- Preferred equity structure?
- Registration or voting rights?
Flag non-standard or investor-favorable terms.

### 5.1.3 Named Investors or Backstop Parties
Disclose PIPE/FPA investors or backstop/anchor parties. Highlight if insiders or related to sponsor.

### 5.1.4 Conditions & Terminations
Material conditions to funding, and any terminations, amendments, or withdrawals. Flag financing subject to redemption thresholds, stock price, or other triggers.

### 5.1.5 Conversion Instruments
Identify any convertible securities (notes, SAFEs) used instead of or alongside PIPE equity. Include conversion price, maturity, and cap/discount.

---

## Section 6: Funding History & Capital Structure

### 6.1 Pre-SPAC Financing Rounds
Any prior funding rounds (Seed, Series A–D) with valuation/raise amounts. If round names aren't used, extract any past equity issuance events with pricing or investor data.

### 6.2 Insider or Related Party Loans
Loans or funding from insiders, sponsor, or affiliates:
- Principal amounts
- Interest rates
- Maturity and repayment terms
- Whether convertible (e.g., into warrants)
Include working capital loans, extension loans, and sponsor advances.

### 6.3 Structured / Potentially Predatory Instruments

#### 6.3.1 High-Interest Loans (>15–20%)
Flag any debt instruments with rates above 15–20%. Include bridge loans, PIK debt, or insider loans with penal terms.

#### 6.3.2 Reverse Factoring / Disguised Debt
Identify supply chain financing, reverse factoring, or embedded financing liabilities. Flag off-balance sheet items or hidden leverage.

### 6.4 Capital Stack Complexity
Determine whether target has:
- Preferred shares or different classes
- Liquidation preferences
- Convertible equity or debt
- Dual-class voting rights
If only ordinary/common equity: note capital stack is simple.

---

## Section 7: Warrant & Convertible Securities

### 7.1 Post-Close Capital Stack
Determine whether post-close structure includes:
- Preferred shares
- Liquidation preferences
- Dual-class equity or voting seniority
- Any structural seniority over ordinary/common shares
If only ordinary/common equity: note capital stack is simple.

### 7.2 Treatment of Warrants at Closing
What happens to existing public and private warrants:
- Assumed, exchanged, or canceled?
- Securities they convert into?

#### 7.2.1 Exercise Mechanics
- Exercise price
- Share per warrant ratio
- When warrants become exercisable
- Expiration date

#### 7.2.2 Cash vs. Cashless
- Under what conditions does cashless apply?
- How are shares calculated under cashless exercise?
Flag if cashless applies only when registration isn't effective.

#### 7.2.3 Early Redemption Triggers
- Stock price trigger (e.g., $18.00 VWAP for 20/30 days)
- Redemption price (typically $0.01)
- Notice period before redemption
Include timing (e.g., starts 90 days after closing).

#### 7.2.4 Other Convertibles
- Convertible notes
- SAFEs
- Sponsor working capital loans
Include key terms: conversion price, cap, rights.

---

## Section 8: Key Risk Factors

### 8.1 Business-Specific Risks
Extract key risks related to target's business model, operations, and market exposure:
- Technology development or failure
- Regulatory or licensing exposure
- Customer concentration or geographic reliance
- Supply chain dependencies
- Key vendor risk
Highlight risks that could materially impair operations or revenue.

### 8.2 Legal / Financial / Disclosure Risks
Disclosed legal, regulatory, or financial reporting risks:
- Ongoing litigation or legal disputes
- Loss of material contracts or key licenses
- Tax exposure or audits
- Related-party governance concerns

#### 8.2.1 Going Concern, Internal Controls, FX or Inflation Risk
- Going concern qualification (auditor or management)
- Internal control weaknesses or exemptions
- Currency risk or inflation exposure (especially in high-risk geographies)
Quote directly if "substantial doubt" or similar appears.

#### 8.2.2 Impact on Downside Recovery
Assess whether disclosed risks would impair investor recovery:
- Asset-light business (leased equipment)
- High burn, negative equity
- No PIPE or backstop capital at close
- Heavy reliance on future funding
Comment if equity recovery would likely be minimal in a distressed case.

---

## Section 9: Insider Conflicts, Sponsor Incentives & Anchors

### 9.1 Insider Economics

#### 9.1.1 Promote Shares or Earnouts
- Number of promote/founder shares
- Earnout terms (if any)
- Transfers to third parties (advisors, sellers)
Flag if promote is not subject to vesting or tied to performance.

#### 9.1.2 Side Deals for Advisory, Board Seats, or Consulting
- Board appointments
- Advisory roles
- Consulting or service agreements tied to equity
Include equity or compensation provided.

### 9.2 Discounted Share Purchase
Determine whether insiders received securities at:
- Nominal or below-market value
- Preferential warrant pricing
- Free equity transfers or equity-linked compensation
Specify purchase price vs. market value if available.

### 9.3 Anchor Investors
Identify anchor or strategic investors:
- Whether they received Class B or private shares
- Whether they paid for their equity
- Any special governance, nomination, or economic rights
Flag undisclosed pricing or early-stage insider allocations.

### 9.4 Insider Economics Independent of Performance
Conclude with a clear **Yes or No**: are insiders positioned to benefit regardless of post-close performance?
Assess:
- Insider equity not subject to vesting, earnouts, or performance milestones
- Insiders retain significant equity even in high-redemption or poor trading scenarios
- Structural protections or discounted entry points providing asymmetric upside

---

## Section 10: Management and Service Providers

### 10.1 Management
Post-close management team and board:
- Names and titles of executive officers and directors
- Biographical details (prior roles, public company/SPAC experience, sector expertise)
- Which individuals are from the SPAC vs. the target
- Changes from pre-close to post-close team composition
Include employment agreements, retention packages, or equity grants tied to deal closing.

### 10.2 Service Providers
All financial, legal, and other advisors:
- M&A advisors and capital markets bankers (including fairness opinion providers)
- Legal counsel to SPAC and to target
- Auditors pre- and post-close (note if changing)
- Fees paid or payable (cash, equity, or success fees)
Flag if compensation is contingent on deal close or includes equity. Include conflicts or related-party affiliations.

---

## Section 11: Auditor Quality & Financial Integrity

### 11.1 Auditor Identity
Identify independent auditor(s) for target and SPAC separately:
- Tier 1 global firm (PwC, KPMG, Deloitte, EY) or lesser-known?
- PCAOB registered?
Flag if lesser-known or unregistered auditor, especially in emerging market jurisdictions.

### 11.2 Accounting Standards
- Target: U.S. GAAP, IFRS, or local GAAP?
- SPAC: typically U.S. GAAP
- Do pro forma financials consolidate two standards?
Flag inconsistencies and whether reconciliations are disclosed.

### 11.3 Audit Red Flags

#### 11.3.1 Recent Restatements
- Restated past financials?
- Reissued audit opinion?
- Material misstatements or adjustments?
Quote restatement reason and period if applicable.

#### 11.3.2 Modified Audit Opinions
- Going concern qualification
- Emphasis of matter paragraph
- Scope limitation or qualified opinion
Quote "substantial doubt" or "material uncertainty" language if present.

#### 11.3.3 PCAOB Issues or Non-Compliance
- Known PCAOB inspection deficiencies
- Lack of PCAOB registration
- Sanctions, fines, or regulatory scrutiny
Flag if any party operates in jurisdiction with PCAOB access limitations (China, historically Argentina, etc.).

#### 11.3.4 Tax Status
- Is the SPAC or post-close entity expected to be a PFIC?
- Adverse tax implications for U.S. holders?
- Non-U.S. holding structures creating tax uncertainty?
Summarize whether a PFIC election is recommended and how it affects U.S. taxable investors.

---

## Section 12: Valuation & Public Market Readiness

### 12.1 Valuation Support

#### 12.1.1 Third-Party Fairness Opinions
If obtained:
- Name of provider
- Date of opinion
- Scope of fairness (to public shareholders or board)
Include limitations or disclaimers mentioned.

#### 12.1.2 Peer Comparables or DCF Support
- Public comp multiples
- Discounted cash flow analysis
- Selected transactions or precedent deals
- Final implied enterprise and equity value ranges
Report weighting of methods and adjustments (net debt, leases).

### 12.2 Profitability & Runway
- Historical and projected Adj. EBITDA, net income, and FCF
- Current or projected cash burn
- Disclosed timeline to break-even or profitability
- Capital needs or plans to raise post-close
Flag if no clear runway or heavy reliance on future capital raises.

### 12.3 Governance Readiness

#### 12.3.1 Board Standards
- Independent board majority?
- Audit, Compensation, and Nominating/Governance Committees formed?
- Audit Committee financial expert designated?
Include planned charters or policies if mentioned.

#### 12.3.2 Internal Controls / SOX Readiness
- Emerging Growth Company (EGC) status?
- Exempt from SOX 404(b) auditor attestation?
- Material internal control weaknesses or remediation plans?
Flag if internal control disclosures are sparse or non-committal.
