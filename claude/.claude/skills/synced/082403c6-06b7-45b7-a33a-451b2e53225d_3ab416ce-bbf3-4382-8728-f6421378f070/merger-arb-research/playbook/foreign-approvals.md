# Foreign merger control and the geographic nexus screen

Load when: the target or buyer earns revenue outside the buyer's home market; the agreement names foreign approvals, refers to "certain other jurisdictions" or a confidential jurisdiction schedule, or defines "Competition Laws" to include foreign or FDI laws; a broker lists countries; the question is which foreign filings apply.

## Why it matters

A foreign filing the desk did not see coming can outlast HSR and become the gate, and a "perfunctory approvals" assumption hides that risk. Most foreign filings are mandatory and suspensory, so each one that applies is a clock in the close-date build. A confidential schedule is never the answer: derive the perimeter from public filings, bound what the filings cannot settle, and say which document will settle the rest.

This is a jurisdiction screen. Meeting a threshold tells you a filing is required and says nothing about whether the regulator will clear it; substance and timing belong in the overlap analysis and `regulatory-clocks.md`.

## What to check

- Revenue by geography for the last fiscal year and two prior years (10-K revenue and segment notes, latest 10-Q, MD&A, risk factors that name markets; use `extract-10k` or the EDGAR filing text). Quote the table and cite filing and page. A fast-growing market can cross a threshold the last filing did not.
- Legal entities by country (10-K Exhibit 21). A subsidiary establishes nexus and says nothing about revenue.
- Employees, offices and properties abroad (Item 1 human capital, Item 2 properties, lease notes).
- Users and personal data abroad (privacy notice, app-store availability, data-protection risk factors naming GDPR or UK GDPR).
- The buyer side's turnover, which depends on who controls the buyer. Regimes count the whole control group; for a fund-backed vehicle that can include the fund's controlled portfolio companies, while a passive minority LP is usually not counted. Until the control chain is documented, write "on present facts".
- The investor classification of the buyer (private, state-owned, trade-agreement country) for Investment Canada Act and FDI tests.
- The agreement's conditions article, "Competition Laws" definition and jurisdiction schedule reference. State which regimes condition closing versus appear only in a covenant.
- Broker and press country lists, tagged as leads. Test each against the ladder.

## The method

1. **Build the ladder.** One row per country or region: revenue ($M, source), % of total, change year on year, Exhibit 21 entity, local staff, local users or data. If the filing gives only "Rest of World", write that row, quote it, and do not allocate the bucket to countries.
2. **Run the ceiling test.** A country's revenue cannot exceed the bucket that contains it.
   - Threshold above the whole bucket: "Not notifiable on the turnover limb: threshold X exceeds the entire [bucket] revenue of Y." This is a bound.
   - Threshold below the bucket: "Cannot be excluded on the turnover limb: [bucket] revenue Y exceeds threshold X; country split needed."
   - Convert currency at a stated rate and date (or the regime's own conversion rule). Use the last completed fiscal year. Run the arithmetic in Python and print it.
   - Test the weaker party's leg first. Where a regime needs two parties above a local threshold and the buyer side has no local turnover, the regime fails there and the target's split is moot. This only holds once the buyer's control group is known. For a newly formed vehicle, the control group is whoever controls it (sponsor, investors, their portfolio companies), so until the control chain is documented write the conclusion "on present facts" and keep every regime the target alone qualifies for on the watch list. Regimes with a target-only limb (UK share of supply, deal-value tests) and all FDI regimes do not depend on buyer turnover at all.
   - Deal-value tests (Germany, Austria, India, Korea) turn on price plus substantial domestic operations. A modest local business and a large price can be caught.
3. **Screen regimes.** One row per regime that survives, plus the ones ruled out: test and limb, threshold with source and check date, ceiling result, conclusion, clock if filed, condition or covenant only. If the target names a market in its filings, run that market even if it is not in the table below.
4. **Run FDI and data hooks separately.** Competition regimes ask about turnover; FDI and national-security regimes ask about sector, entity, data and the buyer's ownership. See `national-security.md`. A regime where the target has no entity and no named customer is not a gate: write "no entity, no named customer".
5. **Gate test.** For each surviving regime say whether it is mandatory and suspensory, whether its clock could outlast the clock that sets the working close (a candidate second gate), and which public document will settle it and when (proxy or information statement regulatory section, Schedule 13E-3, first foreign filings, regulator case registers).

## How to conclude

For each regime write exactly one of:
- **Notifiable**: name the test and limb met and the figures.
- **Not notifiable**: name the test that failed and by how much, or the carve-out that applies.
- **Cannot be excluded**: the bucket exceeds the threshold and the country split is not public; name the missing figure.
- **Indeterminate, data gap**: name the exact missing figure (for example "target EU turnover not broken out from EMEA").

For the perimeter as a whole: **Resolved** when every regime has a conclusion from public figures; **Bounded** when named regimes, tests, figures and a watch list exist but some rows cannot be excluded; **Blocked** only for the exact contents of a confidential schedule, and only beside a Bounded perimeter. Close with an Assessment of two to four sentences: how many regimes cannot be excluded, whether any could outlast the SEC or HSR chain, and what resolves them.

## Reading the agreement against the perimeter

- Quote the "Competition Laws" or "Regulatory Laws" definition first. A definition that sweeps in foreign investment laws means FDI filings can be conditions even when no regime is named.
- Separate regimes that condition closing from those that appear only in a filing covenant. A covenant-only regime cannot hold the close, though a suspensory regime still binds the parties legally.
- Note any regime the statute or threshold makes mandatory but the agreement omits, and say so as a finding.
- Check efforts and outside-date language for any foreign-specific extension trigger (for example an extension that runs only while a named foreign approval is pending). It tells you which foreign clock the parties expect to be long.
- Check every broker country list against the ladder and the ceiling test; record which countries it adds, which it misses, and on what evidence.

## Reference data (verify live before relying on a number; thresholds move every few years; date-stamp what you used)

| Regime | Test | Notes |
|---|---|---|
| EU Merger Regulation | Test 1: combined worldwide turnover > €5bn and at least two parties each > €250m EU-wide. Test 2: combined worldwide > €2.5bn; combined > €100m in each of at least three member states; at least two parties each > €25m in each of those three; at least two parties each > €100m EU-wide | Two-thirds rule: not notifiable if each party earns more than two-thirds of its EU turnover in the same member state (goes national instead). Group-wide turnover counts. Run Test 1 first. EMEA or Europe figures are an upper-bound proxy, labelled as such |
| UK CMA | Turnover: target UK turnover > £100m. Share of supply: combined 25%+ of a description of goods or services, with a safe harbour where each party's UK turnover is £10m or less. Hybrid: one party has 33%+ share and UK turnover > £350m, and the other has any UK nexus, with no overlap required | Thresholds from 1 January 2025; procedure guidance revised again November 2025. Hybrid test catches vertical and potential-competition deals. UK turnover is rarely broken out; Companies House accounts can close the gap |
| China SAMR | Combined worldwide turnover > RMB 12bn, or combined China turnover > RMB 4bn; and at least two parties each > RMB 800m in China | Thresholds from 26 January 2024. SAMR can call in below-threshold deals; state that caveat as its own sentence |
| Germany | Combined worldwide > €500m; one party > €50m German turnover and another > €17.5m. Deal-value limb: price > €400m with substantial domestic operations | Generally no substantial domestic operations below €17.5m German turnover. A June 2026 government draft would raise thresholds to €750m, €75m and €20m; check its status |
| Austria | Combined Austrian turnover > €30m with two parties each > €1m (plus a worldwide combined limb; confirm). Deal-value limb: €200m with substantial domestic activity | Generally no substantial domestic activity below €1m Austrian turnover |
| Australia | Mandatory and suspensory from 1 January 2026. Large-merger limb: combined Australian revenue >= A$200m and either target >= A$50m or global transaction value >= A$250m. Very-large-acquirer limb: acquirer group >= A$500m and target >= A$10m | Monetary tests only. Same-sector acquisitions over a rolling three years aggregate (creeping rule; screen roll-ups). Lower band for asset acquisitions from 1 April 2026 |
| Canada, Competition Act | Size of transaction: target Canadian assets or revenue from them > C$93m. Size of parties: combined Canadian assets or revenue with affiliates > C$400m. Both must be met | Transaction-size figure held flat since 2021; verify. Separate row from the ICA |
| Canada, Investment Canada Act (net benefit) | Private WTO investor: C$1.452bn enterprise value. Trade-agreement investor: C$2.179bn. SOE WTO investor: C$578m asset value. Non-WTO: C$5m direct, C$50m indirect | 2026 figures. Classify the investor first; an SOE error moves the threshold about 2.5x. National-security review has no floor: see `national-security.md` |
| Japan (JFTC) | Acquirer group domestic turnover > JPY 20bn and target group domestic turnover > JPY 5bn (share acquisition crossing 20% or 50%) | Not confirmed in our sources; verify |
| South Korea (KFTC) | One party worldwide assets or turnover >= KRW 300bn and the other >= KRW 30bn, with local nexus; deal-value limb around KRW 600bn | Not confirmed in our sources; verify |
| Turkey | Combined Turkish turnover and two parties above individual Turkish thresholds, or target Turkish turnover plus other party worldwide turnover; technology-undertaking targets lose the local floor | Thresholds revised 2022; not confirmed in our sources; verify |
| France, Italy, Spain, Netherlands, Poland, Nordics | National turnover tests, some with call-in or deal-value elements | Pull current figures for any country the ceiling test did not rule out |
| Brazil, Mexico, Argentina, Chile, Colombia | Local turnover of two groups; mandatory and suspensory in most | Matters when the target has a Latin American business |
| India, Israel, South Africa | Local turnover; India has a deal-value test | Pull current figures for any market the target names |

## Common errors

- Writing "foreign approvals not public" or "per confidential schedule" and stopping.
- Allocating a Rest of World bucket across countries, or treating a broker's "strong in Europe" as a revenue figure.
- Treating EMEA revenue as EU turnover without labelling it a proxy.
- Skipping the EU two-thirds rule and calling a domestic-heavy deal EC-notifiable.
- Treating Canada's two Competition Act thresholds as alternatives; both must be met.
- Applying the private WTO ICA threshold to a state-owned investor.
- Calling a below-threshold SAMR deal categorically out of reach.
- Concluding "the buyer has no foreign turnover" before the control group is known.
- Missing deal-value tests where local revenue is small and the price is large.
- Stopping at a notifiability call without adding the regime's clock to the close-date build.
