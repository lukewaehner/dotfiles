# National-security screen (CFIUS, FOCI, defense and government exposure)

Run this on any deal where the buyer is non-US (or has a foreign parent or foreign co-investors), or where the
target sells to government. The aim is to decide whether a national-security review (CFIUS, or its
equivalents abroad) is a realistic gate, and to read what the parties themselves signalled about it in the agreement.
This is a screen, not a probability estimate.

## Read these in the merger agreement (cite the section)

1. **Government-contracts and security-clearance representation.** Does the target say it holds facility
   clearances, classified contracts, or contracts subject to foreign ownership, control or influence (FOCI)
   rules? An agreement with no such representation is evidence the target thinks the exposure is small.
2. **Efforts clause and burdensome-condition definition.** Does the clause carve out a line-of-business ring-fence
   (for example, a defined government or defense business that the buyer need not take on, or may have to
   hold separate)? A named ring-fence means the parties expected the question.
3. **CFIUS condition.** Is CFIUS clearance a closing condition, a filing covenant only, or absent? Which
   side bears the risk of a mitigation agreement?
4. **Reverse termination fee.** Does the buyer owe a fee if a required approval fails? "No reverse fee" is a
   finding and goes in the timing table.
5. **Outside dates.** Compare the CFIUS timeline (filing, 45-day review, possible 45-day investigation,
   possible withdraw-and-refile) against the outside-date ladder (`scripts/deal_clock.py ladder`).

## Read these in the target's filings

- Government programs and customers named in the 10-K (agency names, program names, contract vehicles).
- Cloud and security authorizations the products hold (for example FedRAMP) and any named defense or
  intelligence-community customers.
- Any export-control or ITAR language in the Regulation or Risk Factors sections.
- Revenue by customer type. **If defense or government revenue share is not disclosed, write "not disclosed".**
  Do not estimate it from a sell-side figure unless that figure is cited and flagged single-source.

## The buyer side

- Home country and ownership of the buyer; any government or state-linked shareholders.
- The buyer's own existing government and defense footprint, which can reduce or raise the concern.
- Prior CFIUS or foreign-investment reviews of this buyer and their outcomes.

## Target sensitivity profile (build this table; it is the screen's core output)

The agreement and the 10-K rarely say why a target is sensitive. The public record does. Fill this from Agent F's
defense and government pack (`references/standing-public-record.md`, section 2) and from Agent A's extract:

| Item | Finding | Source |
|---|---|---|
| Facility clearances and classified work | | Agreement government-contracts representation |
| Mitigation instrument in place today | | Same |
| Federal cloud authorization (level, product) | | Registry or company page |
| Defense Department cloud authorization (level, year) | | Release or trade press |
| Does the target host customer data itself? | | Product pages |
| Named government programs | | Releases |
| Federal contract dollars (total, period, top agencies) | | Spending data; flag an aggregator |
| Export-control status | | Filings |
| Government and defense revenue share | "Not disclosed" unless a filing states it | Filings only |
| Rivals with the same standing, and how they hold it | | Rival mirror |

A target that holds clearances needs a foreign-ownership mitigation instrument after a foreign buyer closes. That
turns the question from "will there be mitigation" into "which instrument, and does the agreement let the buyer
refuse it".

## Sort the mitigation instruments the agreement names

Agreements on these deals usually contain two lists, and reading only one of them gives the wrong answer.

1. **What the buyer must accept.** The efforts clause often lists instruments by name (mitigation agreement,
   national security agreement, special security agreement, security control agreement, proxy agreement, voting
   trust). Quote the list.
2. **What the buyer may refuse.** The burdensome-condition definition often excuses a remedy that holds part of
   the target separately. Quote it, and separate its two tests: **separation** (held or governed apart from the
   buyer) and **scale** (all, a significant portion, or "a line of business"). An instrument on the first list is
   refusable only when both tests are met.

Then say whether the scale words are defined. An undefined "line of business" is an ambiguity that belongs to the
buyer, and it is the place the walk-away risk lives. State, as an Assessment, which mitigation packages sit
clearly inside the buyer's obligation, which clearly trigger the walk right, and which fall in between. Check for
a reverse termination fee: with none, a refused remedy means no deal and no payment.

## The buyer side, in more detail

- **An existing cleared subsidiary.** If the buyer already operates a U.S. subsidiary under a mitigation
  instrument, quote its own description and date it. It gives the regulator a template and the buyer a place to
  put the target's cleared work. It covers that subsidiary only, so do not write that "the buyer has" the
  instrument group-wide.
- **Footprint in countries of concern.** A reviewer will ask who inside the buyer could reach the target's source
  code or customer data. Record the buyer's rank and R&D presence in those countries.
- **Pending rules.** Check Agent F's regulator-state return for any rule that widens ownership review beyond
  classified contracts.

## Run it again when the agreement is filed

A screen run from the press release cannot see the government-contracts representation or the
burdensome-condition wording. When the merger agreement lands, re-run this whole screen in delta mode and replace
the earlier text. On PTC / Schneider the screen ran the day before the agreement was filed and was not re-run,
so the clearance representation sat unread for two days.

## Output

A short table (item, what the agreement or filing says, citation, what it implies) and two or three sentences
that end in a verbal call on whether a national-security review is likely to be a gate, and whether it
fits inside the outside-date ladder. If asked for a "worst-case theory", give the strongest
good-faith version the facts support, then say what in the documents cuts against it.

Print the target sensitivity profile and the instrument sort above the call. End with the counsel questions this screen
raised; they join the list in Section F.
