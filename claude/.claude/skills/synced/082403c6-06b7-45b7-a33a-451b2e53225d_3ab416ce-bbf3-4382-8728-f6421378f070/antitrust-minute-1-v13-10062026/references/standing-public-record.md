# Standing public record — what was knowable before the deal was announced

**Why this file exists.** On PTC / Schneider Electric (October 2026) a broker note the next morning carried five
facts our memo lacked, and every one of them was public before the announcement: the target's Defense Department
cloud authorization (2019), the buyer's own earlier deals and how long they took (2020 to 2021), the buyer's
cleared U.S. subsidiary (April 2025), a pending rule change at a reviewing agency (April 2026), and the fact
that the target's closest rival already sells the same software to the government under a foreign-ownership
arrangement. The first five gather agents read the merger agreement and the parties' SEC filings. None of them
is assigned to the public record outside those filings, so nothing sent us there. Agent F does that job.

The point is not more research. It is a **fixed checklist with a reported result for every line**, run in the
same block as the other agents so it costs no wall-clock time. A check that was skipped must look different
from a check that found nothing.

## Contents

1. Our own library first
2. Sector trigger packs
3. Rival mirror
4. Acquirer profile
5. Regulator state
6. Prior strategic interest
7. The coverage ledger (required output)
8. Questions for counsel
9. Tool notes and fallbacks

---

## 1. Our own library first

Before any web search, pull what the desk already holds. Documents saved before the announcement are the
cheapest source there is, and listing one as "unread" in a finished memo is a miss we have made before.

- Run `semantic-search` on the Drive namespace (`default`) with the four-field ticker filter for the target, and
  again for the acquirer, limited to documents published in the 12 months before the announcement. Use a high
  `top_k` and `rerank=false` to enumerate, then list the distinct files (source, type, date).
- For each file, either read it or keyword-sample it for the deal's live questions (government, defense,
  classified, the acquirer's name, the named regulators, China, the target's main products). Say which you did.
  The vector search returns chunks, not whole files, so "sampled" is the honest word unless the file was read
  through `download-drive-file` or `read-document`.
- Expert-call transcripts and initiation notes get priority: they name private competitors, customers and
  end markets that filings leave out.
- Every file ends in one of three states in the ledger: read, sampled (say for what), or not read (say why).

## 2. Sector trigger packs

The target's end markets select a named list of registries and regulators. This generalises what
`state-healthcare-regimes.md` does for state health care approvals: the exposure is found by testing the target
against a known list, not by waiting for the agreement to name it.

Pick every pack the target's 10-K end markets, customer list or press releases touch. If none fits, say so in
one line and run the generic row at the end.

### Defense and government (software, services, components)

| Check | Where to look | What to record |
|---|---|---|
| Facility and personnel clearances | Merger agreement government-contracts representation (once filed); 10-K; company careers and press pages | Whether clearances exist, and the level if stated. "Level not disclosed" is the usual answer. |
| Foreign-ownership instrument today | The same representation; company site | Whether the target already operates under a mitigation instrument |
| Federal cloud authorization | The FedRAMP Marketplace listing; the company's own product pages | Level (Low, Moderate, High), which product, sponsor agency if shown |
| Defense Department cloud authorization | Company releases; trade press (ExecutiveBiz, Nextgov, FedScoop) | Impact Level and year |
| Federal contract dollars | USAspending recipient profile, or a third-party aggregator of it | Total obligations, period, top three agencies, largest award. Flag "aggregator, single source" when that is what was read. |
| Named programs | Company releases; agency releases | Program, agency, year, reported value, and whether the company confirmed the value |
| Export-control status | 10-K regulation and risk sections; the agreement's representations | ITAR registration or export classification if stated; otherwise "not found after search" |
| Hosted or on-premises | Product pages | Whether the target itself hosts customer data. This decides whether a data-access concern exists at all. |
| Government and defense revenue share | Filings only | "Not disclosed" unless a filing states it. Broker figures are cited as broker figures and never blended. |
| Pending ownership rules | See section 5 | Any rule that widens the review beyond classified work |

### Other packs (short form; research live and say so)

| End market | Registries and regulators to test |
|---|---|
| Health care services | Use `state-healthcare-regimes.md` in full |
| Telecom and media | FCC licences held (Universal Licensing System, International Bureau), Team Telecom review, state utility commissions |
| Energy and utilities | FERC section 203, state commissions, NRC licences, CFIUS for critical infrastructure |
| Banks, insurers, broker-dealers | Use `regulatory-clocks.md`; add the Federal Reserve and OCC application lists and state insurance filings |
| Semiconductors and advanced technology | Export classifications, CHIPS Act funding conditions, SAMR's record on the sector, CFIUS critical-technology test |
| Personal or sensitive data at scale | CFIUS sensitive-data test, state privacy regulators, the EU's data and digital rules |
| Generic row (always) | The target's top five customers by name where disclosed, and whether any is a government body or a competitor of the buyer |

## 3. Rival mirror

For the top two or three competitors named in the target's 10-K, record who owns each and how each holds the
same regulated standing the target holds. A regulator that already accepts a foreign-owned rival under a known
structure has shown what it tolerates, which is better evidence than any forecast.

| Rival | Ultimate owner and country | Same authorization or licence? | Structure used | Source |
|---|---|---|---|---|

"Structure not disclosed" is a valid entry. A rival that tried for the same authorization and failed is also a
finding, because it bears on whether the target can be replaced.

## 4. Acquirer profile

Build this once per buyer and reuse it. Serial acquirers come back.

- **Track record table.** Every deal the buyer has announced in roughly the last six years: target, country,
  announce date, close date, days (use `scripts/deal_clock.py`, never mental arithmetic), approvals known to
  have been required, the date each landed where public, and any remedy or condition. Buyer press releases
  usually give both dates. Include deals done through a controlled subsidiary. Include the outlier that took two
  years; it shows what the buyer will sit through.
- **Apply it.** State the range in days and the calendar dates that range implies for this deal, then say in one
  sentence how this target differs from those targets (bigger, cleared, hosted data, a new regulator). This is
  the first timeline anchor in Section E. Generic comparables come second.
- **Existing regulated footprint.** Subsidiaries that already hold the licence, clearance or mitigation
  arrangement the target will need. Quote the company's own description and date it.
- **Exposure a reviewer will ask about.** Revenue by region from the latest annual results, any state or
  sovereign shareholders, and the buyer's footprint in countries of concern to the reviewing agency (rank among
  its markets, R&D sites). "Share not disclosed" where it is not.
- **Deals in flight.** Any other pending acquisition by the same buyer, its announce date and what is known of
  its approvals. A review already under way for the same buyer is the best live read on its standing.
- **Save it.** If the Projects tool is present, write the profile to the project as
  `claude/Acquirer Profile - [BUYER] ([MM.DD.YYYY]).md` so the next deal by the same buyer starts with it. Check
  for an existing profile before building a new one.

## 5. Regulator state

For each agency likely to review, two questions.

1. **Is a rule or guideline about to change?** Draft guidelines, proposed rules and consultation papers signal
   where an agency is heading even before they bind. Record the document, its date, the comment deadline and the
   expected final date, and say plainly that it is not yet in force.
2. **What happened to the nearest comparable deals in the last 12 months?** Cleared, cleared with conditions,
   withdrawn, blocked. If a search for a blocked or abandoned comparable finds nothing, write "not found after
   search". That absence matters: it is the check on any unsourced claim that an agency "is blocking deals".

Minimum set: the US antitrust agencies, CFIUS and the Defense Department for a foreign buyer or a
government-facing target, the European Commission, the UK CMA, SAMR, and any sector regulator a trigger pack
named. Agents D and E already cover enforcement posture and clocks; this section adds pending changes and the
last year's outcomes, and does not repeat them.

## 6. Prior strategic interest

Search the news record for earlier approaches to the target (reported bids, talks, activist campaigns) in the
last three years. Record who, when, at what reported price, and how it ended. This feeds the counterbid read and
tells you whether the board already knew its options.

## 7. The coverage ledger (required output)

Agent F returns, and the memo prints in Section F, one table that accounts for every check above:

| Check | Result | Status | Source |
|---|---|---|---|
| (one row per check run) | (the finding in a few words) | Found / Not found after search / Not searched | (citation) |

Rules:

- **Found** needs a citation. A company's own page is marked as the company's statement.
- **Not found after search** means a real search was run. Name what was searched.
- **Not searched** is allowed in the agent's return but not in the delivered memo. Before delivery, either run
  the check or move it to Open Questions with the reason it could not be run (tool cannot read the site,
  document not public).
- Print the three counts under the table. The reader should see at a glance how much of the record was covered.

The ledger exists because the earlier screen already asked for clearances and cloud authorizations and we still
missed them. Nothing forced the check to be reported, so nobody saw that it had not been done.

## 8. Questions for counsel

Some answers are not public and no search will produce them: an agency's current mood, how a clause would be
read, whether one review must finish before another. Do not guess at these and do not leave them out. Close
Section F with three to six plain questions the desk can put to outside counsel or an expert, each tied to the
finding that raised it. Keep them answerable: "Would the Defense Department accept a special security agreement
for this business, as it does for [rival]?" and not "What is the CFIUS risk?".

## 9. Tool notes and fallbacks

- Government registries are often built in JavaScript and `WebFetch` returns little. Try the registry once; if
  it does not read, fall back to a web search that names the registry and the company, then to the company's own
  page or trade press, and mark the row with what was actually read.
- Federal spending aggregators (several sites repackage USAspending data) usually read cleanly. Cite the
  aggregator by name and flag the figure single-source.
- If `WebFetch` or `WebSearch` reports a domain cannot be fetched, do not retrieve it another way. Record the row
  as "not searched: site not reachable with our tools".
- Law-firm client alerts are the fastest reliable source for pending rules and draft guidelines. Cite the firm
  and the date.
