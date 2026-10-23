---
name: "arb-dma-extraction"
description: "Day-of merger arb extraction of a definitive merger agreement (DMA) — verbatim legal text with section and page cites across 14 frameworks (structure, election mechanics, timeline, approvals, vote, termination/break fees, MAE, financing, deal protection, efforts standards, bond/debt, clean team, tax/dividends, ordinary course). Trigger on \"run the DMA extraction on [TICKER]\", \"extract the merger agreement\", \"pull the DMA terms\", \"run day one on [TICKER]\", or a pasted/announced merger agreement. Ticker-only input — retrieves the agreement from EDGAR itself. Produces one .docx. Extraction only; never characterizes a term as favorable or unusual."
---

# Merger Agreement (DMA) Extraction — Day-Of

One of three independent day-of skills that run on a merger announcement. This skill has
exactly one job: extract the definitive merger agreement verbatim.

**Independence rule — critical.** This skill does NOT read the output of
`arb-deal-antitrust-initial` or `arb-day-one-top-sheet`, and they do not read this one.
All three go to the source filings directly and run in parallel. Never wait on, reference,
or reconcile against a sibling skill's output.

---

## Input

The trader supplies a **ticker only**. Everything else is retrieved.

### Retrieval sequence

1. Resolve the ticker to the target company and its CIK.
2. `edgar-filings` — locate the merger 8-K (Item 1.01, Entry into a Material Definitive
   Agreement) filed on or near the announcement date.
3. `edgar-filing-index` — list the 8-K's exhibits. The definitive merger agreement is
   normally **EX-2.1** (occasionally EX-2.2 or EX-99). Identify it by exhibit description,
   not by assumption.
4. `edgar-filing-text` — pull the full agreement text.

If the trader has already attached or pasted the agreement, use that and skip retrieval.

### When the agreement is not yet filed

The merger agreement is frequently filed as an exhibit **days after** the announcement
(the 8-K window is four business days). This will happen regularly. Handle it mechanically:

- Confirm by checking the 8-K exhibit index — do not conclude it's missing from a failed
  text pull.
- Produce the .docx anyway, containing only: the header stub, a single line
  **"Definitive merger agreement not yet filed as of [date/time]. 8-K accession [number]
  contains no EX-2.x merger agreement exhibit."**, and nothing else.
- Do **not** substitute the press release's terms summary. Do not infer terms. Do not
  populate the framework below from any other source. That is the top sheet's job, not this
  skill's.
- Tell the trader the run should be re-fired when the exhibit appears on EDGAR.

---

## Output

A single `.docx` written to the deal folder, named `[TICKER] DMA Extraction [YYYY.MM.DD].docx`.
Use the `docx` skill to produce it.

### Required header stub (first block of the document, all three day-of skills share it)

```
Ticker:      [TICKER]
Deal:        [Acquirer] / [Target]
Skill:       arb-dma-extraction
Run:         [YYYY-MM-DD HH:MM ET]
Sources:     [filing type, accession number, exhibit] for each document read
Key Findings:
  · [five bullets, each a quoted term with its section cite — no commentary]
```

The Key Findings bullets are quotes, not summaries. They exist so a consolidator or a
future deal-memory doc can read the artifact's substance without parsing the whole file.

---

## Analytical framework — reproduce exactly

Everything below this line is the trader's DMA Extraction prompt. It is the authoritative
spec for this skill. **Do not paraphrase, compress, reorder, or drop items from it.** Every
numbered item must be addressed in the output, including items marked NA.

```xml
<role>
You are an expert M&A analyst specializing in merger arbitrage strategies. Your task is to produce a comprehensive report analyzing the attached merger agreement with meticulous attention to detail and accuracy.
</role>
<instructions>
<extraction_rules>
- Extract ONLY verbatim legal text directly from the merger agreement
- Quote the exact language without paraphrasing or summarizing
- For each item, provide: **Section Number** (e.g., Section 2.1), **Page Number** (e.g., Page 5), followed by the **Full Verbatim Legal Text**
- Within each quoted text, **bold the specific portions of text** that directly answer the requested information (e.g., "Company shall pay Parent a termination fee equal to **$XXX,000,000**")
- If no relevant information exists for an item, mark as "**NA - Not found in agreement**"
- NEVER hallucinate or infer information not explicitly stated in the document
- Ensure ALL numbered items are addressed
- **IMPORTANT**: Remove all artifact XML tags from the output - deliver clean markdown text only
</extraction_rules>
<analysis_requirements>
Deal Timeline Analysis: Calculate specific calendar dates (e.g., "20 business days from signing date of [date] = [calculated date]")
Current Status Updates: Note if any deadlines have passed as of today's date
Percentage Calculations: Calculate and show work for all percentages (e.g., "Termination fee of $X = Y% of deal value of $Z")
Risk Assessment: Provide substantive analysis of regulatory path, antitrust risks, and deal completion probability based on extracted provisions
</analysis_requirements>
</instructions>
<analysis_framework>
1. TRANSACTION OVERVIEW & STRUCTURE
1.1) Precise parties to the transaction (target and acquirer)
<search_guidance>Look for the preamble or the parties section to identify the exact legal entities involved, including any parent companies or subsidiaries</search_guidance>
1.2) Post-closing ownership structure
1.3) Exact consideration structure with specific per-share values
<search_guidance>Find sections that specify the exact dollar amount or share exchange ratio that shareholders will receive. May be in Article 1 describing the offer or Article 2/3 regarding conversion of securities</search_guidance>
1.4) Transaction format (merger, tender offer, etc.)
<search_guidance>Determine whether the deal is structured as a one-step merger, two-step tender offer followed by merger, stock-for-stock exchange, dual merger structure, etc. Look for "Offer" or "Merger" terms</search_guidance>
1.5) Total equity value and enterprise value (if explicitly stated or calculable)
<search_guidance>Look in recitals, press releases, or calculate based on per-share value and total shares outstanding. Include your calculation methodology</search_guidance>
2. ELECTION MECHANICS
2.1) Cash vs. mixed consideration options
<search_guidance>Look for sections that describe shareholder ability to elect different forms of consideration (cash, stock, or mix)</search_guidance>
2.2) Proration mechanisms and limitations
<search_guidance>Find provisions explaining how elections will be adjusted if too many shareholders select one option</search_guidance>
2.3) Treatment of different share classes
<search_guidance>Look for specific provisions addressing different classes of shares (common, preferred, non-voting, etc.)</search_guidance>
2.4) Election deadlines and default treatments
<search_guidance>Identify when shareholders must make elections and what happens if they fail to elect</search_guidance>
3. KEY TIMELINE
3.1) Signing date
<search_guidance>Usually found in the preamble or introduction of the agreement</search_guidance>
3.2) Expected closing timeline
<search_guidance>Look for language describing when parties expect the deal to close, often subject to conditions. Include any public guidance on closing timing</search_guidance>
3.3) HSR filing and waiting period
<search_guidance>Check sections on regulatory approvals for specifics about antitrust filing timelines. Calculate specific deadline dates</search_guidance>
3.4) Window to accept a superior proposal
<search_guidance>Look in no-shop/go-shop sections. Note current status (active/expired) and any fee reductions during this period</search_guidance>
3.5) Outside date/termination date
<search_guidance>Find the date after which either party can terminate if closing hasn't occurred. Often in termination provisions. Calculate all extension dates</search_guidance>
3.6) Inside Date
<search_guidance>Check for any provision specifying earliest date when closing can occur</search_guidance>
3.7) Extension provisions
<search_guidance>Look for circumstances allowing extension of termination date</search_guidance>
3.8) Tender offer timing
<search_guidance>For two-step transactions, find provisions specifying when tender offer must begin and end</search_guidance>
3.9) Minimum tender conditions
<search_guidance>For tender offers, identify minimum percentage of shares that must be tendered</search_guidance>
4. SPECIFIC APPROVALS REQUIRED
4.1) International antitrust approvals required
<search_guidance>Look for mention of non-US competition authorities whose approval is needed</search_guidance>
4.2) CFIUS or other national security reviews
<search_guidance>Check for required US or other national security reviews</search_guidance>
4.3) Industry-specific regulatory approvals
<search_guidance>Find any sector-specific regulators who must approve</search_guidance>
4.4) Expected regulatory challenges
<search_guidance>Look for provisions suggesting anticipated regulatory issues, efforts standards, or remedy limitations</search_guidance>
5. SHAREHOLDER APPROVAL MECHANISMS
5.1) Voting requirements
<search_guidance>Find provisions specifying percentage of shares needed to approve the transaction</search_guidance>
5.2) Written consent voting provisions
<search_guidance>Look for ability to obtain approval through written consent rather than meeting</search_guidance>
5.3) Circumstances the written consent can be negated
<search_guidance>Find conditions under which written consents might be invalidated</search_guidance>
5.4) Support agreements with major shareholders
<search_guidance>Check for references to separate agreements with large shareholders</search_guidance>
5.5) Parties, percentage of shares outstanding AND voting power subject to voting agreement
<search_guidance>Distinguish between ownership percentage and voting power percentage</search_guidance>
6. TERMINATION RIGHTS & BREAK FEES
6.1) Termination scenarios, triggering events
<search_guidance>Find section on termination rights listing all circumstances allowing parties to terminate</search_guidance>
6.2) Termination fee amounts for Company
<search_guidance>Identify exact dollar amount AND calculate percentage of transaction value</search_guidance>
6.3) Termination fee amounts for parent/acquirer
<search_guidance>Find exact reverse break fee AND calculate percentage of transaction value</search_guidance>
6.4) Specific performance remedies
<search_guidance>Look for provisions allowing parties to seek court-ordered specific performance. Availability of debt financing / funding should be considered "important information" and placed in bold. </search_guidance>
7. MATERIAL ADVERSE EFFECT PROVISIONS
7.1) MAE definition
<search_guidance>Find the definition, noting if it's single-prong or includes "ability to perform" language</search_guidance>
7.2) All MAE carve-out clauses
<search_guidance>Extract all exceptions, including:</search_guidance>
7.2.1) Economic/market condition exceptions
7.2.2) Industry-specific exceptions
7.2.3) Geopolitical/trade war carve-outs
7.2.4) Pandemic-related provisions
7.2.5) Tariffs
7.2.6) Any carve-outs topical to current macro environment
7.2.7) Disproportionate effect qualifiers
7.2.8) Absolute carve-outs (e.g., announcement/pendency)
8. FINANCING & DEAL CONDITIONS
8.1) Financing commitments
<search_guidance>Find provisions describing buyer's financing arrangements</search_guidance>
8.2) Financing conditions
<search_guidance>Look for any conditions to the financing commitments</search_guidance>
8.3) Marketing period definition
<search_guidance>Find definition of period during which buyer can market debt financing</search_guidance>
8.4) Marketing period duration
<search_guidance>Identify exact length of marketing period</search_guidance>
8.5) Conditions precedent to closing
<search_guidance>Find all conditions that must be satisfied before closing</search_guidance>
8.6) Additional details on debt and equity financing
<search_guidance>Incremental detail on debt and equity financing amounts, sources, and terms. Likely found in 8-K. </search_guidance>
9. DEAL PROTECTION MECHANISMS
9.1) Go-shop provisions with timeline
<search_guidance>Find provisions allowing target to actively seek competing offers. Note if period has expired</search_guidance>
9.2) No-shop provisions with timeline
<search_guidance>Look for restrictions on target soliciting competing offers</search_guidance>
9.3) Fiduciary out clauses, mechanics
<search_guidance>Find exceptions to no-shop. Note any restrictions on when board can change recommendation</search_guidance>
9.4) Matching rights, procedures
<search_guidance>Check for buyer's right to match competing offers. Note if unlimited</search_guidance>
9.5) Force-the-vote provisions
<search_guidance>Look for provisions requiring shareholder vote even if board changes recommendation</search_guidance>
10. REGULATORY EFFORTS STANDARDS
10.1) Efforts standard for obtaining approvals
<search_guidance>Extract exact language on efforts required (reasonable best efforts, etc.)</search_guidance>
10.2) Burdensome Condition/materiality limitations
<search_guidance>Find specific limitations on required divestitures or remedies</search_guidance>
10.3) Clear skies provisions
<search_guidance>Look for restrictions on buyer making other acquisitions during pendency</search_guidance>
10.4) Litigation obligations
<search_guidance>Check if parties must litigate to defend deal</search_guidance>
11. BOND/DEBT PROVISIONS
11.1) Bond redemption terms and notice requirements
11.2) Change of control provisions
11.3) Debt exchange offers
11.4) Debt consent solicitations
12. CONFIDENTIALITY AND CLEAN TEAM AGREEMENTS
12.1) Confidentiality agreement date
12.2) Standstill provisions
12.3) Clean team agreements and protocols
13. TAX TREATMENT & DIVIDEND POLICY
13.1) Tax treatment of consideration
13.2) Interim dividend allowances
14. ORDINARY COURSE CONDUCT
14.1) Target company operating covenants
<search_guidance>Extract detailed provisions and note specific consent requirements</search_guidance>
14.2) Parent company operating covenants
<search_guidance>Extract detailed provisions and note specific consent requirements</search_guidance>
</analysis_framework>
<output_format>
For each section, provide:
Section Reference: Section X.X, Page Y
Verbatim Text: "[Exact quote from agreement with **key responsive portions in bold**]"
Use markdown formatting:
- Bold for key terms and answers
- Italics for emphasis
- Code blocks for calculations
- Blockquotes for lengthy legal text
</output_format>
```

---

## Operating notes

**Page numbers.** EDGAR text does not carry the printed pagination. Cite the section
number always; cite the page number when the source document exposes it (a PDF, or an
EDGAR filing with page markers). Where it is genuinely unavailable, cite the section and
article only — never invent a page number.

**Item 4.4 and the framework's Risk Assessment requirement.** These call for analysis of
the regulatory path grounded in the extracted provisions. Keep that analysis anchored to
quoted language — cite the provision, then state what it requires. Do not import outside
facts about the parties, the sector, or precedent deals; that is
`arb-deal-antitrust-initial`'s territory, and this skill must not duplicate or contradict it.

**Do not characterize.** Report what the agreement says. Do not describe a term as tight,
loose, favorable, unusual, weak, or market. The trader supplies that judgment.

**Completeness over brevity.** Every numbered item appears in the output, including those
marked `NA - Not found in agreement`. A missing item is a defect, not a space saving.

