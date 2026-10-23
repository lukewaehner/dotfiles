# Existing Instruments & Anti-Dilution Analysis

## Purpose

When a company does an exploding unit deal, the massive share issuance and price depression can trigger anti-dilution provisions in existing instruments. This reference covers how to identify, classify, and model the risk from pre-existing warrants, convertibles, and other resetting instruments.

---

## Where to Find Existing Instruments in SEC Filings

### Primary Sources (search in this order)

1. **Recent Developments / Prospectus Summary** — Usually within the first 30 pages. Look for:
   - "February 2026 Offering" or similar prior offering references
   - "Warrants" subsection describing prior warrant issuances
   - "Convertible notes" or "convertible securities"

2. **Financial Statements — Notes** — Typically in the back half of the filing:
   - Note on Shareholders' Equity / Stockholders' Equity
   - Note on Warrants
   - Note on Convertible Instruments
   - Note on Related Party Transactions (convertible loans from insiders)

3. **Capitalization Table** — Shows all outstanding instruments

4. **Risk Factors** — Often discloses dilution risk from existing instruments:
   - "substantial dilution" + "warrants" or "convertible"
   - "anti-dilution" provisions

5. **Description of Securities section** — Full legal terms of each instrument class

### Search Terms

Use these search terms in the filing to find all instruments:
- "warrant" / "warrants"
- "convertible" / "conversion" / "convert"
- "note" / "notes payable"
- "equity line" / "ELOC" / "SEPA" / "standby"
- "anti-dilution" / "ratchet" / "weighted average"
- "exercise price" + "adjustment"
- "reset" / "resets"
- "incentive plan" / "stock option" / "S-8"
- "rights" (from SPAC structures)

---

## Anti-Dilution Provision Types

### Type 1: Structural Anti-Dilution (LOW RISK)

**Language to look for:**
- "subject to appropriate adjustment in the event of stock dividends, stock splits, reorganizations or similar events"
- "proportional adjustment for subdivisions, combinations, reclassifications"

**What it means:** Strike price and share counts only adjust for mechanical corporate actions (splits, dividends, reorganizations). Does NOT adjust for new equity issuances at lower prices.

**Impact of new exploding unit deal:** NONE. The prior instrument's strike stays the same. If it's deeply underwater (strike >> current price), it's effectively dead unless the stock recovers.

**Risk level: LOW / GREEN**

### Type 2: Weighted Average Anti-Dilution (MEDIUM RISK)

**Language to look for:**
- "weighted average" + "anti-dilution"
- "the exercise price shall be adjusted to a price determined by dividing (x) an amount equal to the sum of..."
- "broad-based weighted average"
- "narrow-based weighted average"

**What it means:** Strike price adjusts downward based on a formula that accounts for the number of new shares issued and the price at which they were issued, weighted against the existing outstanding shares. The adjustment is moderate — the more shares outstanding before the new deal, the less the strike moves.

**Formula (broad-based):**
```
New Strike = Old Strike × (Shares Outstanding + (New Money / Old Strike)) / (Shares Outstanding + New Shares Issued)
```

**Impact of new exploding unit deal:** Strike resets downward, but not all the way to the new offering price. The more dilutive the new deal, the bigger the reset. This creates additional warrant shares that can be exercised, adding to selling pressure.

**Risk level: MEDIUM / ORANGE**

### Type 3: Full Ratchet Anti-Dilution (HIGH RISK)

**Language to look for:**
- "full ratchet"
- "the exercise price shall be reduced to the price per share at which such additional shares are issued"
- "the lowest price" + "issuance"
- "the exercise price shall be adjusted to equal the effective price per share"

**What it means:** Strike price resets to the LOWEST price in any new equity issuance, regardless of how many shares are issued. This is the most punitive form of anti-dilution.

**Impact of new exploding unit deal:** If the effective price of the new deal (after all resets and ZEP) is below the existing instrument's strike, the existing strike resets to that new low price. This can create massive additional dilution.

**Example:** Prior warrants struck at $3.16. New deal offers units at $0.3231. If full ratchet applies, warrants reset to $0.3231 (or even lower if the effective price after reset is lower). Number of warrant shares increases proportionally.

**Risk level: HIGH / RED**

### Type 4: Floating / Variable Conversion (HIGH RISK)

**Language to look for:**
- "conversion price equal to [X]% of VWAP"
- "floating conversion rate"
- "variable rate" + "conversion"
- "market price" + "conversion"
- "the lower of (i) [fixed price] and (ii) [% of VWAP/market price]"

**What it means:** Conversion price is tied to the market price (typically at a discount to VWAP). As the stock falls, more shares are issuable on conversion. This creates a "death spiral" — lower stock price → more shares → more selling → lower stock price.

**Impact of new exploding unit deal:** Catastrophic. The offering craters the stock, which lowers the conversion price, which means more shares are issuable, which creates more selling pressure. These instruments actively work against you when you're trying to monetize your position.

**Risk level: HIGH / RED**

---

## Common Instrument Types

### Prior Exploding Unit Warrants

Most common in repeat-offender issuers. The first offering's warrants may still be outstanding.

**Check:**
- How many remain outstanding vs. already exercised (via ZEP or cash)
- What's the current strike (after all resets)
- Anti-dilution type (almost always structural only for Maxim deals)
- Term remaining

**Typical finding:** Most prior warrants have already been exercised via ZEP within days of issuance. Remaining warrants are usually a small fraction, struck well above current price, with structural-only anti-dilution. **Low risk.**

### Convertible Notes

**Check:**
- Principal outstanding
- Conversion price (fixed vs. floating)
- Anti-dilution provisions (this is the critical question)
- Maturity date
- Whether conversion can be forced vs. optional

**Red flags:**
- Floating conversion at discount to VWAP → death spiral
- Full ratchet anti-dilution → strike resets to offering price
- Short maturity with balloon payment → forced conversion pressure

### Equity Lines of Credit (ELOCs) / SEPAs

**Check:**
- Facility size remaining
- Pricing mechanism (typically at discount to VWAP)
- Whether the company has been actively drawing
- Commitment period remaining

**Impact:** ELOCs create ongoing selling pressure as the company draws and shares are sold into the market. If the company is actively using an ELOC alongside this offering, it's double dilution.

### Stock Incentive Plans (S-8)

**Check:**
- Shares authorized vs. granted vs. vested
- Exercise prices of outstanding options

**Typical finding:** Even if large share reserves exist, grants are usually made at market prices and most are unvested. Low immediate dilution risk unless there's a change-of-control acceleration clause.

### Legacy SPAC/Merger Instruments

**Check:**
- Founder shares, earn-out shares
- SPAC warrants (typically struck at $11.50 pre-split)
- Rights from the SPAC structure
- Sponsor earn-out provisions

**Typical finding:** For post-deSPAC companies that have already crashed, legacy SPAC warrants are deeply underwater and irrelevant. But check if they have any unusual provisions.

---

## Modeling Existing Instrument Impact in the Excel

For each instrument that DOES reset on the new deal:

1. Calculate the new strike/conversion price post-reset
2. Calculate new shares issuable at the reset strike
3. Add these to the fully diluted share count in Tab 3, Section A
4. Note the additional dilution percentage in the risk matrix

For instruments that do NOT reset: just note the current status (outstanding vs. exercised, underwater vs. in-the-money) for completeness.

---

## Red Flags Checklist

When reviewing a filing, flag these as HIGH RISK:
- [ ] Any instrument with "full ratchet" anti-dilution
- [ ] Any convertible note with floating/variable conversion
- [ ] Active ELOC with remaining capacity
- [ ] Multiple prior offerings in the last 6 months (serial diluter)
- [ ] Going concern opinion in the financial statements
- [ ] Late periodic filings (20-F, 10-K)
- [ ] Auditor changes in the last 12 months
- [ ] Related party convertible notes (insiders lending to company)
- [ ] Large blocks of registered but unissued shares
