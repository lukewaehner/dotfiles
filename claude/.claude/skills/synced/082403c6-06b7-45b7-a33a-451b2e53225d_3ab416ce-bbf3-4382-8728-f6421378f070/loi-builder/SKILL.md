---
name: loi-builder
description: Generate Meteora's standard Letter of Intent (LOI) for SPAC business combinations using the locked-in sponsor-friendly clause selection. Use this skill whenever the user asks to draft, build, generate, create, prepare, or write an LOI, letter of intent, or non-binding term sheet for a SPAC business combination, de-SPAC transaction, or proposed merger between a SPAC and a target operating company. Also trigger on phrases like 'draft an LOI for [target]', 'put together an LOI', 'we need an LOI', 'LOI for our deal with X', 'build the LOI for [ticker]', or any reference to creating a non-binding offer letter for a SPAC business combination. Produces a .docx file using Meteora's house-standard clause selection across the project's reference LOI library (BIXI/Unchained/SALT and IVCB/American Tungsten/Trigg/Compute Labs precedents). Always use this skill for SPAC LOI drafting — do not assemble LOIs ad hoc, because consistent clause selection across deals is the entire point of having this skill.
---

# Meteora SPAC LOI Builder

Draft a SPAC business-combination Letter of Intent using Meteora's locked-in clause selection. Every section is pre-decided — see `references/sponsor_friendly_clauses.md` for the actual text and provenance.

## House-standard terms (locked in)

| Term | Choice |
|---|---|
| Founder share haircut | **2/3 (66.67%) converted to warrants**, 1/3 retained by sponsor |
| Min cash condition | **Explicit: NONE** (sponsor can close at 100% redemption) |
| Shareholder earnout | **None** — no dilutive earnout shares to target |
| Board composition | **One designee per Sponsor**, plus independent directors with sponsor consent, target picks rest |
| Tax structure | **Parties cooperate in good faith** (BIXI language) |
| Termination fee | **Silent** (no break-up fee mentioned) |
| Exclusivity | **Non-exclusive with 10-business-day Right of First Negotiation** if target gets a competing bid |
| Term length | **60 days** from signature |
| Diligence access | **Full and prompt, sole discretion of Sponsor** (IVCB) |
| Management availability | **Testing-the-waters mandate** (IVCB) |
| Lock-up threshold | **5%+ Sellers** locked up (BIXI threshold) |
| Public warrants | **Delisted** post-Closing (IVCB) |
| Listing | **Nasdaq or NYSE American (uplist)** |
| Trust waiver | **Standard broad** ("any other matter") |
| Expenses | **Each party bears own** + underwriter waiver/equity reduction language |
| PIPE placement agent | **"May" mutually agree** (no obligation to engage) |
| PIPE inducement disclosure to target | **Silent** |
| LTIP | **10%** of post-Closing outstanding shares |
| Conditions to close | **Minimal**: Seller approval, Sponsor stockholder approval, target MAC/bring-down, listing, catch-all |
| MAC bring-down | **Target only** (sponsor not subject to reciprocal MAC) |
| Founder share lock-up exceptions | **PIPE / non-redemption support carve-out** (universal) |
| Fiduciary out / Superior Proposal | **Dropped entirely** (moot under non-exclusive) |
| Public warrants | **Delisted** |

These are not preferences — they are Meteora's standard. Do not deviate without an explicit instruction from the user.

## Workflow

### Step 1: Read the clause library

Read `references/sponsor_friendly_clauses.md` first. This is the source of truth for every clause. Do not improvise text — pull from the library. Do not soften any clause without an explicit user instruction; if the user asks to soften something, say which clause and what the softer version says before generating.

### Step 2: Collect deal variables

Confirm the following inputs. If the user gave them in the request, just echo them back and proceed. Group remaining gaps into one ask via `ask_user_input_v0` if there are 2 or more, or just ask in plain text for a single missing item.

**Required:**
1. Sponsor full legal name and short name (e.g., "Investcorp Europe Acquisition Corp I" / "IVCB")
2. Target full legal name and short name
3. Sponsor signatory name
4. Target signatory name + title
5. Target address
6. Trust amount (e.g., "$24,170,000")
7. Sponsor's current exchange (typically OTC Expert or OTC Pink for an uplist scenario)
8. Sponsor unit / common / warrant tickers
9. Pre-money valuation
10. LOI date and offer-expiration date
11. NDA date

**Sensible defaults if user doesn't specify:**
- LOI date → today
- Offer expiration → 5–10 business days from LOI date
- Sponsor's current exchange → "OTC Expert Market" if user says they're uplisting; "Nasdaq" if already listed
- Interim relisting → "OTC Pink Market" (default in clause library)

If the sponsor is already on Nasdaq, drop the second sentence of the US Listing clause (the OTC Pink relisting language) — that sentence is only relevant for the IVCB-style uplift path.

### Step 3: Assemble the document

Use `assets/loi_skeleton.md` for the section assembly order. Pull each section's text from `references/sponsor_friendly_clauses.md`. Substitute all `{TOKENS}` with the deal variables.

**Read `/mnt/skills/public/docx/SKILL.md` before generating the file** to refresh on docx-js conventions for this environment. Key requirements:
- US Letter page size (12240 × 15840 DXA)
- Arial default font, 11pt
- 1-inch margins
- Smart quotes via XML entities for inserted apostrophes/quotes
- Section headings: bold + italic, ~12pt
- Defined terms: bold on first appearance only

**Document layout:**

```
[LOI_DATE]                                                 (left-aligned, top of page)

Confidential                                               (italic, optional)

[TARGET_FULL_NAME]
[TARGET_ADDRESS]
Attn: [TARGET_SIGNATORY], [TARGET_TITLE]

Dear [Mr./Ms. SIGNATORY_LASTNAME]:

[OPENING THREE PARAGRAPHS — from "Header / Preamble"]

Proposed Terms and Conditions of Transaction

***Transaction***
[body]

***Board of Directors***
[body]

[... rest of sections ...]

Binding LOI Provisions
(treat as a section divider — bold, larger font, centered or left-aligned)

***Non-Exclusivity with Right of First Negotiation***
[body]

[... rest of binding sections ...]

[Signature Page Follows]
[page break]

If you are in agreement with the terms set forth above and desire to proceed with the
negotiation of the proposed Transaction on the basis of this LOI, please sign this LOI
in the space provided below.

Very truly yours,

[SPONSOR_FULL_NAME]

By: ___________________________
Name: [SPONSOR_SIGNATORY_NAME]


ACCEPTED and AGREED:

[TARGET_FULL_NAME]

By: ___________________________
Name: [TARGET_SIGNATORY_NAME]
```

Use the BIXI-family inline-heading format (section heading on its own line, body text below as flowing paragraphs) — not the IVCB two-column table format. Inline headings read cleaner in Word and are easier for the target to redline.

### Step 4: Deliver

Save the .docx to `/mnt/user-data/outputs/` and present it via `present_files`. Filename pattern:

```
{SPONSOR_SHORT}_{TARGET_SHORT}_LOI_{DATE_COMPACT}.docx
```

Examples: `IVCB_ComputeLabs_LOI_28Apr26.docx`, `BIXI_SALT_LOI_10Apr26.docx`

After presenting, give a brief one-paragraph summary listing the three or four most material terms baked in (founder share haircut %, exclusivity status, min cash, valuation). Don't re-explain the whole spec — just the differentiators the user might want to sanity-check before sending.

## Optional sections (only include if explicitly requested)

These are **omitted by default**. Include only if user explicitly asks:

- **Convertible note financing** — when a concurrent convert is contemplated (e.g., the BIXI/Unchained BTC-collateralized convert structure). Use the clause library's "Optional convertible add-on" text. *Note: this section was removed from the standard library after the spec lock-in but can be inserted under a new heading "Convertible Note Financing" if needed.*
- **Foreign-jurisdiction language** — Australian scheme of arrangement, FIRB approval, ATO scrip-for-scrip ruling, court approval, independent expert. Only if target is non-US **and** user explicitly wants it. **Default: drop entirely** even for foreign targets unless asked.
- **Post-Transaction Capital Structure Exhibit A** — detailed pro-forma cap table. Only if user asks. Default: omit.
- **Public warrants treatment beyond delisting** — modifications, redemption mechanics, etc. Default: leave to Definitive Agreement.

## When to deviate from the locked-in spec

The clauses are intended to be the **opening offer** — the starting position before negotiation. If the user explicitly says "the target won't accept X" or "soften Y," then deviate, but **always tell the user what you're changing and the second-position fallback** before generating. Don't silently soften.

Common second-position fallbacks (for reference):
- 2/3 founder share haircut → 50% (closer compromise)
- No min cash → $25M (SALT precedent) or "to be agreed in Definitive"
- Non-exclusive → 30-day exclusivity (compromise)
- Right of First Negotiation 10 business days → 5 business days (target push)
- Target-only MAC → reciprocal MAC (target push)

If the user wants a fully target-friendly LOI (e.g., they're representing the target side), this skill is the wrong tool — flag it and ask whether they really want the sponsor template.

## Variables reference

See the bottom of `references/sponsor_friendly_clauses.md` for the full token list.
