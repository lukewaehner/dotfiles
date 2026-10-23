---
name: "arb-deal-antitrust-initial"
description: "Day-of merger arb antitrust and overlap screen on a newly announced deal — acquirer portfolio/overlap mapping, market definition and concentration, competitive effects, target capital structure and leverage, litigation and fraud risk, valuation and precedents, stakeholder analysis, all EDGAR-cited. Trigger on \"run the initial deal and antitrust screen on [TICKER]\", \"run the antitrust screen\", \"overlap screen on [TICKER]\", \"run day one on [TICKER]\", or a newly announced merger. Ticker-only input — pulls the 8-K, press release, and EDGAR filings itself. Produces one .docx. Never estimates market shares, HHI, or probabilities without sourced data."
---

# Initial Deal & Antitrust Screen — Day-Of

One of three independent day-of skills that run on a merger announcement. This skill has
exactly one job: the overlap, market-structure, and deal-risk screen off the announcement
and EDGAR.

**Independence rule — critical.** This skill does NOT read the output of
`arb-dma-extraction` or `arb-day-one-top-sheet`, and they do not read this one. All three
go to the source filings directly and run in parallel. Never wait on, reference, or
reconcile against a sibling skill's output.

**Boundary with `arb-dma-extraction`.** That skill owns every merger-agreement term
verbatim. This skill's "Deal Structure and Terms Analysis" section reads terms from the
8-K and press release for context and does not attempt a clause-level extraction of the
agreement. This skill's territory is the market, the portfolio, the competitors, the
target's financial condition, and the litigation picture.

---

## Input

The trader supplies a **ticker only**. Everything else is retrieved.

### Retrieval sequence

1. Resolve the ticker to the target company and CIK. Identify the acquirer and classify it:
   **PE sponsor / strategic / hybrid-consortium.** The portfolio-context sections below are
   built for sponsors; for a strategic acquirer, apply the same overlap logic to the
   acquirer's own business segments and disclosed competitors.
2. `edgar-filings` → the merger 8-K and its press release exhibit (EX-99.1).
3. `extract-8k` where available for a fast structured read of the announcement.
4. Target's latest **10-K and 10-Q** — Competition section, segment reporting (product,
   geographic, customer type), MD&A, legal proceedings, capital structure and debt notes.
5. Acquirer's EDGAR filings where it is a public filer; for a sponsor, its portfolio
   companies' filings.
6. `semantic-search` against the **ArbJournal / Chain Bridge Research** vector index for
   precedent transactions with comparable structure, sector, and regulatory posture. Cite
   from hit metadata — institution, author, date.

Run retrieval concurrently where possible; the clock matters.

### Missing-data rule

The framework below is explicit and it governs: where market size, share, or concentration
data is not available from a reliable source, **state the limitation explicitly**. Never
estimate, never back into a number, never produce an HHI or a probability percentage
without sourced inputs.

---

## Output

A single `.docx` written to the deal folder, named
`[TICKER] Initial Deal & Antitrust [YYYY.MM.DD].docx`. Use the `docx` skill.

### Required header stub (first block of the document, all three day-of skills share it)

```
Ticker:      [TICKER]
Deal:        [Acquirer] / [Target]
Skill:       arb-deal-antitrust-initial
Run:         [YYYY-MM-DD HH:MM ET]
Sources:     [filing type, accession number] for each EDGAR document read;
             [institution, author, date] for each ArbJournal hit
Key Findings:
  · [five bullets — each a sourced fact with its citation, no commentary]
```

Findings are sourced facts, not conclusions.

---

## Analytical framework — reproduce exactly

Everything below this line is the trader's Initial Deal & Antitrust prompt. It is the
authoritative spec for this skill. **Do not paraphrase, compress, reorder, or drop items
from it.** Every section, deliverable, checklist step, and verification standard applies.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<antitrust_risk_assessment_guide>
  <general_instructions>
    <perspective>Conduct analysis from the perspective of a prospective deal risk analyst evaluating transaction completion probability. Do not provide strategic recommendations for parties involved in the transaction, and do not focus on where the target stock is trading relative to deal consideration.</perspective>
    <critical_requirements>
      <requirement>All facts and figures must be cited with specific sources</requirement>
      <requirement>Never estimate, calculate, or hallucinate market shares, HHI calculations, or probability percentages without explicit source data</requirement>
      <requirement>If market size or concentration data is unavailable, explicitly state this limitation rather than making estimates</requirement>
      <requirement>Distinguish clearly between sourced facts and analytical opinions</requirement>
      <requirement>Competitor disclosures and geographic revenue breakdowns are required outputs, sourced directly from EDGAR filings (10-K, 10-Q, 8-K, merger filings)</requirement>
    </critical_requirements>
  </general_instructions>
  <portfolio_context_analysis>
    <section title="Critical Portfolio Company Due Diligence">
      <requirements>
        <requirement>Comprehensive listing of acquirer's portfolio (majority and minority stakes) to identify horizontal and adjacent overlaps</requirement>
        <requirement>Historical portfolio investigation including past exits to assess consolidation patterns</requirement>
        <requirement>Analysis of direct, adjacent, complementary, and potential future competitors</requirement>
        <requirement>Verification using acquirer website, EDGAR, specialized PE databases, and reputable news sources</requirement>
      </requirements>
    </section>
    <section title="PE-Specific Competitive Effects Framework">
      <deliverables>
        <deliverable>Portfolio Company Overlap Table aligning portfolio companies against target product/service lines</deliverable>
        <deliverable>Revenue segmentation comparison by product, geography, and customer type</deliverable>
        <deliverable>Geographic revenue breakdowns for target and overlapping portfolio companies from EDGAR</deliverable>
        <deliverable>Analysis of high-concentration regions and geographic expansion trends</deliverable>
        <deliverable>Vertical integration assessment for upstream/downstream relationships</deliverable>
        <deliverable>Review of whether acquisition represents part of a roll-up strategy</deliverable>
      </deliverables>
    </section>
    <section title="Enhanced Competitive Effects Evaluation">
      <considerations>
        <consideration>Platform vs. add-on characterization</consideration>
        <consideration>Customer overlap and potential cross-selling or bundling</consideration>
        <consideration>Data advantage risks from combined portfolio</consideration>
        <consideration>Innovation impact from combined R&D capabilities</consideration>
      </considerations>
    </section>
    <section title="Regulatory History Examination">
      <requirements>
        <requirement>Review prior antitrust reviews of the PE sponsor in related sectors</requirement>
        <requirement>Summarize remedies/divestitures previously required</requirement>
      </requirements>
    </section>
    <section title="Geographic Revenue Analysis Requirements">
      <mandatory_items>
        <item>Market-by-market assessment for each overlapping product/service line</item>
        <item>Target geographic revenue breakdown with EDGAR citation</item>
        <item>Portfolio companies' geographic revenue breakdown using same categories</item>
        <item>Combined entity's position by geography (text and table only)</item>
        <item>Geographic concentration flags where overlaps exceed screening thresholds</item>
        <item>Year-over-year geographic expansion trends</item>
      </mandatory_items>
    </section>
    <section title="Portfolio Company Competitor Documentation">
      <requirements>
        <requirement>Extract and cite competitors listed in each relevant portfolio company's latest 10-K/10-Q</requirement>
        <requirement>Cross-reference competitor lists across portfolio companies and target</requirement>
        <requirement>Identify common competitors</requirement>
        <requirement>Analyze likely responses from non-portfolio competitors</requirement>
      </requirements>
    </section>
    <section title="Probability Modeling with Portfolio Considerations">
      <constraints>
        <constraint>Base assessments solely on historical precedent of similar PE transactions with overlaps</constraint>
        <constraint>Include remedy likelihood qualitatively where overlaps exist</constraint>
        <constraint>Identify potential divestiture candidates in text or table form</constraint>
      </constraints>
    </section>
    <section title="Enhanced Documentation Requirements">
      <requirements>
        <requirement>Include relevant sections from portfolio companies' latest EDGAR filings</requirement>
        <requirement>Extract geographic segment tables verbatim with citations</requirement>
        <requirement>Provide verbatim competitor listings from EDGAR Competition sections</requirement>
        <requirement>Summarize PE investment thesis and how target fits within portfolio</requirement>
      </requirements>
    </section>
  </portfolio_context_analysis>
  <analysis_framework>
    <section title="Deal Structure and Terms Analysis">
      <required_elements>
        <element>Purchase price, premium calculation, and analyst comparison</element>
        <element>Deal structure and consideration details</element>
        <element>Financing structure including debt/equity amounts</element>
        <element>Sponsor background and ownership structure</element>
        <element>Dividend/distribution policy during pendency</element>
        <element>Termination fees and downside protections</element>
        <element>Expected closing timeline and milestones</element>
        <element>Material adverse change provisions</element>
      </required_elements>
    </section>
    <section title="Target Financial Analysis">
      <required_elements>
        <element>Capital structure overview including total debt, equity, and key debt instruments with EDGAR citations</element>
        <element>Leverage metrics (Net Debt/EBITDA, Debt/Equity, interest coverage) sourced from EDGAR filings</element>
        <element>Recent financing activity including equity offerings, debt issuances, and credit facility amendments</element>
        <element>Free cash flow profile including operating cash flow, capital expenditures, and unlevered free cash flow trends</element>
        <element>Liquidity position including cash on hand, revolver availability, and near-term debt maturities</element>
        <element>Covenant compliance disclosures and any waiver or amendment history from EDGAR filings</element>
        <element>Potential solvency concerns including going concern disclosures, audit qualifications, or financial distress indicators</element>
        <element>Dividend and share repurchase history and sustainability relative to free cash flow generation</element>
      </required_elements>
    </section>
    <section title="Valuation and Precedent Analysis">
      <required_elements>
        <element>Key valuation multiples (EV/Revenue, EV/EBITDA, P/E)</element>
        <element>Comparison to precedent transactions with multiples cited</element>
        <element>Peer group trading multiples</element>
        <element>Assessment relative to recent M&A activity</element>
        <element>Premium analysis versus historical averages</element>
        <element>Synergy expectations and disclosed targets</element>
      </required_elements>
    </section>
    <section title="Strategic Stakeholder Analysis">
      <required_elements>
        <element>Existing strategic investors and rights</element>
        <element>Board composition and approval processes</element>
        <element>Shareholder approval requirements</element>
        <element>Management retention and change-in-control terms</element>
        <element>Key customer/supplier/partner relationships</element>
        <element>Activist or significant shareholders with objections</element>
        <element>Potential competing bidders</element>
      </required_elements>
    </section>
    <section title="Litigation and Fraud Risk Analysis">
      <required_elements>
        <element>Overview of active material litigation involving the target and bidder sourced from EDGAR disclosures (10-K, 10-Q, 8-K legal proceedings sections)</element>
        <element>Historical litigation profile including past settlements, judgments, and financial impact with EDGAR citations</element>
        <element>Regulatory investigations or government enforcement actions disclosed in filings</element>
        <element>Any disclosed fraud allegations, financial restatements, or internal investigation disclosures</element>
        <element>Review of publicly available short-seller reports or public fraud allegations targeting either the target or the bidder</element>
        <element>Estimated financial exposure from pending litigation as disclosed in EDGAR filings</element>
        <element>Deal-specific litigation risks including merger objection lawsuits, fiduciary duty claims, and appraisal rights actions</element>
        <element>Assessment of material litigation or fraud allegations as a potential deal-closing impediment or MAC trigger</element>
      </required_elements>
    </section>
    <section title="Market Definition and Concentration Analysis">
      <steps>
        <step>Define relevant product and geographic markets</step>
        <step>Provide geographic and segment revenue breakdowns from EDGAR</step>
        <step>Apply hypothetical monopolist test</step>
        <step>Only quantify market shares and HHI with reliable data</step>
        <step>If data unavailable, state limitation explicitly</step>
        <step>Identify and analyze significant competitors</step>
        <step>Extract competitors from EDGAR Competition sections</step>
        <step>Assess adjacent markets and substitutes</step>
        <step>Evaluate barriers to entry</step>
      </steps>
    </section>
    <section title="Competitive Effects Analysis">
      <subsections>
        <subsection>Horizontal Overlap Assessment</subsection>
        <subsection>Vertical Relationship Assessment</subsection>
        <subsection>Potential Competition Assessment</subsection>
        <subsection>Conglomerate Effects</subsection>
        <subsection>Innovation and Dynamic Competition Concerns</subsection>
        <subsection>Buyer/Supplier Power and Monopsony Effects</subsection>
        <subsection>Portfolio Context Integration (platform vs. add-on, cross-selling, data advantages, innovation impacts)</subsection>
      </subsections>
    </section>
    <section title="Evidence Collection and Documentation">
      <required_sources>
        <source>10-K and 10-Q MD&A (EDGAR)</source>
        <source>Segment reporting by product, geography, and customer type (EDGAR)</source>
        <source>Competition sections of 10-Ks and 10-Qs (EDGAR)</source>
        <source>Merger agreements, proxy statements, S-4/F-4, and 8-Ks (EDGAR)</source>
        <source>Industry analyst reports and trade publications</source>
        <source>FTC/DOJ precedent cases and enforcement actions</source>
        <source>Trade association data and industry studies</source>
        <source>Customer and supplier contract disclosures</source>
        <source>Patent filings and R&D disclosures</source>
        <source>PE sponsor and portfolio company disclosures verified against EDGAR</source>
      </required_sources>
    </section>
  </analysis_framework>
  <implementation_checklist>
    <required_portfolio_steps>
      <step>List all PE acquirer portfolio companies</step>
      <step>Flag overlaps with target</step>
      <step>Extract geographic revenue breakdowns from EDGAR</step>
      <step>Compare product/service offerings in table form</step>
      <step>Document all competitors from filings with citations</step>
      <step>Analyze historical acquisition patterns</step>
      <step>Evaluate roll-up or platform strategy</step>
      <step>Assess cross-selling and data combination risks</step>
      <step>Review previous antitrust reviews</step>
    </required_portfolio_steps>
    <geographic_revenue_documentation>
      <step>Standardize geographic categories across companies</step>
      <step>Extract revenue percentages by region from filings</step>
      <step>Compare combined geographic presence in tables</step>
      <step>Document expansion trends</step>
      <step>Analyze regional regulatory considerations</step>
    </geographic_revenue_documentation>
    <financial_analysis_documentation>
      <step>Extract capital structure and leverage metrics from most recent EDGAR filings</step>
      <step>Document near-term debt maturities and liquidity position</step>
      <step>Identify any going concern disclosures, covenant waivers, or distress indicators</step>
      <step>Summarize recent financing activity and free cash flow trends</step>
    </financial_analysis_documentation>
    <litigation_and_fraud_documentation>
      <step>Extract legal proceedings disclosures from target and bidder EDGAR filings</step>
      <step>Search for publicly available short-seller reports or fraud allegations on either party</step>
      <step>Document estimated financial exposure from pending litigation with citations</step>
      <step>Assess deal-specific litigation risks including merger objection suits and appraisal actions</step>
    </litigation_and_fraud_documentation>
    <documentation_format_requirements>
      <requirement>Present all findings in text and tables only</requirement>
      <requirement>Include a dedicated "Portfolio Company Analysis" section</requirement>
      <requirement>Provide comparative tables for geographic revenue</requirement>
      <requirement>Document competitor lists with exact citations</requirement>
    </documentation_format_requirements>
  </implementation_checklist>
  <fact_verification_requirements>
    <market_data_standards>
      <standard type="market_size_figures">Must cite specific industry reports, government data, or trade association studies</standard>
      <standard type="market_share_calculations">Only if both revenue and total market size are from reliable sources</standard>
      <standard type="hhi_calculations">Only if sufficient market participant data is available</standard>
      <standard type="probability_estimates">Only if based on historical precedent data from similar transactions</standard>
      <standard type="valuation_multiples">Cite precedent transactions, filings, or analyst reports</standard>
      <standard type="competitor_lists">Required verbatim from EDGAR filings</standard>
      <standard type="geographic_revenue">Required verbatim from EDGAR segment tables</standard>
      <standard type="portfolio_mapping">Portfolio verified via EDGAR and sponsor disclosures; minority stakes noted</standard>
      <standard type="leverage_and_financial_metrics">Sourced from most recent EDGAR filings (10-K, 10-Q); do not estimate</standard>
      <standard type="litigation_exposure">Sourced from EDGAR legal proceedings disclosures; publicly available short reports cited by source and date</standard>
    </market_data_standards>
  </fact_verification_requirements>
</antitrust_risk_assessment_guide>
```

---

## Operating notes

**Buyer type drives the portfolio sections.** The `portfolio_context_analysis` block is
written for a PE sponsor. For a **strategic** acquirer, apply the identical logic to the
acquirer's own reported segments, product lines, geographic revenue, and 10-K Competition
disclosures — the overlap question is the same, the source is the acquirer's own filings
rather than a portfolio roster. For a **consortium**, run it for each member.

**Sourced facts vs. analytical opinion must be visibly separated**, per the framework's
critical requirements. Where the framework calls for assessment (competitive effects,
remedy likelihood, litigation as a MAC trigger), label it as analysis and ground it in the
cited facts above it. Do not let opinion migrate into the factual sections.

**Do not discuss the spread.** The framework is explicit: do not focus on where the target
trades relative to deal consideration. No price, no spread, no implied probability from
the tape.

**Tables and text only.** No charts, no graphics.
