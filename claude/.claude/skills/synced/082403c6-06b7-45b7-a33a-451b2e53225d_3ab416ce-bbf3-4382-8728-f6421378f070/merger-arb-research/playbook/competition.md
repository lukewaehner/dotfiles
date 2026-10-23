# Competition: overlap, market definition and theories of harm

Load when: the buyer is a strategic operating company, or a sponsor whose portfolio companies sell to
the target's customers; a note or headline claims an overlap or a clean deal; or you must rate second
request, challenge or remedy risk.

## Why it matters for the spread

Antitrust risk moves the spread through two separate channels: a long review (second request, refiles,
foreign filings) costs time, and a real horizontal or vertical problem risks a block or a forced
divestiture. Most mistakes come from reading company-level self-descriptions instead of products, and
from blending "overlap on paper", "slow review" and "regulator sues" into one rating.

## Step 1: classify before any concentration talk

State in one line whether the deal is horizontal, vertical, or market extension. In a true market
extension no shared market exists, so shares and HHI are inapplicable, which is a different statement
from unavailable. If the screen is clean, keep the theories-of-harm discussion short and say why; do not
manufacture depth.

## Step 2: product-level overlap matrix

Company-level checks (do the 10-Ks name each other, do segments match) miss niche lines that sit under
different segment names, and miss acquired units the parent reports in one line. Build catalogs instead.

- Catalog every product each party sells today, including every unit the buyer acquired and still runs
  under its own brand. Sources in order: the product menu on each company's site (legacy pages too);
  the 10-K Business section or a non-US annual report; the acquired unit's last standalone annual report;
  press releases for products no longer on the menu.
- Record each product: what it does, customer type served, current or legacy, source.
- Lay both catalogs on one grid: customer type as rows, task as columns (design, data management,
  simulation, operations, service, and so on). Any cell holding products from both parties is a candidate
  overlap regardless of segment labels. A cell where one party sells and the other sells an adjacent task
  to the same customer feeds the vertical and conglomerate theories.
- Write one sentence per shared cell naming both products and whether they read as head-to-head or
  adjacent. If no cell is shared, say so and cite the catalogs; a clean screen is a finding.
- A product page proves "sells this today" and nothing more. It gives no revenue, share or customer count.

## Step 3: test each candidate overlap

A name in a Competition section is a candidate. Before it raises the overlap read, run four tests:

- Management's own words: search both parties' recent earnings calls, investor days and conference
  remarks for who they call their direct competitors and how they describe the other party. Quote with
  date. A CEO naming a different rival, or calling the other party a partner or complement, outweighs a
  bare 10-K listing; a CEO naming the other party head to head is strong overlap evidence.
- Substitute or complement: would a customer buy one instead of the other, or alongside it?
- Same buyer, same budget: do both sell to the same function inside the customer?
- Direction of naming: who names whom (Step 4).

Outcome: shown, not shown (say what was checked), or unresolved (say what would resolve it).

Also check the acquirer's same-week earnings call coverage and the press release for synergy framing.
Synergies from capacity rationalization, plant consolidation, pricing or go-to-market overlap are
admissions of horizontal proximity. A slide showing combined share or "#1 in X" is among the strongest
overlap evidence there is. Quote it.

## Step 4: the competitor check runs in both directions

- Outbound: quote each party's Competition section verbatim via `extract-10k` (or `edgar-filing-text`
  with `summary=true`, then the Competition offset). State plainly when a filing names no one; that is
  usually a drafting choice, not proof of an undefinable market.
- Inbound: pull the Competition sections of up to three plausible public peers and check whether they
  name either party. A rival naming your party is a statement against interest, made before the deal;
  weigh it at least as heavily as a self-listing.
- Adjacency: `entity-neighbors` (hops 1, rel_types such as CO_MENTIONED_WITH, MENTIONS, IN_INDUSTRY) or
  `graph-search` (entity = ticker, query on competitors, hops 1 to 2) for candidate peers. Co-occurrence
  is not a naming; never present it as a disclosure.
- Sellside lists: `semantic-search`, namespace `default`, document_type in Initiation of Coverage and
  Sellside Note, query naming the specific product line. Often the only source for private competitors.
- Reconcile, do not merge. Names on both parties' lists are the clearest evidence of a shared market;
  say so explicitly, after resolving parent and subsidiary aliases. A party naming nobody while several
  analysts name the same rivals implies a real, narrower market. A name in every analyst list and no
  filing is usually a significant private player. A name in filings but no current coverage may have
  exited; check.
- Resolve every peer's ownership with an `edgar-filings` or `edgar_company_facts` lookup before writing
  public, private, or sponsor-owned. Silence in a note is not "private". On a sponsor deal, a competitor
  in the sponsor's portfolio is the overlap.
- When there is time, diff the last three 10-Ks per party: names added, dropped, unchanged. Watch for
  stale or out-of-order filings from delinquent filers.
- An empty inbound check is a finding only if it ran: "no filer among the N screened names the target".

## Step 5: market definition and concentration

- For every line with real apparent overlap, run a narrow-versus-broad sensitivity: name the narrow
  market (one channel, protocol, customer tier), name the broad one, say which is economically right and
  why (customer type, channel, trade size, protocol), and say whether the narrow one would change the read
  if a regulator insisted on it. Never land on the broad market silently.
- Never estimate, compute or invent shares, HHI or probabilities. Compute share only when both the
  revenue figure and the total market come from citable sources; HHI only with sufficient participant
  data. Otherwise write the gap.
- If no deal-specific share exists, search once for the acquirer's or target's closest prior deal in the
  same line; a research shop's HHI table from that deal may serve as a labeled proxy, cited to its own
  transaction and date.
- Analyst share estimates carry across attributed (firm, note, date) and labeled as estimates. If two
  disagree, report both.

## Step 6: prior cooperation

Separately from naming, check whether the parties have operated as partners: joint ventures, liquidity
or order-flow pools, licensing, data sharing, distribution, reseller or integration agreements. Search
prior 8-Ks, press releases and trade press. State the finding positively or negatively with dates.
Behavioral cooperation weighs against a naming-based overlap; a 10-K naming does not preclude a JV.

## Step 7: vertical, interface and information theories

- Where the target is a system of record or platform others integrate with, list the named third-party
  integrations the buyer could degrade: system, owner, whether the owner is a buyer rival, public evidence
  (partner listing, release). This turns "foreclosure" into what a pre-notification questionnaire asks,
  identifies likely complainants, and tells you where they will complain.
- Access to rivals' confidential information: if the target supplies, hosts data for, or services the
  buyer's competitors, the combined firm would see their pricing, roadmaps or customer data. Note whether
  the target hosts customer data at all; if not, the theory is weak.
- Input foreclosure and customer foreclosure: say which party sells into the other's rivals and whether
  alternatives exist (few and concentrated versus many and established).

## Step 8: litigation cited as market evidence

Any suit, agency complaint or arbitration cited as evidence of market power gets a dated disposition
check: `docket-search` and `docket-details` by caption or number, caption plus "settlement" or "dismissed",
and both parties' later 8-Ks. Aggregators show "pending" long after resolution. State the disposition
beside the citation. A settlement via licensing or interoperability commitments usually cuts against a
foreclosure theory.

## Step 9: the merger agreement shows what the parties fear

Read these clauses one by one; each is negotiated evidence of perceived risk.

- Efforts standard: reasonable best efforts versus hell or high water; whether divestiture duty runs
  both ways.
- Divestiture cap: unlimited, a materiality standard, a dollar or revenue cap, or "except as set forth on
  Section X of the Parent Disclosure Schedule", which signals a pre-agreed confidential remedy basket and
  that the parties mapped the problem assets before signing.
- Burdensome Condition definition: quote it. It is the real ceiling on what the buyer must give up.
- Litigation commitment: defend through final non-appealable judgment, or weaker.
- Remedy-proffer deadline and pull-and-refile rights: compute dates.
- Antitrust reverse fee: say whether it is regulatory-specific or generic, state the percentage with its
  base, and benchmark against the conventional 3 to 4% of EV. Well above signals perceived risk; absent
  or low signals the parties saw a clean path.
- Interim standstills naming product spaces the parties may not acquire in: quote verbatim. Counsel's
  list of sensitive markets is often the best day-one market-definition evidence.
- Which regimes are closing conditions versus covenants only; only conditions can block.

## Step 10: enforcement posture

State the current posture of the gating agency as its own dated, sourced finding: a speech, a recent
challenge or clearance pattern, an ArbJournal roster entry (see precedents-and-sources.md). Note that it
is time-sensitive. Never treat posture as a background assumption.

## How to conclude

Rate three questions separately, LOW, MODERATE or HIGH, no percentages:

1. Second request risk (first-review exit, possibly after a refile).
2. Timing risk (second request, foreign or investment-screening filings, sector approvals). Parallel
   foreign filings that will likely clear belong here, not in the challenge read.
3. Challenge or remedy risk, which stays LOW unless an overlap was shown in Step 3.

Overall completion risk comes from 1 and 3. Never let a timing concern lift the challenge rating, or a
clean challenge rating hide a timing problem.

Before locking, write the best sourced case for one level lower and one level higher, and search for the
evidence that would move you either way if you have not. Test every disagreeing note: attribute it, name
the mechanism it relies on, check that mechanism in a primary source, then say whether you agree, disagree
or move. A tested claim outranks any sell-side tier. Close with a stress-test line: the fact that most
supports the verdict, the fact that most cuts against it, and which you weighted and why.

## Common errors

- Treating a 10-K competitor listing as a proven overlap, or "neither names the other" as proof of none.
- Screening segments instead of products, and missing the buyer's separately branded acquired units.
- Diffing two competitor lists by eye and missing names on both.
- Writing "private" without an EDGAR lookup.
- Quoting graph adjacency as if a company named another.
- Inventing a share or HHI, or calling a market-extension HHI "unavailable".
- Anchoring on the buyer's one memorable second request instead of its whole record by overlap type.
- Citing a lawsuit as live evidence after it settled.
- Writing internal labels ("gated", "sector-gate") into the deliverable instead of naming the regulator
  and its effect on the closing date.
