# Foreign merger-control jurisdictional thresholds — EC / UK CMA / SAMR / ACCC / Canada

The encoded domain knowledge behind Section E.1's "Foreign merger control" row. Before this file
existed, that row was a bare label — "EC / CMA / SAMR / other — or explicit absence from Article
VII" — with no test behind it, which meant the analyst either skipped it or guessed. Every entry
below answers the same three questions, because those are the three the row needs:

1. **What is the actual jurisdictional test** — the statute's own threshold, not a rule of thumb.
2. **What data does applying it require** — which figure, for which party, in which currency.
3. **How do you apply it to the deal in front of you** — where the data comes from and what
   conclusion to write down.

**Use these as the default and verify live.** Every regime below has moved its own thresholds at
least once in the last two-to-three years — that is the normal pace of change for this kind of
rule, not a sign these numbers are unusually unstable. Confirm the regulator's own current guidance
before finalizing a notifiability conclusion, the same discipline `references/regulatory-clocks.md`
already asks for on sector regulators. What this file buys you is that you are verifying a specific,
already-identified number rather than discovering from scratch that the regime exists and has a
threshold at all.

**This is a jurisdiction screen, not a substantive review.** Clearing (or missing) a threshold only
tells you whether a filing is required — it says nothing about whether that regulator would clear,
condition, or block the deal. Section D's competitive-effects analysis and Section E.2's Approval
Clock Build still carry the substantive and timing analysis; this file only answers "does this
regulator have to see the filing at all."

## Contents

- [EU Merger Regulation (EUMR)](#eu-merger-regulation-eumr)
- [UK Competition and Markets Authority (CMA)](#uk-competition-and-markets-authority-cma)
- [SAMR — China](#samr--china)
- [ACCC — Australia](#accc--australia)
- [Canada — Competition Act](#canada--competition-act)
- [Canada — Investment Canada Act](#canada--investment-canada-act)
- [Applying this file to a deal](#applying-this-file-to-a-deal)

---

## EU Merger Regulation (EUMR)

**The test (EUMR Article 1).** A transaction has "EU dimension" — and mandatory pre-closing
notification to the European Commission — if **either** of two turnover tests is met:

- **Test 1.** Combined worldwide turnover of all parties exceeds **€5 billion**, AND at least two
  of the parties each have EU-wide turnover exceeding **€250 million**.
- **Test 2 (the "3-state" test).** Combined worldwide turnover of all parties exceeds **€2.5
  billion**, AND combined turnover in at least **three EU member states** exceeds **€100 million**
  in each of those three states, AND at least two parties each have turnover exceeding **€25
  million** in each of those same three states, AND at least two parties each have EU-wide turnover
  exceeding **€100 million**.

**The carve-out that reverses a "yes."** Even where Test 1 or Test 2 is met, the transaction is
**not** notifiable to the Commission if each party earns more than **two-thirds of its EU-wide
turnover within one and the same member state** — the deal is treated as a national matter for that
state's own regulator instead. This is a real reversal, not a technicality — it comes up whenever
one or both parties are heavily domestic within a single large EU market (commonly Germany or
France), and skipping it produces a false "EC-notifiable" conclusion.

**What data this requires.** Worldwide turnover, EU-wide turnover, and (only if Test 1 fails)
per-member-state turnover, for each party — the prior fiscal year, calculated per the Commission's
own turnover-calculation rules (which include group-wide turnover, not just the notifying entity's
own).

**Applying it.** Pull each party's geographic revenue breakdown from its own EDGAR 10-K segment
disclosure (Section C already requires extracting this) — most US filers break out revenue by
broad region (e.g., "Europe," "EMEA") rather than the EU specifically, so state that gap explicitly
if a true EU-only figure isn't disclosed and use the broader regional figure as a labeled
upper-bound proxy rather than silently treating it as EU turnover. For a foreign party, use its home
filing's equivalent segment disclosure. Run Test 1 first (it needs no member-state breakdown); only
attempt Test 2 if Test 1 fails and country-level detail is actually available. State one of:
**notifiable** (name the test met and the figures), **not notifiable** (name which test failed and
by how much, or that the two-thirds carve-out applies), or **indeterminate — data gap** (name
exactly which figure is missing, e.g. "target's EU-wide turnover is not broken out from its EMEA
segment in the 10-K").

---

## UK Competition and Markets Authority (CMA)

**Three independent jurisdictional tests**, current as of the January 1, 2025 threshold increase —
meeting any one of them gives the CMA jurisdiction:

- **The turnover test.** The target's UK turnover exceeds **£100 million** (raised from £70 million
  effective January 1, 2025).
- **The share of supply test.** The merger creates or enhances a combined share of **25% or more**
  of the supply of goods or services of any description in the UK (or a substantial part of it)
  where the parties overlap — this is a share-of-supply test, not a formal market-share/HHI
  calculation, and the CMA has wide discretion in how it defines the relevant "description of
  goods or services." **New safe harbor** (also effective January 1, 2025): the share of supply
  test does **not** give the CMA jurisdiction if each party's own UK turnover is **£10 million or
  less** — a genuinely small UK-turnover target can clear a 25%+ combined share and still fall
  outside CMA jurisdiction.
- **The hybrid test (new).** Added alongside the 2025 threshold changes specifically to reach
  non-horizontal and potential-competition deals that the other two tests miss: jurisdiction attaches
  if one party has **at least 33% share** of a UK product category and **UK turnover exceeding
  £350 million**, and the *other* party merely has a **"UK nexus"** — a UK-incorporated entity, UK
  business activity, or UK customers — with **no horizontal overlap required at all**. This is the
  test most likely to catch a vertical or adjacent-market deal that a generalist read would wave
  through as "no UK antitrust issue."

**What data this requires.** UK-specific turnover for the target (turnover test); each party's UK
turnover and a reasoned view of combined share within the relevant supply category (share of supply
test); the larger party's UK market share and UK turnover, plus confirmation of the smaller party's
UK presence in any form (hybrid test).

**Applying it.** UK turnover is rarely broken out as its own line in a US filer's 10-K — most report
"Europe" or "EMEA" — so treat a UK-specific figure as frequently unavailable from EDGAR alone; note
the gap and, where the deal is UK-material, flag that a primary-source UK filing (Companies House
accounts) or the parties' own merger-notice filing would be needed to close it. State the same three-
way conclusion as the EUMR entry — notifiable / not notifiable / indeterminate — data gap — and name
which of the three tests drove the call. **Verify live**: the CMA updated its merger procedure
guidance again in November 2025, only months before this file was written — reconfirm the current
guidance rather than assuming the January 2025 figures above are still the latest word.

---

## SAMR — China

**The test.** Mandatory pre-closing filing with the State Administration for Market Regulation is
required where **both** of the following are met (thresholds effective January 26, 2024, roughly
20% above the levels they replaced, which had been unchanged for 15 years):

- **Combined-turnover limb.** Either the combined **worldwide** turnover of all parties exceeds
  **RMB 12 billion** (~US$1.7 billion), **or** the combined turnover of all parties **within China**
  exceeds **RMB 4 billion** (~US$568 million).
- **Individual-party limb.** At least **two** of the parties each have turnover **within China**
  exceeding **RMB 800 million** (~US$114 million).

**The discretionary call-in.** SAMR retains authority to review a transaction that falls **below**
these thresholds if it has reason to believe the deal may have the effect of eliminating or
restricting competition. A "thresholds not met" conclusion is therefore a jurisdictional-filing
conclusion, not a guarantee SAMR has no interest — say so explicitly rather than treating a
below-threshold deal as categorically outside SAMR's reach.

**What data this requires.** Worldwide turnover for the combined-turnover limb; China-specific
turnover for both limbs, for each party.

**Applying it.** China-specific revenue is commonly disclosed as its own line or a readily
identifiable component of an "Asia" or "Asia-Pacific" segment in a US filer's 10-K — check
specifically for a China breakout before falling back to a broader regional figure as a proxy. State
the three-way conclusion, and where thresholds are not met, add the discretionary-call-in caveat as
its own sentence rather than folding it into "not notifiable."

---

## ACCC — Australia

**The test.** Australia's merger regime became **mandatory** on January 1, 2026 (previously
voluntary), and runs on **monetary thresholds only — there is no market-share or concentration
test**. Notification is required if **either** of two limbs is met:

- **The "large merger" limb.** Combined Australian revenue of the merger parties is **at least
  A$200 million**, AND **either** the target's Australian revenue is **at least A$50 million**
  **or** the global transaction value is **at least A$250 million**.
- **The "very large acquirer" limb.** The acquirer group's Australian revenue is **at least A$500
  million**, AND the target's Australian revenue is **at least A$10 million** — this limb exists
  specifically to catch a large acquirer taking a small target, where the large-merger limb's
  combined-revenue test might not be met on the target side alone.

**The creeping-acquisition rule.** Acquisitions in the **same sector over a rolling three years**
are aggregated toward these thresholds (with certain prior acquisitions excluded from the
calculation per ACCC guidance) — directly relevant to a PE roll-up sponsor making repeated small
add-on acquisitions in one sector, where no single deal would meet the thresholds on its own but the
rolling total does. Screen for this explicitly on any serial-acquirer or roll-up-strategy deal.

**A separate, lower band for asset acquisitions** (as opposed to share/entity acquisitions) phases in
**April 1, 2026** — note this as a forward date rather than assuming the share-acquisition
thresholds above apply uniformly to an asset deal.

**What data this requires.** Australian-specific revenue for both parties; global transaction value;
for a roll-up sponsor, the sector-level history of prior same-sector Australian acquisitions in the
trailing three years.

**Applying it.** Australian revenue is rarely its own line in a US 10-K — check for an
"Australia"/"APAC" breakout and treat a broader Asia-Pacific figure as a labeled proxy if that's all
that's disclosed. State the three-way conclusion, naming which limb (if any) was met, and flag
explicitly if a roll-up fact pattern makes the creeping-acquisition rule the actual live question
rather than this single transaction viewed in isolation.

---

## Canada — Competition Act

**The test.** Mandatory pre-closing notification requires **both** of the following (2026
thresholds; the transaction-size figure has been held flat since 2021 rather than adjusted annually,
which is itself worth noting as a live-verify item):

- **Size-of-transaction threshold.** The target's assets in Canada, or the gross revenues from
  sales in, from, or into Canada generated from those assets, exceed **C$93 million**.
- **Size-of-parties threshold.** The combined assets in Canada, or combined gross revenues from
  Canadian sales, of all parties to the transaction and their affiliates exceed **C$400 million**.

**Both thresholds must be met — this is the most common error point.** A deal with two very large
parties (easily clearing the C$400m party-size test) but a small Canadian target (falling short of
the C$93m transaction-size test) is **not** notifiable, and vice versa. Do not treat either threshold
alone as sufficient; state both figures and both conclusions explicitly.

**What data this requires.** The target's Canadian assets or Canadian-sourced revenue (transaction
size); combined Canadian assets or revenue across all parties and their affiliates (party size).

**Applying it.** Treat this as its own row separate from the Investment Canada Act entry below — one
is a competition-law filing, the other a foreign-investment review, and a deal can trip one, both, or
neither. Canadian revenue is infrequently broken out on its own in a US 10-K (often folded into a
broader "North America" segment); flag the gap where it exists rather than estimating. State the
three-way conclusion against both thresholds together.

---

## Canada — Investment Canada Act

**This is a distinct review from the Competition Act above — a foreign-investment net-benefit
review, not a competition-law filing — and needs its own conclusion, not a shared one.** A
transaction can be reviewable under the Investment Canada Act, the Competition Act, both, or
neither, independently.

**The net-benefit review thresholds (2026), which vary sharply by investor type:**

- **WTO investor (private sector), direct acquisition of control of a non-cultural Canadian
  business:** reviewable above **$1.452 billion** in enterprise value.
- **State-owned enterprise (SOE) investor that is also a WTO investor:** a materially lower
  threshold, **$578 million** in asset value.
- **Trade-agreement-country investor** (an investor from a country party to CUSMA, CPTPP, CETA, or
  a similar agreement Canada has designated): a **higher** threshold than the general WTO figure,
  **$2.179 billion** in enterprise value.
- **Non-WTO investor:** far lower thresholds — **$5 million** in asset value for a direct
  acquisition, **$50 million** for an indirect one (e.g., acquiring a non-Canadian parent that holds
  a Canadian subsidiary).

**Part 4 national security review — no monetary floor, ever.** Separately and unconditionally from
every threshold above: **any** investment by a non-Canadian, **regardless of size**, can be called in
for national security review at the discretion of the responsible Minister (and ultimately the
Governor in Council). This is not a fourth tier of the net-benefit thresholds — it is a categorically
different, size-independent gate, and should be stated as its own unconditional line in the memo
rather than nested under the net-benefit figures above. A small deal that clears every net-benefit
threshold by a wide margin can still face a national security review if the target's business (data,
critical infrastructure, sensitive technology, proximity to government) draws that scrutiny.

**What data this requires.** Enterprise value or asset value of the transaction; the acquirer's
investor classification (WTO private-sector / SOE / trade-agreement-country / non-WTO) — which
determines which threshold applies and can materially change the answer; whether the target's
business touches a sector that draws heightened national-security attention (defense, critical
minerals, sensitive data, critical infrastructure) regardless of deal size.

**Applying it.** Classify the acquirer's investor type first — this is the single biggest driver of
which threshold applies, and getting it wrong (e.g., treating an SOE as an ordinary WTO investor)
changes the answer by roughly 2.5x. State the enterprise or asset value against the correct
threshold for a net-benefit conclusion, and separately and explicitly address the unconditional
national-security question — "no net-benefit review triggered; national security review remains
possible at ministerial discretion regardless of deal size, and nothing in the target's business
profile flags heightened risk" is a complete, honest answer even when the net-benefit thresholds
are not met.

---

## Applying this file to a deal

For each of the six regimes:

1. **Pull the specific revenue/turnover figures the regime's own test needs** — worldwide, EU-wide,
   UK, China, Australian, or Canadian, per party — from each party's EDGAR 10-K segment disclosure
   (Section C already requires extracting geographic revenue) or, for a foreign party, its home
   filing's equivalent. State plainly which figures are directly disclosed versus which had to be
   approximated from a broader regional bucket, and label any approximation as a proxy.
2. **Apply the regime's specific test** exactly as stated above — note which sub-test or limb was
   used, since several regimes (UK CMA, ACCC, Canada) have more than one independent path to
   jurisdiction and a deal can trip one without tripping another.
3. **Write a reasoned conclusion for each regime**: **notifiable** (name the test and the figures
   that met it), **not notifiable** (name the test and by how much it fell short, or which carve-out
   applies), or **indeterminate — data gap** (name the specific missing figure). Never default to a
   vague "foreign merger control may apply" — that sentence is what this file exists to replace.
4. **Feed the notifiable regimes into Section E.1's "Foreign merger control" row and, where a
   regime is notifiable, into Section E.2's Approval Clock Build** — a notifiability conclusion
   without a timing entry stops halfway.
5. **Re-verify the thresholds themselves against the regulator's own current guidance** before
   finalizing — every regime above has moved its thresholds within the last two-to-three years, and
   several (UK CMA, ACCC) are still in active transition as of this file's writing.
