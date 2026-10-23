# National security, CFIUS and foreign-ownership mitigation

Load when: the buyer is non-US, has a foreign parent, foreign co-investors or a fund with offshore vehicles or foreign LPs; the target sells to the US government or defense, holds facility clearances, cloud authorizations (FedRAMP, DoD Impact Levels) or export-controlled technology; the target holds sensitive personal data at scale or operates critical infrastructure; the agreement contains a CFIUS condition, a foreign-person representation, a list of mitigation instruments or a burdensome-condition carve-out for a government business.

## Why it matters

A national-security review can be the longest clock on a deal that looks clean on antitrust, and it usually ends in a mitigation package; outright blocks are rare. The spread question is whether the package the regulator will ask for sits inside what the buyer must accept or inside what it may refuse, and what the buyer pays if it walks. With no reverse fee, a refused remedy means no deal and no payment. End the screen in a verbal call; do not assign a probability.

## What to check

In the merger agreement (cite the section):
- Government-contracts and security-clearance representation: facility clearances, classified contracts, contracts subject to FOCI rules, any mitigation instrument in place today. Absence of such a representation is evidence the target sees little exposure.
- CFIUS: closing condition, filing covenant only, or absent; which side bears mitigation risk.
- Foreign-person representation and any fund clause ("not a foreign person", "not a covered transaction or covered investment"). Quote it, and say that a representation binds no regulator and is no CFIUS determination.
- Efforts clause list of instruments the buyer must accept, and the burdensome-condition definition of what it may refuse.
- Reverse termination fee: amount, whether regulatory failure triggers it, what backs it. Size it against the most recent foreign-buyer deal in the same sector, using that deal's own agreement.
- Outside date and extensions against the CFIUS path (`deal_clock.py ladder`).

In the target's filings and the public record:
- Government programs, agencies and contract vehicles named in the 10-K and releases.
- Federal contract dollars: total, period, top agencies, largest award (USAspending recipient profile; flag an aggregator as single-source).
- FedRAMP level and product (FedRAMP Marketplace); DoD Impact Level and year (company releases, trade press).
- Export-control or ITAR language (Regulation and Risk Factors sections).
- Hosting model: does the target host customer or government data itself, or does it sit on customer premises and government-only servers (product pages, authorization listing). If a program's deployment model is not public, write "deployment model not stated".
- Government and defense revenue share: "not disclosed" unless a filing states it. Cite broker figures as broker figures and never blend them.
- Sensitive personal data on more than one million US individuals (31 CFR Part 800 categories, including geolocation and non-public communications; confirm the current list). A yes makes the target a TID US business for covered investments; a no ends that point.
- Rival mirror: for the top two or three competitors named in the 10-K, the ultimate owner and how each holds the same clearance or authorization. A regulator that already accepts a foreign-owned rival under a known structure has shown what it tolerates.
- Pending rules at DCSA, CFIUS or DoD that widen ownership review beyond classified work (law-firm alerts, Federal Register).

On the buyer side:
- Home country, ownership, any state or sovereign-linked holders, foreign LPs with control, board or information rights (Form ADV, Form D, public pension schedules, the equity commitment description).
- Existing US government and defense footprint, including any cleared US subsidiary operating under a mitigation instrument. Quote the company's own description and date it. It gives the agency a template, but it covers that subsidiary only and extends to an acquired business only by amendment or a new instrument.
- Every prior US national-security clearance the buyer obtained: target, year, instrument if known, sourced from the buyer's own releases or filings.
- Footprint and R&D in countries of concern; who inside the buyer could reach source code or customer data after closing.
- Other pending deals by the same buyer under review.

## Target sensitivity profile (build this table; it is the core of the screen)

| Item | Finding | Source |
|---|---|---|
| Facility clearances and classified work | | Agreement representation |
| Mitigation instrument in place today | | Same |
| Federal cloud authorization (level, product) | | FedRAMP Marketplace or company page |
| DoD cloud authorization (Impact Level, year) | | Release or trade press |
| Hosts customer data itself? | | Product pages |
| Named government programs | | Releases |
| Federal contract dollars | | USAspending or aggregator |
| Export-control status | | Filings |
| Government and defense revenue share | "Not disclosed" unless a filing states it | Filings only |
| Sensitive personal data > 1M US individuals | | Privacy notice, 10-K |
| Rivals with the same standing, and how they hold it | | Rival mirror |

A target holding facility clearances will need a FOCI instrument once a foreign buyer closes. The question then becomes which instrument, and whether the agreement lets the buyer refuse it.

## Reading the mitigation lists

Agreements usually carry two lists; reading only one gives the wrong answer.
1. What the buyer must accept: instruments named in the efforts clause (mitigation agreement, national security agreement, letter of assurance, board resolution, security control agreement, special security agreement, proxy agreement, voting trust). Quote the list.
2. What the buyer may refuse: the burdensome-condition definition, which often excuses a remedy that holds part of the target separately. Split it into a **separation** test (held or governed apart from the buyer) and a **scale** test (all, a significant portion, a line of business). An instrument on the first list is refusable only when both tests are met.

Then say whether the scale words are defined. An undefined "line of business" is ambiguity the buyer can use, and it is where walk-away risk lives. State as an Assessment which packages sit clearly inside the buyer's obligation, which clearly trigger the walk right, and which fall between. Then name the structure the buyer would most likely propose (extend an existing SSA, a new SSA for the cleared unit, a proxy or voting trust, a CFIUS NSA, none) and test it against those lists. That sentence is the finding.

## Reference data (verify current rules and definitions before relying on them)

### CFIUS

| Item | Rule |
|---|---|
| Declaration | 30-day assessment; outcomes include clearance, a request for a full notice, or no action |
| Notice | Draft notice and formal acceptance first (unclocked); 45-day review; 45-day investigation, +15 in extraordinary cases; 15 days for a presidential decision. Withdraw-and-refile restarts the 45 days and is common |
| Mandatory filing: critical technology | Foreign person acquires control or covered rights in a TID US business that produces, designs, tests, manufactures, fabricates or develops critical technology for which a US export authorization would be required to the investor's jurisdiction |
| Mandatory filing: foreign government | A foreign government holds a substantial interest (49% or more) in the investor and the investor acquires a substantial interest (25% or more voting) in a TID US business |
| Timing of a mandatory filing | At least 30 days before completion; penalties up to the greater of $5M or the transaction value under the 2024 rule |
| Voluntary filing | Any other covered control transaction or covered investment; CFIUS can call in non-notified deals |
| Covered investment (non-controlling) | Access to material non-public technical information, a board or observer seat, or involvement in substantive decisions on a TID US business |
| TID US business | Critical technologies, covered critical infrastructure, or sensitive personal data (generally more than one million individuals, or data tailored to US government personnel) |
| Fund exception (31 CFR 800.307) | Indirect investment through a fund by a foreign LP with no control, no access and limited advisory-committee rights is not a covered investment |
| Excepted investors | Investors from excepted states (Australia, Canada, New Zealand, UK; confirm list) meeting ownership and conduct criteria are exempt from mandatory filing and covered-investment jurisdiction |

### FOCI mitigation instruments (DCSA), lightest to heaviest

| Instrument | What the foreign owner gives up | Notes |
|---|---|---|
| Board resolution | Excludes the foreign owner from classified information | Minority, non-controlling holdings |
| Security control agreement (SCA) | Outside directors on the cleared entity's board; owner keeps control otherwise | Foreign owner cannot control the cleared entity |
| Special security agreement (SSA) | Outside directors, government security committee, limits on affiliate access | Access to proscribed information (Top Secret, SAP, SCI, COMSEC, Restricted Data) requires a national interest determination, which is a known slow item |
| Proxy agreement or voting trust | Voting rights pass to cleared US proxies or trustees; owner keeps economic rights only | Heaviest; most likely to trip a separation-and-scale walk right |

CFIUS outcomes are separate instruments (national security agreement, letter of assurance) and can run alongside DCSA FOCI mitigation. Team Telecom reviews foreign ownership in FCC licence transfers.

### Foreign national-security and FDI regimes

| Regime | Trigger | Clock |
|---|---|---|
| UK National Security and Investment Act | Mandatory and suspensory for acquisitions crossing 25%, 50% or 75% (or gaining veto rights) in 17 sectors, including defence, dual-use and advanced technology; voluntary call-in elsewhere; non-approved mandatory deals are void | 30 working days to decide on call-in; assessment 30 working days plus 45 more, extendable by agreement |
| Canada ICA national security (Part IV.1) | Any investment by a non-Canadian, any size, at ministerial discretion; separate from net-benefit review | Multi-stage notices; can run well beyond 200 days |
| Japan FEFTA | Prior notification for designated sectors, including 1% of a listed company in core sectors | 30-day standard wait, often shortened, extendable |
| EU member-state FDI (Germany, France, Italy, Spain and others) | Sector lists and percentage thresholds, mandatory in sensitive sectors; the EU screening regulation coordinates | Germany about 2 months plus 4; France 30 plus 45 business days; Italy 45 days; verify per regime |
| Australia FIRB | National-security businesses with no monetary floor; other sector thresholds | 30-day statutory period, routinely extended |
| South Korea, Taiwan, India, Saudi Arabia | Sector or origin-based screening where the target has a local entity | Research live |

Fill the target-presence column from Exhibit 21 and the customers the 10-K or releases name. A regime with no entity and no named customer is not a gate. A regime with a hook and a clock longer than the competition filings is a candidate second gate in the close-date build (`regulatory-clocks.md`).

## How to conclude

- Print the sensitivity profile and the instrument sort, then two or three sentences ending in a verbal call: is a national-security review likely to be a gate, which instrument is likely, does it sit inside the buyer's obligation or its walk right, and does the CFIUS path (filing, 45 plus 45, a possible refile) fit inside the outside-date ladder.
- If asked for a worst case, give the strongest good-faith version the facts support, then what in the documents cuts against it.
- End with three to six answerable counsel questions tied to findings (for example whether DCSA would accept an SSA for this business as it does for a named rival; whether holding the cleared unit under a proxy trips the burdensome-condition carve-out).
- Re-run the whole screen when the merger agreement is filed; a press-release screen cannot see the clearance representation or the burdensome-condition wording.

## Common errors

- Treating the foreign-person representation as a CFIUS determination.
- Writing that the buyer "has" an SSA group-wide when only one subsidiary operates under it.
- Reading the must-accept list without the burdensome-condition carve-out, or the reverse.
- Estimating government revenue share from a sell-side figure.
- Saying "data stays with the customer" without a sourced hosting model.
- Saying "the buyer has cleared before" without listing the clearances.
- Ignoring foreign LPs and offshore feeders in a new vehicle's capital stack.
- Treating a regime with no local entity or customer as a gate, or skipping one that has both.
- Noting "no reverse fee" without stating that a refused remedy then ends the deal at no cost to the buyer.
