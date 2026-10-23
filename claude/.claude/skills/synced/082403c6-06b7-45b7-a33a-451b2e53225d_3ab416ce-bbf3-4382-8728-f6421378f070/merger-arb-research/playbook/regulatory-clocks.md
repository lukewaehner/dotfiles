# Regulatory clocks and the close-date build

Load when: building or checking a closing date; the deal needs any approval beyond a plain HSR filing (EC, CMA, SAMR, CFIUS, a bank, insurance, telecom, energy or state regulator); guidance runs longer than HSR plus a proxy can explain; a broker or management close date needs testing.

## Why it matters

The spread prices time as much as break risk. A close date read off the middle of a precedent set blends deals with different perimeters and buyers, and it tells the desk nothing about which regulator to watch or what a slip looks like. Build the date bottom-up, one approval body at a time, from the agreement's own filing covenants, and use precedents only as a sanity check.

Most change-of-control regimes share one shape: a short headline period that runs from a complete filing, plus a deficiency or information-request mechanism. Completeness is the elastic variable, and the gap between filing and an accepted filing is rarely disclosed.

## What to check

- Filing covenants and deadlines (merger agreement covenants section; count business days under the agreement's own Business Day definition and holiday calendars with `deal_clock.py bdays`). Typical covenants require filings 10 to 40 business days after signing; label the convention an assumption if the agreement is not yet filed.
- Which regimes are closing conditions and which appear only as covenants (conditions article). Only a condition can hold the close.
- Efforts standard, divestiture cap or confidential remedy basket, litigation commitment, remedy-proffer deadline, pull-and-refile rights and caps, timing-agreement limits (efforts covenant). Compute every dated covenant to a calendar date.
- Outside date and extension ladder (termination article; `deal_clock.py ladder`). Note which extension step the company's guidance first fits inside.
- Ticking fee trigger date, the approvals that trigger it, accrual end and cap. The trigger date is the parties' revealed base case for when those approvals land.
- Advisor list and approvals sentence in the press release. Dedicated sector counsel on both sides with no antitrust firm named, or a release that names a sector regulator and omits HSR, tells you which review the parties expect to bind.
- Target 10-K Regulation section, read in full, for regulators outside the headline sector (a FINRA broker-dealer, an RIA, a licensed foreign entity, a captive insurer). These are findable on day one.
- The acquirer's own track record: announce-to-close days on its last five or six deals, the approvals each needed, any remedy (buyer press releases, 8-Ks; compute with `deal_clock.py`). This comes before generic comparables.
- Agency posture and pending rule changes (agency sites, law-firm alerts, the desk's research index on active second requests and CFIUS reviews).
- Any broker, headline or management date: run it through `deal_clock.py --check` for weekends, holidays and dates the filing covenant cannot physically allow.

## How to build the date

1. For each approval body, confirm it requires approval, notification or nothing. Count authorised entities and domiciles; a count of countries or licences overstates the perimeter. Branches and passported entities usually need only home-supervisor approval.
2. Estimate the filing date from the covenant (latest permitted date) and an early-filing case.
3. Add unclocked pre-filing engagement where the regime expects it (EC, CMA, CFIUS, prudential supervisors, FINRA).
4. Apply the statutory clock from its real start, plus the interruption that the buyer's domicile or profile makes likely.
5. Apply the acquirer archetype adjustment (table below).
6. State which approvals run in parallel and which are sequenced, and label sequencing as an assumption. Some sector regulators wait for antitrust clearance; ministerial steps follow the prudential recommendation; a lead state may wait on a sister state. Sequencing errors are the largest single source of timeline error.
7. Base-case close = latest single approval date plus a short closing tail (a few business days, or the tender expiry mechanics). Compare to precedent and to guidance; where they disagree, say which you trust and why. Usually the build governs.
8. Second-gate test: list every clock by derived approval date, name the second-longest, say how many days behind the gate it sits, and name the event that would make it overtake (Phase 2, call-in, refile, investigation period). Write it as one sentence: gated by X; Y is the second clock N days behind and would overtake it if Z.

## Cash tender and HSR mechanics

- HSR waiting period: 30 calendar days for a merger; 15 for a cash tender offer. Day one is the day after filing; expiry is 11:59 pm ET on the last day and rolls to the next business day off a weekend or federal holiday.
- Tender offer period: at least 20 business days under Rule 14e-1, counted per Rule 14d-1(g)(3) (weekends and federal holidays excluded, so Columbus Day and Veterans Day count as closed). Read the agreement's launch covenant, HSR covenant and initial offer period, then run `deal_clock.py tender`.
- If the Business Day definition names a local holiday calendar, report the agreement-calendar deadline and the weekends-only count side by side; brokers use both.
- Working close date is the contractual floor on the agreement's calendar, stated as "earlier if the parties file early". Add days only for evidence in hand: an overlap whose precedents needed a refile or second request, a documented agency posture, or a later state or foreign clock.
- Pull-and-refile: the parties withdraw before expiry and refile (within two business days, no new fee, per 16 CFR 803.12; verify) to restart the period and give staff a second look without a second request. It is a friction signal. Treat it as a downside scenario unless the cited precedents needed one.
- Second request: extends the period to 30 days after substantial compliance (10 days for a cash tender). Compliance alone commonly takes several months, and parties usually sign a timing agreement with staff that adds advance notice of closing (commonly 60 to 90 days after compliance) and caps on custodians and depositions. Realistic signing-to-close on deals with a second request is roughly 10 to 14 months, longer with litigation; verify against current DAMITT-style duration statistics.
- State premerger statutes named in the filing covenant (copy-of-HSR states) get their own row; most carry no separate waiting period, but verify each.

## Reference data (verify each critical-path row live, and date-stamp what you used)

### Antitrust

| Regime | Statutory clock | What starts it | Interruption and practical range |
|---|---|---|---|
| US HSR | 30 days (15 cash tender) | Filing by both parties (acquirer only for a tender) | Pull-and-refile restarts; second request runs to 30/10 days after substantial compliance plus any timing agreement |
| EC (EUMR) | Phase 1: 25 working days (35 with remedies or a member-state referral request). Phase 2: 90 working days, +15 if remedies offered late, up to +20 on request | Formal notification | Pre-notification is its own unclocked period and on complex or interoperability-heavy deals is most of the timeline; 5 to 6 months has been sourced on recent software deals. Stop-the-clock on information requests in Phase 2 |
| UK CMA | Phase 1: 40 working days. Phase 2: 24 weeks, extendable by up to 8 | Formal notification (CMA confirms completeness) | Voluntary and non-suspensory, but interim orders can hold integration. Pre-notification commonly 1 to 3 months; check current Mergers Charter targets |
| China SAMR | Phase 1: 30 days; Phase 2: 90 days; extension 60 days | Acceptance of a complete filing | Pre-acceptance can take weeks; stop-the-clock power since the 2022 AML amendment; simplified cases often cleared within weeks of acceptance |
| Canada Competition Act | 30-day waiting period; supplementary information request restarts 30 days after compliance | Complete notification | Advance ruling certificate or no-action letter can end it early |

### Foreign investment and national security

| Regime | Clock | Notes |
|---|---|---|
| CFIUS declaration | 30 days | Outcome may be a request to file a full notice, which restarts the process |
| CFIUS notice | 45-day review, 45-day investigation (+15 in extraordinary cases), 15 days for a presidential decision | Draft notice and acceptance come first and are unclocked. Withdraw-and-refile restarts the 45 days and is common |
| UK NSIA | 30 working days to call in; assessment 30 working days plus 45 more, extendable by agreement | Mandatory and suspensory in 17 sectors |
| Canada ICA national security | Can be triggered for any investment, any size; multi-stage periods can run well past 200 days | Separate from net-benefit review |
| Japan FEFTA prior notice | 30-day standard wait, often shortened, extendable | Designated sectors |
| EU member-state FDI (Germany, France, Italy, Spain) | National Phase 1 and Phase 2 periods, roughly 1 to 4 months each | Check the target's subsidiaries before assuming a filing |

### Sector regulators

| Regulator | Clock and trigger | Practical notes |
|---|---|---|
| US state insurance (Form A, NAIC Model #440) | Control presumed at 10% of voting securities. Commissioner typically acts within about 60 days of a complete filing; hearings mandatory in some states | Approval from each domiciliary regulator only. 4 to 6 months from filing for a straightforward applicant; one or two domiciles have closed in 150 to 180 days announce-to-close; multi-domicile deals run longer. Duration is set by completeness: every ultimate controlling person, NAIC biographical affidavits with third-party background checks, a five-year business plan, source of funds |
| Form E (state competition filing) | 30-day wait where buyer and target write the same line in the same state above thresholds | Inapplicable where the buyer carries no insurance risk; say so as a positive finding. Form A also has a competition limb |
| State captive insurers | Many states carve captives out of the holding-company act; change of control runs under the captive act or rule, often with no stated clock | Benchmark off the state's new-captive licence time; 30 to 90 days from a complete filing is a reasonable band. If the commissioner declines to waive notice and hearing, fall back to a full Form A timeline as the outside case |
| UK PRA / FCA | 60 working days from a complete s.178 notice; interruption up to 30 working days (non-UK applicants) | PRA thresholds 10%, 20%, 30%, 50%; FCA solo-regulated 20%. Appointed representatives usually need no pre-approval |
| EEA Solvency II supervisors | 60 working days, +30 for non-EEA applicants | Belgium runs 82 (EEA) / 92 (non-EEA) working days and is often the longest clocked review in a European insurance deal. Central Bank of Ireland intermediaries: notification only |
| Canada OSFI + Minister of Finance | No statutory clock on the ministerial step | Sequenced after OSFI; a structural long pole |
| Bermuda BMA, Cayman CIMA | Notice or fit-and-proper approval | Rarely binding; confirm approval versus notice |
| FINRA (Rule 1017 CMA) | Prior approval for a change of 25% or more of a member broker-dealer, including limited-purpose BDs | Guidance suggests about 30 days once complete; simple ownership-change applications run nearer 4 to 4.5 months with pre-filing and information cycles. Own row; do not fold into the primary sector clock |
| Registered investment advisers | Advisers Act s.205(a)(2) assignment requires client consent | Negative-consent notice to clients; an AUM-retention risk with no government clock. Form ADV amendment follows closing |
| Federal Reserve, OCC, FDIC | BHC Act, Bank Merger Act, Change in Bank Control Act (60-day notice, extendable) | Public comment, CRA protests and control determinations for fund investors drive length; verify current processing times |
| FCC | 180-day informal shot clock | Routinely paused; treat 180 as a floor and read the pause history of comparables. Team Telecom review of foreign ownership runs alongside |
| FERC (FPA s.203) | 180 days, extendable by 180 | Contested proceedings run long |
| NRC licence transfer | No fixed clock | Research live; foreign ownership limits apply |
| STB (major rail) | Statutory schedule of many months with an evidentiary record | A proceeding; antitrust runs through the agency |
| State PUCs | Highly variable; often the longest pole in a utility deal | Intervenor settlements resemble insurance commitment negotiations |
| State health care transaction laws | See `state-healthcare.md` | Clocks run from a complete notice |
| Gaming, DCSA/DDTC, DOT/FAA | Research live | |

### Acquirer archetype as a timing input (sector reviews)

| Archetype | Regulator posture | Direction |
|---|---|---|
| Incumbent sector strategic, already an approved control person | Known applicant and business model | Fastest |
| Alternative manager with an established regulated platform | Repeat applicant, chain mapped, commitments on file | Fast to moderate |
| Generalist private equity, first regulated acquisition of this type | Full first-time-owner review; commitments negotiated from scratch | Moderate to slow |
| Investor from an adjacent sector, first regulated acquisition | Business plan and capital questions are the review | Slow |
| Foreign, sovereign-linked or opaque ownership | Investment screening and ministerial discretion on top | Slowest |

A first-time private-equity owner of a carrier draws questions on affiliated investment management fees, dividends and leverage, reserves, offshore or affiliated reinsurance and opaque ownership. These are resolved through commitments (capital maintenance, dividend limits, notice undertakings, RBC floors), and negotiating them takes calendar time no statute describes. Continuity of an already-approved control person, or a founder and management rollover, is the most underweighted mitigant; tie it to the specific approvals it helps.

## Decoding timing signals

- Close guidance is negotiated disclosure set against the slowest approval's realistic case, and companies do not guide past their own outside date. A window opening at month 4.5 and closing at month 10.5 says the slow lane is live.
- If guidance runs well past the buyer's own record, list candidate reasons as hypotheses (a security review, another pending deal by the same buyer, a long pre-notification, conservatism) and say which the evidence supports.
- A ticking fee is price protection first. Its trigger date anchors the base case, the named approvals confirm the critical path, and an accrual rate near the desk hurdle neutralises duration risk inside the accrual window; carry it into the IRR math.
- A higher efforts standard or an earlier filing deadline for one regime than for antitrust tells you which review the parties expect to be slower.

## Common errors

- Reporting only the statutory clock, which is the number least predictive of the outcome.
- Averaging precedent timelines into the working date, or counting comparables from announcement when this agreement allows weeks to file.
- Treating a pull-and-refile or second request as a base case when no comparable needed one.
- Counting states where the insurer is licensed instead of its domicile; defaulting a captive to Form A.
- Missing a FINRA, RIA or foreign licensed entity disclosed in the target's own Regulation section.
- Building only the gating clock and never naming the second one; assuming EC Phase 1 is short while ignoring pre-notification.
- Treating parallel filings as additive, or sequenced ones as parallel, without labelling the assumption.
- Repeating a quoted close date that falls on a weekend or before the filing covenant could allow.
