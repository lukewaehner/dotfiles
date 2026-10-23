# Buyer branch: strategic acquirer

The acquirer **is** the competitive entity, and it files. No discovery exercise is needed — its own
10-K/10-Q substitutes for portfolio mapping. The work is a rigorous two-company comparison, and the
risk profile skews toward the classic direct-horizontal case, which is often *higher*-scrutiny than a
sponsor deal: two named competitors merging is exactly what the agencies are built to catch.

## Mapping the acquirer

From the acquirer's latest 10-K / 10-Q (use `extract-10k` — it returns the Competition section and
segment tables directly):

- **Segments and business lines** with revenue by segment, cited.
- **The Competition section verbatim**, cited. Then the **mutual-listing check**: does the target
  appear in the acquirer's competitor list, or the acquirer in the target's? A named-competitor
  merger is the strongest overlap evidence available in public filings, and where it exists the
  horizontal case is largely made by the parties' own disclosures. Flag it prominently rather than
  burying it in a table.
- **Geographic revenue breakdown** from the segment tables, verbatim with citation.
- **M&A history** over the past 5–10 years in this sector — the strategic analogue of roll-up
  analysis. Serial acquisitions of nascent competitors invite killer-acquisition scrutiny.
- **Acquirer regulatory history** — prior reviews, second requests, consent decrees, blocked or
  abandoned deals, behavioural remedies still in force. An acquirer operating under a live decree
  faces a different review; state the finding explicitly either way.
- **Vertical check** — is either party a disclosed supplier to or customer of the other
  (customer-concentration disclosures, supply-agreement 8-Ks)? A pre-existing link makes foreclosure
  concrete rather than hypothetical.

**Deliverable — Acquirer Competitive Footprint table:** segment / business line | revenue (cited) |
disclosed competitors in that line (verbatim, cited) | relevance to target.

**Deliverable — Overlap Screen table:** acquirer segment/line | overlap type | overlapping target
line | geography | evidence citation.

## Strategic-specific theories of harm

- **Unilateral effects** — head-to-head competition eliminated. Closeness-of-competition evidence
  comes from mutual competitor listings, overlapping customers, and win/loss dynamics in trade press.
- **Coordinated effects** — whether the post-merger structure is conducive to tacit coordination
  among the remaining rivals.
- **Killer acquisition / entrenchment** — acquiring a nascent or potential competitor to neutralise
  it. Weigh the target's pipeline and R&D against the acquirer's incumbency.
- **Vertical foreclosure with existing relationships** — where pre-deal supply or customer links
  exist, the foreclosure incentive is concrete.
- **Access to rivals' confidential information** — test this whenever the target hosts or manages data
  for companies that compete with the acquirer (design files, product records, pricing, customer lists held in the
  target's software or cloud). It is a different theory from foreclosure: the worry is not that rivals lose the
  product but that the acquirer can see what is in it. Three checks: does the target host the data itself or does
  it sit on the customer's own systems; which of the acquirer's competitors are named customers, with a source;
  and has a reviewing agency put this theory in a guideline or a recent decision (see Agent F's regulator-state
  return). Record what the parties have said about customer relationships, marked as a party statement. The usual
  fix is a firewall commitment, so check it against the agreement's remedy limits. Expect it to add time at the
  agency that has written it down, and say which one.
- **Synergy-claim exposure** — cost synergies framed around capacity rationalisation, plant
  consolidation, or pricing / go-to-market overlap are read by regulators as admissions of horizontal
  proximity. Quote the framing from the press release or deck and carry it into the effects table.
- **Self-drawn combined market position** — if the deck maps a pro-forma share, rank or "#1 in X"
  claim, that is the acquirer's own market definition and its own overlap admission. Capture it
  verbatim with the slide cited.

## When the strategic deal is market-extension, not horizontal

Many strategic acquisitions join non-overlapping franchises — a pharma company buying into a
different therapeutic area, a software company buying an adjacent category. The right move is to
**resolve the threshold question first and say so plainly**, then reframe the portfolio-context test
rather than skipping it: state whether the combination is platform-diversifying or
franchise-concentrating, whether there is customer overlap to cross-sell into, whether any combined
data asset arises, and whether any competing development path is removed. That reframing is what the
ZYME/TBPH exemplar does, and it is the difference between a section that concludes "no overlap" with
evidence and one that simply has nothing in it.

Two traps in this case, both of which make a clean deal look under-analysed:

1. Write "concentration analysis is **inapplicable** — the parties do not participate in a common
   relevant market", not "HHI could not be calculated". The second implies missing work.
2. Where the parties share a *nominal* touchpoint — both list a preclinical program in the same
   broad area, both mention a category in a risk factor — address it explicitly and say why it sits
   below any cognisable overlap threshold (research-stage, no shared target, no marketed product, no
   near-term competition). An unaddressed touchpoint is the thing a careful reader finds and the
   memo did not.
