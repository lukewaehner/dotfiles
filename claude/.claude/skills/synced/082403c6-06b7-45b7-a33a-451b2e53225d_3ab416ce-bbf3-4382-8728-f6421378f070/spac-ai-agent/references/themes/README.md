# Themes

This directory holds cross-cutting analytical frameworks that apply across many SPAC deals — not tied to any one ticker. Themes are the rules-of-the-road that an experienced SPAC arb analyst would mutter to themselves before reading any new deck.

## When the skill reads these

The skill should consult relevant theme files at four points:

1. **Step 3 (Apply Six Core Principles)** — when a principle is in play on the current deal, read the corresponding theme file for the deeper framework.
2. **Step 4 (Sponsor Archetype Assignment)** — read `sponsor-tiers.md` for the full archetype × execution grid.
3. **Step 4b (Deal-Archetype Check)** — read `deal-archetypes.md` to check whether the deal matches a recognized cross-name multi-trait archetype with a determined Meteora playbook.
4. **Step 6 (WLAC Negative-Example Guards)** — when one of the failure-mode flags fires, read the corresponding theme file for the canonical fix.

The skill does not need to read every theme file on every run — only the ones relevant to the situation. Token-efficient consultation, not full preload.

**Separate directory**: `references/current-themes/` holds the living market-regime / dead-trades / live-themes / active-sponsors files that ARE read unconditionally on every run. That directory is persistent memory about what is currently live vs. dead; this directory is timeless analytical frameworks.

## File naming

`{theme-slug}.md` — descriptive lowercase-hyphenated slug.

## Suggested initial themes

- `sponsor-tiers.md` — full archetype × execution grid (institutional / bank-franchise / serial-hype / middle / first-time / banker-shopped / dead-shell)
- `deal-archetypes.md` — cross-name multi-trait deal archetypes (sponsor + UW + target + structure → determined Meteora playbook); growing library, currently includes Asian-shell + low-quality-UW + banker-shopped target
- `coc-trap.md` — debt change-of-control + minimum cash condition + no PIPE = three-way refinancing trap
- `retail-memeability.md` — which sectors survive post-close above trust and which don't
- `pipe-language.md` — committed vs. "reasonable best efforts" vs. structured-flexibility language
- `audit-quality.md` — first-time PCAOB audits, PFIC traps, going-concern flags, common reclassifications
- `rights-pricing.md` — rights × ratio = implied PubCo, time-value adjustments, when rights mispricing is exploitable
- `extension-economics.md` — when sponsors extend, what extension contributions tell you, redemption dynamics across extensions, postponement mechanic
- `non-redemption-agreements.md` — real NRAs vs. faked NRAs, what to grep for in 424B3 filings
- `warrant-arb.md` — when listed options exist alongside warrants, computing the dislocation, hedge ratios

## File format

Each theme file is freer-form than the current-themes files. Structure suggestion:

```markdown
# {Theme name}

## Core idea
2-3 sentences on what this theme is and why it matters.

## How to recognize it
Concrete signals — what to look for in filings, in the tape, in deal terms.

## How to apply it
What the analysis should say or do when this theme is in play.

## Common mistakes
The wrong way to apply this theme — equally important as the right way.
```

## Maintenance

Add a theme file whenever a recurring pattern surfaces across multiple analyses. Themes are the durable abstraction; the `current-themes/` directory captures what is in-regime right now.
