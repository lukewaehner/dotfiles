# Meteora SPAC LOI — Master Clause Library

This is the source of truth for LOI generation. Every section below is the locked-in choice for Meteora's standard LOI template, drawn across the five reference LOIs in the project (American Tungsten, Trigg, Compute Labs, Unchained, SALT). Variables in `{CURLY_BRACES}` get filled at runtime.

Provenance comments after each section explain why the chosen version was picked, so you can defend it if the target pushes back.

---

## Header / Preamble

> **{SPONSOR_FULL_NAME}** ("**{SPONSOR_SHORT}**", "**we**" or "**us**") is pleased to submit this letter of intent ("**LOI**") for a proposed business combination transaction (the "**Transaction**", as further described below) between {SPONSOR_SHORT} and {TARGET_FULL_NAME} ("**{TARGET_SHORT}**", with {TARGET_SHORT} and {SPONSOR_SHORT} together referred to herein as the "**Parties**"). The proposed Transaction would allow the holders of equity securities of {TARGET_SHORT} (the "**Sellers**") to receive stock of {SPONSOR_SHORT}.
>
> {SPONSOR_SHORT} is an acquisition company formed for the purpose of consummating a business combination transaction with one or more businesses, and it currently has over ${TRUST_AMOUNT} in cash held in a trust account (the "**Trust Account**"). {SPONSOR_SHORT}'s securities are currently quoted on {EXCHANGE} marketplace, but are expected to be uplisted to {UPLIST_TARGET} prior to or in connection with the consummation of the Transaction (the "**Closing**").
>
> The proposed terms and conditions of the Transaction are described below. This LOI is non-binding except as specified below under "Binding LOI Provisions," and the proposed Transaction is subject to completion of satisfactory due diligence by {SPONSOR_SHORT} and the execution and delivery by the Parties of a definitive agreement for the Transaction satisfactory to all Parties (the "**Definitive Agreement**").

---

## Transaction

> A business combination between {TARGET_SHORT} and {SPONSOR_SHORT}, whose units, common stock and warrants are currently quoted on {EXCHANGE_SHORT} (the "**Exchange**") under the ticker symbols {UNIT_TICKER}, {COMMON_TICKER} and {WARRANT_TICKER}, pursuant to which {SPONSOR_SHORT} will directly or indirectly acquire 100% of {TARGET_SHORT}'s share capital (the "**Transaction**"). The precise legal transaction structure, including any pre-Closing reorganization, will be determined and mutually agreed by the Parties based on business, legal, tax, accounting and other considerations.
>
> **The Parties shall work together in good faith, with the assistance of their respective legal, tax and accounting advisors, to determine the transaction structure and related tax treatment for the Transaction. {TARGET_SHORT} shall cooperate in preparing and proposing potential tax structures for the Transaction, but no such structure shall be binding unless and until mutually agreed by the Parties. The final transaction structure shall take into account business, legal, tax, accounting and regulatory considerations of both Parties and shall be reflected in the Definitive Agreement.**
>
> In the event the transaction structure results in an entity other than {SPONSOR_SHORT} being the parent listed company, references in this term sheet to {SPONSOR_SHORT} will be deemed to mean such new parent company after Closing, as applicable.
>
> From and after Closing, the combined company will use the name and adopt a corresponding ticker symbol as determined by {TARGET_SHORT}.
>
> The total consideration provided to the Sellers (including holders of equity awards and other equity-linked securities) in the Transaction is expected to be the fully distributed pre-money Valuation described below less assumed debt, transaction expenses and the value of the shares of Class B common stock originally issued to its Sponsor (the "**Founder Shares**") at Closing (at $10.00 per share), to be refined after initial marketing and calculated on a fully-diluted basis using treasury stock methodology (the "**Transaction Consideration**"), based on the initial assumptions below. Accordingly, the Transaction Consideration will consist of shares of {SPONSOR_SHORT}'s common stock, at $10.00 per share, issued to the Sellers at Closing (the "**Share Consideration**").
>
> Unvested, out-of-the-money {TARGET_SHORT} convertible securities at Closing will be assumed by {SPONSOR_SHORT} and will reduce the Share Consideration otherwise payable to the Sellers based on a Black-Scholes valuation or other approach as mutually agreed by the Parties. All other vested and in-the-money convertible securities will be deemed to be outstanding and form part of the Share Consideration.

> *Provenance:* Tax structure language is BIXI's "Parties cooperate in good faith" formulation. Convertible-securities reduction-via-Black-Scholes from IVCB family — preserves sponsor optionality on out-of-the-money instruments.

---

## Board of Directors

> Upon Closing, we would expect the board of directors of {TARGET_SHORT} to consist of (i) the required number of independent directors per Securities and Exchange Commission ("**SEC**") and {EXCHANGE_SHORT} rules (with such independent directors to be selected by {TARGET_SHORT} and consented to by {SPONSOR_SHORT}, such consent not to be unreasonably withheld), (ii) **one (1) director shall be designated by {SPONSOR_SHORT} (the "{SPONSOR_SHORT} Designee")**, and (iii) the remainder shall be designated by {TARGET_SHORT}; provided that (i) the board will be structured as a classified board, and (ii) {TARGET_SHORT} shall allocate the directors into classes at their discretion. {TARGET_SHORT} will (a) enter into customary indemnification agreements with the members of the board of directors and (b) obtain (or maintain) customary D&O insurance, including tail coverage for the former directors and officers of {SPONSOR_SHORT}.

> *Provenance:* BIXI family — sponsor gets one designated board seat. Plus SPAC consent on independent director selection, classified board (entrenches), and tail D&O coverage required.

---

## US Listing

> In conjunction with the proposed Transaction, {SPONSOR_SHORT} will apply for listing on Nasdaq or NYSE American. The Parties acknowledge that final approval for listing is subject to the combined company's satisfaction of the applicable initial listing requirements. {SPONSOR_SHORT} will use commercially reasonable efforts to prepare and submit all necessary applications and documentation in a timely manner, and to work collaboratively with {TARGET_SHORT} to respond to any Nasdaq or NYSE American comments or conditions to listing approval. Prior to Closing, {SPONSOR_SHORT} shall use commercially reasonable efforts to cause its common stock to be relisted on the {INTERIM_MARKET} from the {CURRENT_OTC_TIER}.

> *Provenance:* IVCB family — concurrent uplist to Nasdaq or NYSE American. Variable `{INTERIM_MARKET}` defaults to "OTC Pink Market" and `{CURRENT_OTC_TIER}` defaults to "OTC Expert Market"; if sponsor is already on Nasdaq, drop the second sentence entirely.

---

## Timing

> This LOI and the proposed terms of the Transaction are based on {SPONSOR_SHORT}'s analysis of provided information. {TARGET_SHORT} or {SPONSOR_SHORT} have not conducted any substantive business, legal, financial, tax, regulatory or other due diligence to date.
>
> However, subject only to prompt satisfaction of our diligence requests and a customary negotiation process, we believe that we can complete our due diligence and enter into a Definitive Agreement no later than the expiration of the Term of this LOI (as defined below under "Term").

---

## Valuation

> Based on the information available to us at this time, and subject to completion of due diligence by {TARGET_SHORT} and {SPONSOR_SHORT} and its advisors satisfactory to {SPONSOR_SHORT} **in its sole discretion**, the total pre-money enterprise value ascribed to {TARGET_SHORT} for purposes of the Transaction will be ${VALUATION} ("**Valuation**"). The Valuation reflects commercial discussions to date and does not constitute a formal valuation or fairness opinion.
>
> The Parties acknowledge that the Valuation is subject to change following due diligence. A fairness opinion may be obtained from an appropriately qualified U.S. financial advisor to support the financial terms of the Transaction if so required by either or both Parties.
>
> The Share Consideration to be received by Sellers will be based on the Valuation, subject to adjustment for redemptions, PIPE proceeds, Transaction expenses and other dilution.

> *Provenance:* IVCB family — "satisfactory to {SPONSOR} in its sole discretion." Fairness opinion is *optional* (IVCB) rather than mandatory.

---

## Lock-Up and Registration Rights

> The Founder Shares of {SPONSOR_SHORT} held by the Sponsor and its independent directors will not be transferable for a period of six months after Closing, subject to customary exceptions. **Any Founder Shares transferred to support a PIPE or non-redemptions will be released from lock-up at Closing**, subject to any registration requirements.
>
> The lock-up period for shares of New {TARGET_SHORT}'s common stock issued in the Transaction to the officers, directors and **5%+** stockholders of the Sellers shall be on terms no more restrictive, in the aggregate, than those applicable to the Sponsor, subject to customary exceptions. Any such lock-up will be mutually agreed by the Parties after finalization of the Transaction holding structure and initial feedback from potential investors, and before signing the Definitive Agreement, but in no event will be sooner than for the Founder Shares of {SPONSOR_SHORT} held by the Sponsor.
>
> The shares of New {TARGET_SHORT}'s common stock issued in the Transaction to Sellers holding less than 5% of {TARGET_SHORT}'s shares other than {TARGET_SHORT}'s officers and directors will have no lock-up at Closing.
>
> {SPONSOR_SHORT} will amend and restate the registration rights agreement entered into in connection with its initial public offering (the "**IPO**") to provide registration rights to the Sellers, the Sponsor and {SPONSOR_SHORT}'s independent directors (and their respective permitted transferees) requiring New {TARGET_SHORT} to register the resale of the shares of New {TARGET_SHORT}'s common stock issued in the Transaction pursuant to a shelf registration statement to be filed with the SEC within 30 days after Closing.

> *Provenance:* BIXI family on the 5% threshold (broader sweep than IVCB's 10%). Founder share PIPE/NRA carve-out is universal across all five LOIs.

---

## Founder Share Haircut (2/3 conversion to warrants)

> As a condition to the Transaction, {SPONSOR_SHORT} shall cause **66.67% (two-thirds)** of the Founder Shares to be converted into cash-exercisable warrants (the "**Converted Warrants**"), exercisable for shares of New {TARGET_SHORT} common stock at varying strike prices and pursuant to terms and conditions mutually agreed in the Definitive Agreement. Such Converted Warrants shall be issued to the holders of the Founder Shares and/or their designees and may be used for future capital raising purposes by New {TARGET_SHORT}. The remaining **33.33% (one-third)** of the Founder Shares shall be retained by the Sponsor and its designees, subject to the lock-up and registration rights provisions set forth above and any commitments previously made in connection with non-redemption agreements or extension financings.

> *Provenance:* The five reference LOIs use either 68.87% (IVCB family) or 10% (BIXI family) for founder share haircut. **Meteora's house standard is 2/3 (66.67%) — slightly more sponsor-friendly than IVCB's 68.87% but well within the IVCB-family band.** The 1/3 retained block is what the sponsor walks away with as promote.

---

## Public Warrants Treatment

> The Parties agree that, subject to compliance with applicable securities laws, the public warrants of {SPONSOR_SHORT} (currently trading under the symbol {WARRANT_TICKER}) **will not be listed or quoted for trading on any national securities exchange or over-the-counter market following the consummation of the Transaction**. The warrants will remain outstanding in accordance with their existing terms, and any modifications thereto shall be mutually agreed by the Parties and reflected in the Definitive Agreement. The treatment of all public and private warrants of {SPONSOR_SHORT} shall be set forth in the Definitive Agreement.

> *Provenance:* IVCB family — public warrants delisted post-Closing. Removes a layer of public-market overhang and simplifies the post-Closing cap structure.

---

## PIPE

> In connection with the Transaction, {TARGET_SHORT} may seek to raise additional capital through a private investment in public equity ("**PIPE**") financing. The size, structure, and terms of the PIPE have not yet been determined and will be subject to market conditions, investor feedback, and mutual agreement of the Parties. **The Parties may mutually agree** to engage a PIPE Placement Agent to assist in sourcing and structuring the PIPE financing. {SPONSOR_SHORT} agrees to reasonably cooperate with {TARGET_SHORT} and the PIPE Placement Agent in connection with the PIPE process. The size, pricing and structure of any PIPE, as well as non-redemption agreements and transaction expenses will affect {TARGET_SHORT}'s equity ownership at Closing and over time.

> *Provenance:* BIXI family — "**may** mutually agree" to engage placement agent (no obligation to engage). Silent on disclosure of PIPE inducements / NRA economics to target — sponsor-flexibility default.

---

## Minimum Cash Condition

> **The Parties acknowledge and agree that the Transaction shall not be subject to a minimum cash condition.** {SPONSOR_SHORT} shall be entitled to consummate the Transaction regardless of the level of redemptions by its public stockholders or the amount of proceeds, if any, raised through any PIPE financing, convertible note financing, or other equity or debt financing in connection with the Transaction.

> *Provenance:* Unchained LOI — explicit no-minimum-cash position. The added second sentence makes the position explicit and forecloses target arguments at the Definitive Agreement stage that any specific number is required. SPAC can close even at 100% redemption with no PIPE.

---

## LTIP (Long-Term Incentive Plan)

> It is anticipated that a new equity incentive plan (the "**LTIP**") pursuant to which New {TARGET_SHORT} may grant cash and equity incentive awards and compensation to officers, directors, employees and other eligible service providers will be approved and adopted in connection with Closing. The initial number of New {TARGET_SHORT} shares under the LTIP will be approximately **10%** of the outstanding shares of New {TARGET_SHORT}, based upon benchmarking against peer companies (taking into account the nature of the business of {TARGET_SHORT} as well as the fact that New {TARGET_SHORT} will be a publicly listed company).

> *Provenance:* IVCB family standard 10% — half the dilution of SALT's 20%.

---

## Definitive Agreement (minimal closing conditions, target-only MAC)

> The Definitive Agreement will include (i) representations, warranties, and covenants to be agreed upon by the Parties, and (ii) other terms and conditions customary for transactions similar to the Transaction.
>
> The conditions to Closing in the Definitive Agreement will include:
>
> - the approval of the Transaction by the Sellers;
> - the approval of the Transaction by the stockholders of {SPONSOR_SHORT};
> - the bring-down at Closing of representations and warranties and covenants **of {TARGET_SHORT}** to a customary standard;
> - **no material adverse change having occurred with respect to {TARGET_SHORT}**;
> - approval for listing of {SPONSOR_SHORT} shares on Nasdaq or NYSE American in the United States; and
> - other customary Closing conditions that are identified in the course of due diligence.
>
> The Definitive Agreement will be governed by the laws of the State of Delaware and the exclusive forum for any disputes under or relating to the Definitive Agreement shall be in the State of Delaware.

> *Provenance:* Stripped-down version of IVCB family. **Bring-down and MAC apply to target only — sponsor is not subject to a reciprocal condition.** Closing-conditions list is intentionally minimal: only stockholder approvals, target MAC/bring-down, listing approval, and the catch-all. Drops regulatory approvals, third-party approvals, Fairness Opinion, ancillary documents, no-orders, and no-prescribed-occurrences clauses (all of which appear in the IVCB family) — those expand at the Definitive Agreement stage.

---

## Financial Statements and Financial Information

> Promptly after execution of this LOI, the Parties' respective advisors will determine the nature and scope of the financial statements and financial information of {TARGET_SHORT} required to be included in the proxy/registration statement to be filed with the SEC in connection with the Transaction, and {TARGET_SHORT} will immediately commence whatever work is necessary to prepare or finalize such financial statements and financial information, and engage an appropriate independent auditor to audit the financial statements that are required to be audited.

> *Provenance:* IVCB family. No "minimize cost/disruption" softener — sponsor flexibility on financial work scope.

---

# Binding LOI Provisions

## Non-Exclusivity with Right of First Negotiation

> The Parties acknowledge and agree that, during the Term of this LOI, **{TARGET_SHORT} shall not be subject to any exclusivity obligations** in favor of {SPONSOR_SHORT}, and {TARGET_SHORT} and its Related Parties (as defined below) shall be free to engage in discussions, negotiations, and information exchanges with any third party concerning any potential acquisition of, investment in, financing of, or sale of any assets or equity or debt securities of {TARGET_SHORT} (each, a "**Competing Proposal**").
>
> Notwithstanding the foregoing, {TARGET_SHORT} agrees that, during the Term, in the event {TARGET_SHORT} receives a Competing Proposal that {TARGET_SHORT} or its board of directors is prepared to pursue or accept, {TARGET_SHORT} shall (i) promptly notify {SPONSOR_SHORT} in writing of the existence and material economic terms of such Competing Proposal (the identity of the proposing party may be withheld if subject to a confidentiality obligation), and (ii) **negotiate in good faith and exclusively with {SPONSOR_SHORT} for a period of ten (10) business days** following such notice (the "**Right of First Negotiation Period**") before entering into any binding agreement with the third party with respect to such Competing Proposal. During the Right of First Negotiation Period, {SPONSOR_SHORT} shall have the opportunity to revise or improve the terms of the Transaction set forth in this LOI in response to such Competing Proposal. If, following the Right of First Negotiation Period, {TARGET_SHORT} and {SPONSOR_SHORT} have not reached agreement on revised terms acceptable to {TARGET_SHORT}, {TARGET_SHORT} shall be free to enter into a binding agreement with the third party.
>
> For purposes of this LOI, "**Related Parties**" means, with respect to a Party, each of its subsidiaries, affiliates (including, to the extent applicable, parallel or subsequent investment funds or management vehicles) and each of its and their employees, agents, representatives, affiliates, equity holders and any other person or entity acting on its behalf.
>
> For the avoidance of doubt, no termination fee, break-up fee, or expense reimbursement shall be payable by either Party in connection with the termination of this LOI or the entry by {TARGET_SHORT} into any Competing Proposal, and neither Party shall be subject to any obligation to negotiate the Definitive Agreement in good faith or otherwise.

> *Provenance:* Custom-built per Meteora's spec. Replaces the standard 60-day exclusivity from all five reference LOIs. The 10-business-day Right of First Negotiation gives the sponsor a chance to match a competing offer without locking the target up. Termination-fee silence is preserved (per spec).

---

## Due Diligence Access

> Upon execution of this LOI and until this LOI expires, {TARGET_SHORT} shall allow {SPONSOR_SHORT} and its employees, agents and advisors **full and prompt access** to its facilities, records, key employees, suppliers and advisors for the purpose of conducting {SPONSOR_SHORT}'s due diligence review. The due diligence investigation may include, but is not limited to, financial modeling, a quality of earnings report, a review of {TARGET_SHORT}'s business plan and such review of the Company's commercial, financial, legal, tax, environmental, intellectual property and labor records and agreements and any other matters as {SPONSOR_SHORT} and {SPONSOR_SHORT}'s accountants, tax and legal counsel and other advisors may deem relevant or appropriate (**in each case in the sole discretion of {SPONSOR_SHORT}**). For the avoidance of doubt, nothing in the preceding sentence does or shall be deemed to obligate {SPONSOR_SHORT} or its advisors to conduct any due diligence other than diligence which {SPONSOR_SHORT} may, in its sole discretion, determine to conduct.

> *Provenance:* IVCB family — sole-discretion access. No BIXI-style "competitively sensitive / privileged / confidentiality" carve-outs that let target gate diligence requests.

---

## Management Availability

> Upon request by {SPONSOR_SHORT}, {TARGET_SHORT} agrees to make its management reasonably available to participate in a "testing the waters" process in order to determine general interest and market enthusiasm for the Transaction on the material terms and conditions contemplated by this LOI, as well as any investor meetings with potential investors in the PIPE.

> *Provenance:* IVCB family. No BIXI-style "subject to {TARGET}'s reasonable control over messaging" gating language.

---

## Choice of Law and Jurisdiction Matters

> This LOI shall be governed by the laws of the State of Delaware, without giving effect to its conflict of laws principles, provisions or rules which would require the application of any other law, and the Parties consent to the exclusive jurisdiction of the Delaware Court of Chancery (as well as to any courts to which an appeal may be taken from the Delaware Court of Chancery), for all disputes related hereto (or, if for any reason it shall be determined by such court that it does not have subject matter jurisdiction, any state or federal court in the State of Delaware). Each of the Parties expressly waives any and all objections it may have to venue, including without limitation, the inconvenience of such forum, in any courts. In addition, each of the Parties further agrees that service of any process, summons, notice or document by U.S. registered mail (or similar private providers of mail services) to such Party's respective primary address (including the address identified on the signature pages hereto) shall be effective service of process with respect to any matters brought hereunder. Each of the Parties (i) unconditionally waives any right it may have to a trial by jury in respect of any litigation or other proceeding directly or indirectly arising out of this LOI and (ii) agrees and covenants that it shall not seek in any manner to resolve any dispute other than as set forth in this section entitled "Choice of Law and Jurisdiction Matters".

> *Provenance:* Universal across all five LOIs.

---

## Confidentiality

> The Parties agree that this LOI and its contents constitute confidential information under, and shall be subject to, the terms of the Mutual Non-Disclosure Agreement, dated as of {NDA_DATE} (the "**Mutual Non-Disclosure Agreement**"), between {TARGET_SHORT} and {SPONSOR_SHORT}, as the same may be further amended or supplemented.

---

## Expenses

> Each Party will bear its own costs and expenses in connection with this LOI and the negotiation of the Transaction, including all fees and expenses of their representatives and advisors, regardless of whether the Parties enter into the Definitive Agreement. {SPONSOR_SHORT} shall either obtain a waiver from the underwriters in its IPO of any deferred compensation or shall negotiate suitable reductions in any amounts due and provide for the payment of such amounts in equity of New {TARGET_SHORT}.

> *Provenance:* "Each party bears own" formulation per spec — no commitment that target absorbs sponsor's expenses out of trust at close (different from IVCB family). Underwriter waiver/equity-reduction language preserved from IVCB family.

---

## Trust Account Waiver

> {TARGET_SHORT} hereby acknowledges that {SPONSOR_SHORT} has established a trust account (the "**Trust Account**") containing the proceeds of its IPO and from certain private placements occurring simultaneously with the IPO (including interest accrued from time to time thereon) for the benefit of {SPONSOR_SHORT}'s public stockholders (the "**Public Stockholders**") and certain other parties (including the underwriters of the IPO). For and in consideration of {SPONSOR_SHORT} entering into this LOI, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, {TARGET_SHORT} hereby agrees (on its own behalf and on behalf of its Related Parties) that it does not now and shall not at any time hereafter have any right, title, interest or claim of any kind in or to any assets held in the Trust Account, and shall not make any claim against the Trust Account, regardless of whether such claim arises as a result of, in connection with or relating in any way to this LOI or any other matter, and regardless of whether such claim arises based on contract, tort, equity or any other theory of legal liability (any and all such claims are collectively referred to hereafter as the "**Released Claims**"). {TARGET_SHORT} hereby irrevocably waives (on its own behalf and on behalf of its Related Parties) any Released Claims that it may have against the Trust Account now or in the future as a result of, or arising out of, any discussions, contracts or agreements with {SPONSOR_SHORT} and will not seek recourse against the Trust Account for any reason whatsoever.

> *Provenance:* IVCB family — broad waiver covering "any other matter," not BIXI's narrowing "for the sole purpose of this LOI."

---

## Term

> This offer to enter into this LOI shall expire by its terms on {OFFER_EXPIRATION} at 5:00 p.m. New York time (the "**Offer Expiration Time**"), unless prior to the Offer Expiration Time, this LOI shall have been accepted without modification and such acceptance has been evidenced by delivery to {TARGET_SHORT} of validly executed signatures by {SPONSOR_SHORT}. Upon signing by both Parties, this LOI shall become effective and shall expire on the earlier of (i) signing of the Definitive Agreement, (ii) **that date which is 60 days after the date on which the parties exchange signatures**, or (iii) written consent of all Parties (the "**Term**"); provided, however, that the provisions set forth under the heading "Binding LOI Provisions" (other than under "Non-Exclusivity with Right of First Negotiation," "Due Diligence Access" and "Management Availability") shall continue in full force and effect following the expiration hereof.

> *Provenance:* IVCB family on the 60-day fixed term. Survival carve-out updated to reference the new Non-Exclusivity section name.

---

## General Provisions

> No contract or agreement providing for any transaction involving {TARGET_SHORT} or the Sellers (or any other person) does exist (or shall be deemed to exist) between {SPONSOR_SHORT} (or any of its Related Parties), on the one hand, and {TARGET_SHORT} or the Sellers (or any other person), on the other hand, unless and until a Definitive Agreement has been executed and delivered, and none of the Parties or their respective Related Parties shall be obligated to engage in negotiations regarding, or to enter into any contract or agreement effecting, the Transaction. In furtherance of the foregoing and for the avoidance of doubt, but without limiting the enforceability of the "Expenses" provision above, no obligation shall be created by this LOI for any party to negotiate in good faith (or any other standard that may be applicable under law) and each of the Parties (on behalf of itself and each of its Related Parties) expressly waives and covenants not to sue in connection with the failure by any person to negotiate the transaction or the Definitive Agreement (whether in good faith or otherwise). Except as specifically set forth or referred to herein, nothing herein is intended or shall be construed to confer upon any person or entity other than the Parties and their successors or assigns, any rights or remedies under or by reason of this LOI. **This LOI is not assignable by {TARGET_SHORT}.** This LOI may be executed in counterparts, each of which shall be deemed to be an original, but all of which together shall constitute one agreement. The headings of the various sections of this LOI have been inserted for reference only and shall not be deemed to be a part of this LOI. This LOI contains the entire agreement of the Parties with respect to the subject matter hereof, and supersedes any and all prior agreements and understandings (other than the Mutual Non-Disclosure Agreement).

> *Provenance:* IVCB family — asymmetric assignment restriction (target only).

---

# Section-Selection Summary

| Section | Source | Per Meteora spec |
|---|---|---|
| Header / preamble | Hybrid | Standard |
| Transaction structure | BIXI tax language | Parties cooperate in good faith on tax |
| Board of Directors | BIXI | One Sponsor Designee |
| US Listing | IVCB | Nasdaq/NYSE American (uplist) |
| Timing | Universal | — |
| Valuation | IVCB | Sole discretion + optional fairness opinion |
| Lock-Up | BIXI | 5%+ threshold |
| Founder Share Haircut | **Meteora-custom** | **2/3 (66.67%) conversion** |
| Public Warrants | IVCB | Delisted |
| PIPE | BIXI | "May" engage placement agent |
| Min Cash Condition | Unchained-plus | **Explicit no min cash** |
| LTIP | IVCB | 10% |
| Definitive Agreement | Custom-light | Stockholder approvals + target MAC + listing only |
| Financial Statements | IVCB | No softener |
| **Exclusivity** | **Custom** | **Non-exclusive + 10-bd Right of First Negotiation** |
| Due Diligence Access | IVCB | Sole-discretion full and prompt |
| Management Availability | IVCB | Testing-the-waters mandate |
| Choice of Law | Universal | Delaware Chancery |
| Confidentiality | Universal | NDA cross-reference |
| Expenses | Custom | Each party bears own + underwriter waiver/equity reduction |
| Trust Account Waiver | IVCB | Broad |
| Term | IVCB | 60-day fixed |
| General Provisions | IVCB | Asymmetric assignment |

**Sections OMITTED from the standard LOI:**
- Shareholder Earnout (no dilutive shares to target)
- Termination Fee / break-up fee (silent)
- Fiduciary out / Superior Proposal carve-out (moot under non-exclusive)
- Post-Transaction Capital Structure exhibit / Exhibit A cap table
- Foreign-jurisdiction language (Australian scheme, FIRB, ATO, etc.)
- Convertible note add-on (only include if user explicitly requests)
- "Minimum Cash Condition / Convertible Note Financing" combined section — replaced with stand-alone explicit no-min-cash section

---

# Variables to fill at runtime

| Token | Description | Example |
|---|---|---|
| `{SPONSOR_FULL_NAME}` | Full legal name of SPAC | Investcorp Europe Acquisition Corp I |
| `{SPONSOR_SHORT}` | Defined short name | IVCB |
| `{TARGET_FULL_NAME}` | Full legal name of target | Compute Labs Incorporated |
| `{TARGET_SHORT}` | Defined short name | Compute Labs |
| `{SPONSOR_SIGNATORY_NAME}` | Person signing for sponsor | Vikas Mittal |
| `{TARGET_SIGNATORY_NAME}` | Person signing for target | Albert Zhang |
| `{TARGET_TITLE}` | Target signatory's title | Chief Executive Officer |
| `{TARGET_ADDRESS}` | Target's address (multi-line) | Suite 2, 68 Hay Street, Subiaco, WA 6008 Australia |
| `{TRUST_AMOUNT}` | Trust balance (with commas, no $) | 24,170,000 |
| `{EXCHANGE}` | Sponsor's current exchange | the OTC Expert Market |
| `{EXCHANGE_SHORT}` | Short form for clauses | the OTC Expert Market |
| `{UPLIST_TARGET}` | Where uplisting | the OTC Pink market |
| `{INTERIM_MARKET}` | Where to interim-list before Closing | OTC Pink Market |
| `{CURRENT_OTC_TIER}` | Where currently listed | OTC Expert Market |
| `{UNIT_TICKER}` | Unit ticker | IVCUF |
| `{COMMON_TICKER}` | Common stock ticker | IVCBF |
| `{WARRANT_TICKER}` | Warrant ticker | IVCWF |
| `{VALUATION}` | Pre-money valuation (with commas, no $) | 400,000,000 |
| `{LOI_DATE}` | Date of LOI | April 28, 2026 |
| `{OFFER_EXPIRATION}` | Date offer expires | May 8, 2026 |
| `{NDA_DATE}` | Date of mutual NDA | January 21, 2026 |
