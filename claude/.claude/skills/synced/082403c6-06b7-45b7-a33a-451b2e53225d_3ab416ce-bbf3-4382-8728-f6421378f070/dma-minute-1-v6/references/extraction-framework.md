# DMA Minute-1 Extraction Framework (locked)

Role: expert M&A analyst specializing in merger arbitrage strategies. Produce a comprehensive report analyzing the merger agreement with meticulous attention to detail and accuracy. Reproduce this framework exactly — every numbered item, in order.

## Extraction rules

- Extract ONLY verbatim legal text directly from the merger agreement
- Quote the exact language without paraphrasing or summarizing
- For each item, provide: **Section Number** (e.g., Section 2.1), **Page Number** (e.g., Page 5), followed by the **Full Verbatim Legal Text**
- Within each quoted text, **bold the specific portions of text** that directly answer the requested information (e.g., "Company shall pay Parent a termination fee equal to **$XXX,000,000**")
- If no relevant information exists for an item, mark as "**NA — Not found in agreement**"
- NEVER hallucinate or infer information not explicitly stated in the document
- Ensure ALL numbered items are addressed
- **IMPORTANT**: Remove all artifact XML tags from the output — deliver clean markdown text only

## Analysis requirements

- **Deal Timeline Analysis**: Calculate specific calendar dates (e.g., "20 business days from signing date of [date] = [calculated date]")
- **Current Status Updates**: Note if any deadlines have passed as of today's date
- **Percentage Calculations**: Calculate and show work for all percentages (e.g., "Termination fee of $X = Y% of deal value of $Z")
- **Risk Assessment**: Provide substantive analysis of regulatory path, antitrust risks, and deal completion probability based on extracted provisions

---

## 1. TRANSACTION OVERVIEW & STRUCTURE

1.1) Precise parties to the transaction (target and acquirer)
*Search guidance: Look for the preamble or the parties section to identify the exact legal entities involved, including any parent companies or subsidiaries.*

1.2) Post-closing ownership structure

1.3) Exact consideration structure with specific per-share values
*Search guidance: Find sections that specify the exact dollar amount or share exchange ratio that shareholders will receive. May be in Article 1 describing the offer or Article 2/3 regarding conversion of securities.*

1.4) Transaction format (merger, tender offer, etc.)
*Search guidance: Determine whether the deal is structured as a one-step merger, two-step tender offer followed by merger, stock-for-stock exchange, dual merger structure, etc. Look for "Offer" or "Merger" terms.*

1.5) Total equity value and enterprise value (if explicitly stated or calculable)
*Search guidance: Look in recitals, press releases, or calculate based on per-share value and total shares outstanding. Include your calculation methodology.*

## 2. ELECTION MECHANICS

2.1) Cash vs. mixed consideration options
*Search guidance: Look for sections that describe shareholder ability to elect different forms of consideration (cash, stock, or mix).*

2.2) Proration mechanisms and limitations
*Search guidance: Find provisions explaining how elections will be adjusted if too many shareholders select one option.*

2.3) Treatment of different share classes
*Search guidance: Look for specific provisions addressing different classes of shares (common, preferred, non-voting, etc.).*

2.4) Election deadlines and default treatments
*Search guidance: Identify when shareholders must make elections and what happens if they fail to elect.*

## 3. KEY TIMELINE

3.1) Signing date
*Search guidance: Usually found in the preamble or introduction of the agreement.*

3.2) Expected closing timeline
*Search guidance: Look for language describing when parties expect the deal to close, often subject to conditions. Include any public guidance on closing timing.*

3.3) HSR filing and waiting period
*Search guidance: Check sections on regulatory approvals for specifics about antitrust filing timelines. Calculate specific deadline dates.*

3.4) Window to accept a superior proposal
*Search guidance: Look in no-shop/go-shop sections. Note current status (active/expired) and any fee reductions during this period.*

3.5) Outside date/termination date
*Search guidance: Find the date after which either party can terminate if closing hasn't occurred. Often in termination provisions. Calculate all extension dates.*

3.6) Inside Date
*Search guidance: Check for any provision specifying earliest date when closing can occur.*

3.7) Extension provisions
*Search guidance: Look for circumstances allowing extension of termination date.*

3.8) Tender offer timing
*Search guidance: For two-step transactions, find provisions specifying when tender offer must begin and end.*

3.9) Minimum tender conditions
*Search guidance: For tender offers, identify minimum percentage of shares that must be tendered.*

## 4. SPECIFIC APPROVALS REQUIRED

4.1) International antitrust approvals required
*Search guidance: Look for mention of non-US competition authorities whose approval is needed.*

4.2) CFIUS or other national security reviews
*Search guidance: Check for required US or other national security reviews.*

4.3) Industry-specific regulatory approvals
*Search guidance: Find any sector-specific regulators who must approve.*

4.4) Expected regulatory challenges
*Search guidance: Look for provisions suggesting anticipated regulatory issues, efforts standards, or remedy limitations.*

## 5. SHAREHOLDER APPROVAL MECHANISMS

5.1) Voting requirements
*Search guidance: Find provisions specifying percentage of shares needed to approve the transaction.*

5.2) Written consent voting provisions
*Search guidance: Look for ability to obtain approval through written consent rather than meeting.*

5.3) Circumstances the written consent can be negated
*Search guidance: Find conditions under which written consents might be invalidated.*

5.4) Support agreements with major shareholders
*Search guidance: Check for references to separate agreements with large shareholders.*

5.5) Parties, percentage of shares outstanding AND voting power subject to voting agreement
*Search guidance: Distinguish between ownership percentage and voting power percentage.*

## 6. TERMINATION RIGHTS & BREAK FEES

6.1) Termination scenarios, triggering events
*Search guidance: Find section on termination rights listing all circumstances allowing parties to terminate.*

6.2) Termination fee amounts for Company
*Search guidance: Identify exact dollar amount AND calculate percentage of transaction value.*

6.3) Termination fee amounts for parent/acquirer
*Search guidance: Find exact reverse break fee AND calculate percentage of transaction value.*

6.4) Specific performance remedies
*Search guidance: Look for provisions allowing parties to seek court-ordered specific performance. Availability of debt financing / funding should be considered "important information" and placed in bold.*

## 7. MATERIAL ADVERSE EFFECT PROVISIONS

7.1) MAE definition
*Search guidance: Find the definition, noting if it's single-prong or includes "ability to perform" language.*

7.2) All MAE carve-out clauses
*Search guidance: Extract all exceptions, including:*

7.2.1) Economic/market condition exceptions
7.2.2) Industry-specific exceptions
7.2.3) Geopolitical/trade war carve-outs
7.2.4) Pandemic-related provisions
7.2.5) Tariffs
7.2.6) Any carve-outs topical to current macro environment
7.2.7) Disproportionate effect qualifiers
7.2.8) Absolute carve-outs (e.g., announcement/pendency)

## 8. FINANCING & DEAL CONDITIONS

8.1) Financing commitments
*Search guidance: Find provisions describing buyer's financing arrangements.*

8.2) Financing conditions
*Search guidance: Look for any conditions to the financing commitments.*

8.3) Marketing period definition
*Search guidance: Find definition of period during which buyer can market debt financing.*

8.4) Marketing period duration
*Search guidance: Identify exact length of marketing period.*

8.5) Conditions precedent to closing
*Search guidance: Find all conditions that must be satisfied before closing.*

8.6) Additional details on debt and equity financing
*Search guidance: Incremental detail on debt and equity financing amounts, sources, and terms. Likely found in 8-K.*

## 9. DEAL PROTECTION MECHANISMS

9.1) Go-shop provisions with timeline
*Search guidance: Find provisions allowing target to actively seek competing offers. Note if period has expired.*

9.2) No-shop provisions with timeline
*Search guidance: Look for restrictions on target soliciting competing offers.*

9.3) Fiduciary out clauses, mechanics
*Search guidance: Find exceptions to no-shop. Note any restrictions on when board can change recommendation.*

9.4) Matching rights, procedures
*Search guidance: Check for buyer's right to match competing offers. Note if unlimited.*

9.5) Force-the-vote provisions
*Search guidance: Look for provisions requiring shareholder vote even if board changes recommendation.*

## 10. REGULATORY EFFORTS STANDARDS

10.1) Efforts standard for obtaining approvals
*Search guidance: Extract exact language on efforts required (reasonable best efforts, etc.).*

10.2) Burdensome Condition/materiality limitations
*Search guidance: Find specific limitations on required divestitures or remedies.*

10.3) Clear skies provisions
*Search guidance: Look for restrictions on buyer making other acquisitions during pendency.*

10.4) Litigation obligations
*Search guidance: Check if parties must litigate to defend deal.*

## 11. BOND/DEBT & MATERIAL CONTRACT PROVISIONS

11.1) Bond redemption terms and notice requirements
11.2) Change of control provisions
11.3) Debt exchange offers
11.4) Debt consent solicitations

11.5) Material customer/supplier/licensing contracts with change-of-control provisions
*Search guidance: Only pursue this where the target's standalone value depends materially on one or a
few commercial relationships (a key customer, licensor, or long-term supply partner) — not every
deal has one worth chasing. Check the merger agreement's Material Contracts representation and
disclosure schedule index for any such contract, and separately check the target's recent 8-K
filings for a standalone customer/supplier/collaboration agreement (a master services agreement, a
long-term supply agreement, a licensing or commercialization agreement) filed as a material
contract. Quote the actual change-of-control/assignment clause verbatim from the contract itself —
do not infer its terms from a press release, a sell-side note, or either party's informal
characterization of what happens to the relationship post-close.*

11.6) What the change-of-control clause actually requires
*Search guidance: State plainly whether the clause requires the counterparty's consent to assign the
contract, gives the counterparty a unilateral termination or license-out right, or is silent (the
contract simply survives, assignable without consent). This is what determines whether the
acquirer's ability to retain the relationship post-close is contractually assured or merely
contingent on the counterparty's cooperation — a real value-continuity/completion-risk fact, cited to
the specific contract section, not folded into the Material Adverse Effect discussion in Section 7.
Mark `NA — Not applicable` if the target's value doesn't concentrate on a single relationship, or `NA
— Not found` if a genuine search turned up no such contract.*

## 12. CONFIDENTIALITY AND CLEAN TEAM AGREEMENTS

12.1) Confidentiality agreement date
12.2) Standstill provisions
12.3) Clean team agreements and protocols

## 13. TAX TREATMENT & DIVIDEND POLICY

13.1) Tax treatment of consideration
13.2) Interim dividend allowances

## 14. ORDINARY COURSE CONDUCT

14.1) Target company operating covenants
*Search guidance: Extract detailed provisions and note specific consent requirements.*

14.2) Parent company operating covenants
*Search guidance: Extract detailed provisions and note specific consent requirements.*

---

## Output format

For each section, provide:

- **Section Reference**: Section X.X, Page Y
- **Verbatim Text**: "[Exact quote from agreement with **key responsive portions in bold**]"

Use markdown formatting:
- Bold for key terms and answers
- Italics for emphasis
- Code blocks for calculations
- Blockquotes for lengthy legal text
