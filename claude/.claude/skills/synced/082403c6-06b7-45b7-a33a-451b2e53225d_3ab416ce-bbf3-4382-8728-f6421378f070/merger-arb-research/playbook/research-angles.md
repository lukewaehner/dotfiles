# Research angles

Load when: building a research tree in Hour-1, or when Minute-1 has one deciding question worth a quick probe.

Most first reads use one kind of source, usually the deal filings. Answers that move spreads tend to come from
a second or third kind: a regulator's register, the buyer's own history, procurement data, a rival's filing, a
docket. For each sub-question, pick angles from at least three rows. Tool names are in
`precedents-and-sources.md`.

## Kinds of source

| Kind | What it answers | Where |
|---|---|---|
| The parties' own filings | Terms, footprint, revenue by country, subsidiaries, licences, risk factors, legal proceedings, past deal timelines | EDGAR: 8-K, 10-K (Item 1, 1A, 3, Ex-21), 10-Q, DEF 14A, S-4/DEFM14A of past deals, SEC comment letters (CORRESP/UPLOAD) |
| The buyer's own history | How its past deals went: regulators, durations, remedies, mitigation | Its past announcement and completion releases, annual reports (foreign buyers: universal registration document, annual report), its past merger proxies' "Regulatory Approvals" sections, ArbJournal |
| Regulator registers and decisions | Whether a filing exists, how similar cases went, timing in practice | FTC early-termination list and press releases, DOJ ATR cases, EC case search (M.xxxx), CMA case pages, SAMR decisions, ACCC register, Competition Bureau, state AG and health agency notice pages (Oregon HCMO, Massachusetts HPC, California OHCA), FCC ECFS dockets, FERC eLibrary, state PUC dockets, bank regulators' orders |
| National security and government business | Sensitivity of the target, existing mitigation, clearances | CFIUS annual reports, Treasury press releases, DCSA FOCI guidance, the target's FedRAMP marketplace listing and DoD Impact Level authorizations, USAspending.gov and SAM.gov contract awards, GSA schedules, the buyer's U.S. federal subsidiary's own site and press |
| Precedent deals | Durations, outcomes, friction (pull-and-refile, second request, Phase 2, mitigation) | ArbJournal precedents and vector search, completion 8-Ks, law-firm deal summaries |
| Courts | Pending suits, appraisal, past enforcement, how a judge has ruled | Dockets (federal and Delaware Chancery), caselaw search, plaintiff-firm "investigation" announcements |
| Policy and enforcement posture | Agency leadership statements, pending rule changes, political attention | Federal Register, agency speeches and policy statements, congressional letters, comment dockets |
| Holders and insiders | Who votes, who rolls, who pledged, who sold | 13D/13G and amendments, Forms 3/4, 13F, the proxy's beneficial ownership table |
| Money behind the buyer | Equity providers, LPs, control | Form D, Form ADV (Schedule D), 13F, fund marketing materials, press on fundraises, foreign registries |
| Customers, suppliers, contracts | Change-of-control exposure, overlap at product level | Material contracts filed as exhibits, customer press releases, product pages and catalogues of both parties (including the buyer's acquired brands), trade press, conference agendas |
| Market | Price, unaffected date, technicals, credit | Price history, short interest, index rebalance calendars, bond and loan prices, options |
| Commentary | How specialists read a regime or a clause | Law-firm client alerts, regulator-practice guides, academic or trade analysis (always traced back to a primary source before it reaches the memo) |

## Example trees

**Foreign buyer of a target with U.S. government business (CFIUS).**
Sub-questions: what does the target sell to the government and under which authorizations (FedRAMP, DoD IL,
facility clearances); does the buyer already operate a cleared U.S. subsidiary and under what instrument (SSA,
proxy agreement, board resolution); has the buyer been through CFIUS and how long did it take; how have recent
same-country, same-sector reviews ended; does a rival already sell to the government under a FOCI arrangement
(the template for mitigation); does the agreement's burdensome-condition definition cap that mitigation; how
does the outside date compare with a 45-day review plus a 45-day investigation plus a possible refile.
Angles: target 10-K and contract data, FedRAMP marketplace, USAspending, the buyer's annual report and its
U.S. subsidiary's site, the buyer's past completion releases, CFIUS annual reports, rival filings and press,
law-firm CFIUS commentary, the agreement's efforts and definitions.

**Sponsor or new-vehicle buyer with undisclosed equity.**
Sub-questions: who controls the buyer; who are the equity providers and what have they raised (Form D); have
they backed deals of this size; is any of the money foreign; does the reverse fee have real security; what
does the debt commitment (if any) say about conditions and flex.
Angles: the agreement's financing representations and definitions, Form D and ADV, 13F, prior deals by the
same providers, press on fundraises, the escrow and guarantee terms.

**Multi-state health care target.**
Sub-questions: which states have transaction-notice or prior-approval laws that reach this target and this
buyer; which states the target operates in and at what scale; which clocks run longest from the latest
permitted filing date; has the target or buyer filed in those states before.
Angles: state statutes and agency notice pages, the target's site locations and licences, its past merger
proxies, the agencies' published transaction lists, law-firm state-law trackers.

**Timing set by financing mechanics.**
Sub-questions: when can the marketing period start; which blackout does it hit; when does financial
information go stale; does an audit date force a restart; can the debt fund into escrow early.
Angles: the agreement's definitions, the target's filing calendar and fiscal year, deal_clock, precedent
sponsor deals' actual close dates against their marketing-period terms.

These are illustrations. Build the tree the deal calls for.
