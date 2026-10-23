# State health care approvals

Load when: the target is a multi-state health care provider or services business (pharmacy, home infusion, home health, clinics, physician practices, behavioral health, labs); the press release cites "state regulatory approvals" or "health care regulatory approvals"; the agreement has a separate filing deadline or a higher efforts standard for health care filings than for antitrust; the state list sits in a confidential disclosure letter.

## Why it matters

On a multi-state provider deal the slowest state often sets the closing date long after HSR has expired, and a prior-approval state can stop it. State transaction laws are threshold-triggered, so the 10-K Regulation section, which lists licences, will not show them, and the agreement usually hides the state list in a disclosure letter. Treat the deal as at least conditionally dual-gated at announcement and derive the state list yourself; "list unfiled" is a sourcing gap, never the answer.

## The three layers

| Layer | What it is | Trigger | On the critical path? |
|---|---|---|---|
| A. Transaction notice and review laws | Advance notice, sometimes review or approval, before a health care deal closes | Revenue, asset or in-state presence thresholds at party or parent level | Can be: long lead times set the earliest date; comprehensive reviews set the tail |
| B. Licensure and change of ownership | Resident and non-resident pharmacy, home infusion, home health and similar licences; certificate of need where it survives | Holding the licence in that state | Often, because the slowest single state sets the date (Walgreens/Sycamore closed 108 days after HSR expiry on state work; general knowledge, verify). Name the slow states |
| C. Federal program and accreditation | Medicare and Medicaid enrollment ownership changes, DEA registrations, accreditation notices | Program participation | Rarely; usually notification. Confirm in one line |

## What to check

- Target footprint by state: sites, licences, revenue where given (10-K, state licence lookups, the target's own licensing pages). Site counts are a proxy only.
- Each Layer A statute's own threshold, applied at the level the statute names: the target, the acquirer's ultimate parent, and any sponsor or affiliates the statute counts (agency pages; a current law-firm guide to health care transaction laws, which change yearly).
- The target's earlier state notices from prior deals (agency public notice pages). A past filing shows the state treated it as covered.
- State regulatory approvals paragraphs in the target's and acquirer's earlier merger proxies; note when they say only "certain states".
- Agency public notice pages for this deal. A posted filing is a monitorable before any proxy.
- The agreement: health care filing deadline (often 30 business days after signing; count with `deal_clock.py bdays` on the agreement's calendar), efforts standard for health care approvals, whether each state is a listed closing condition, outside date.
- Each regime's effective date, so precedents can be tagged by era.

## The perimeter test

1. Test the statute's measure. A one-site state can be in on a revenue test; a ten-site state can be out because it has no transaction law. A note that calls a small-footprint state "unclear" has substituted a proxy for the test.
2. Measure at the right level. Massachusetts counts the revenue of the uppermost parent in the business of health care and all affiliates, including revenue outside Massachusetts, so a large strategic buyer usually meets it. Maine's law targets private equity, hedge fund and certain management-services buyers taking majority interest or control, so the buyer's identity decides coverage.
3. Answer three separate questions for each state: does the statute apply; is it notice-only, review with possible referral, or prior approval; is it a listed closing condition. A statute can require a filing the agreement's list omits.
4. Rank states by regime and clock, never by site count.

## How to conclude

- Status per state: **Applies** / **Likely** / **Probable** / **Possible, verify** / **Notice only** / **Not a transaction gate** (no Layer A law; falls to Layer B). Name the fact that would move each one.
- The perimeter lands as **Bounded** at worst: named states, regime, notice or approval, the deciding data, and a watch list (agency notice pages, proxy regulatory section, target's prior filings). **Blocked** is allowed only for the disclosure letter's exact list, and only beside a Bounded perimeter.
- When sources disagree on which states are in, a note that tested the statute's revenue measure beats one that counted sites, regardless of broker tier. If the statute-based note's inputs are unverified, carry its conclusion as Probable.
- One desk line: state health approvals set the date; earliest close [date] on lead times; tails run to [date] ([states]); [conditional state] could push to [date] if it applies.

## Clock arithmetic

Count from the filing date. Announcement-based counts understate the clock. Compute with `deal_clock.py adddays --start <filing> --n <days> --base <base close> --outside <outside date>`.

- **Floor** = filing date + notice lead time. The deal cannot close before it.
- **Tail** = filing date + comprehensive-review outer bound. Compare to the base close and the outside date: a tail well inside the outside date is a timing risk; a tail near or past it is a completion risk. Say which.
- Run both at the agreement's latest permitted filing date and at an early-filing date.
- Where a clock tolls on an information request (Oregon explicitly), state it as "from complete notice, before tolling".
- Run down conditional rules. If a possible regime's lead time would push the earliest close past base, show the arithmetic, label it conditional, name the deciding fact (coverage of this buyer and target, treatment of pending deals), and add it to the watch list.

Hypothetical illustration: filing on day 0 under a state with a 90-day notice and another with a 180-day comprehensive review gives a floor at day 90 and a tail at day 180. If the agreement allows 30 business days to file, both move out about six weeks from announcement, which an announcement-based comparable hides.

## Reference data: Layer A laws (secondary sources read October 2026; laws change yearly; re-verify every row you rely on)

| State | Notice before closing | Review | Type |
|---|---|---|---|
| California (OHCA) | 90 days | 45 days initial; 60 days to notify a cost and market impact review; review done within 90 days (+30) of that determination | Notice with possible cost review |
| Connecticut | 30 days | Up to 200+ days | Review |
| Illinois | 30 days | No stated timeline; attorney general discretion | Notice |
| Indiana | 90 days | No stated timeline; attorney general discretion | Notice |
| Maine | 180 days | 60 days to approve, conditionally approve or refer to comprehensive review (triggered by, among other things, more than $100M of assets transferred). Review process begins 1 January 2027 | Prior approval; covers private equity, hedge fund and certain management-services buyers taking majority interest or control of a provider |
| Massachusetts (HPC) | 60 days | 30 days initial; cost review of 74 to 104 days staff analysis, up to 30 days for party response, 30 days to final report, then a 30-day wait before closing; about 215 days outer bound | Notice with possible cost review |
| Minnesota | 60 days (revenue $80M or more); 30 days ($10M to $80M) | No stated timeline | Notice |
| Nevada | 30 days before; 60 days after closing | No stated timeline | Notice |
| New Mexico | Before closing | 120 days to approve or disapprove | Prior approval |
| New York | 30 days | None | Notice only |
| Oregon (OHA) | 30 days | 30 days preliminary; up to 180 days comprehensive; both extendable while awaiting information | Review with approval authority |
| Rhode Island | 60 days | No stated timeline | Notice |
| Washington | 60 days | No stated timeline | Notice |

Thresholds: California applies at annual revenue or California assets of at least $25M, or at least $10M when transacting with an entity meeting $25M, or any party serving a designated primary care shortage area (agency source). Oregon was reported by one broker as $25M for one party and $10M for another on a three-year average; not verified against the rule.

Only prior-approval regimes (Maine, New Mexico, Oregon's review) can stop a closing outright, and only long notice lead times (California 90, Indiana 90, Maine 180) set a hard earliest date. Carry a notice-only state as a line in the table; it does not gate the close.

## Precedents

- Count comparables from filing as well as from announcement.
- Tag each comparable by regime era ("before [state] regime" or "after"). A comp set that predates the regimes now in scope is a floor on duration; do not use it as the central estimate.
- Keep the HSR-era tag as well; a row can carry both.

## Common errors

- Stopping at "state list unfiled" or "per disclosure letter".
- Calling the gate "state pharmacy licensing" without testing Layer A statutes.
- Ranking states by site count or treating site count as the coverage test.
- Testing revenue at the target level when the statute counts the buyer's parent or the sponsor's affiliates.
- Treating a notice-only state as a gate, or a prior-approval state as a formality.
- Counting clocks from announcement or ignoring tolling.
- Leaving a possible long-lead-time state (Maine) unexamined because coverage is uncertain.
- Using a comp set from before the current state regimes as the central estimate.
