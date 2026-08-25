---
name: week-summarizer
description: Use when the user wants a weekly (or custom-window) digest of what shipped across one or more git repositories — summarizing commits from any branch, grouped by functional module, broken out as feat/fix/ci/refactor. Triggers on "week summary", "weekly digest", "what shipped this week", "standup summary across repos", "summarize this week's commits".
---

# Week Summarizer

## Overview

Pulls commits from **every branch** (not just the default one) across the
last week from one or more repos, and groups them by module — the
Conventional Commit scope, or an inferred top-level directory when a commit
has no scope. Only `feat`, `fix`, `ci`, and `refactor` are kept; `docs`,
`test`, `chore`, `style`, `build`, `perf`, and non-conventional subjects are
dropped by design, since those aren't what a weekly digest is for.

## When to Use

- Weekly standup or status summary across one or several repos.
- "What shipped this week in X, Y, Z" or after time away from a project.
- You need work-in-progress branches counted too, not just what landed on
  main — a feature branch with real commits carries signal even before it
  merges.

## How It Works

1. For each repo, `git log --all --no-merges --since=<window>` walks every
   ref, so a commit sitting on an unmerged feature branch still counts.
2. Each commit subject is parsed as a Conventional Commit
   (`type(scope): desc`, optionally `type(scope)!: desc`). Only
   feat/fix/ci/refactor survive the filter.
3. Module = the commit's scope. When a commit has no scope, the script falls
   back to the most common top-level directory among its changed files —
   a heuristic hint, not ground truth. Override it when the diff makes a
   better module name obvious, and treat a near-tie (2-3 directories with
   the same file count) as a sign to look at the full changed-file list
   yourself rather than trust whichever one `sort -rn` happened to put
   first — pick the directory that carries the commit's actual behavior
   change, not the one with the most incidentally-touched files (a repo-wide
   lint/config change, for instance, often touches a "big" directory without
   being about that directory at all).
4. Within a repo, modules print alphabetically; within a module, commits
   group feat → fix → refactor → ci.

## Usage

```bash
~/.claude/skills/week-summarizer/collect-week.sh [--since "<git date expression>"] [repo-path ...]
```

- `--since` accepts anything `git log --since` accepts (`"7 days ago"`,
  `"2 weeks ago"`, `"2026-08-14"`). Default: `7 days ago`.
- Repo paths: any number, in any order relative to `--since`. Default:
  current directory.
- The script prints markdown directly — read-only (`git log`, `git
  diff-tree` only), no writes, no history rewriting. Hand its output back to
  the user as-is, or lightly edit for tone; the parsing and grouping is
  already done.

## Output

```
# <repo-name>

- **<module>**
  - feat: <description> (<short-hash>)
  - fix: <description> (<short-hash>)
```

A repo with no matching commits in the window prints a one-line "no
feat/fix/ci/refactor commits" note instead of an empty header. An invalid
repo path prints "not a git repository, skipped" rather than failing the
whole run.

## Common Mistakes

- **Reading a rebase-duplicated commit as two separate changes.** `--all`
  walks by object identity, not content — a commit that lives on a feature
  branch and again (different hash) on main after a rebase-merge shows up
  as two lines with the same description. Skim for exact repeated
  descriptions before reporting a count of "things shipped."
- **Trusting the inferred module name for scopeless commits without
  checking the diff.** The top-level-directory heuristic is a starting
  point — rename it in the summary when the diff says otherwise (e.g. every
  change funnels through one generic `src/`, or a repo-wide CI/lint change
  happens to touch one directory's files more than another's without being
  "about" that directory).
- **Narrowing to the default branch.** The point of `--all` is catching
  commits that never reached main. Don't "simplify" the query to just
  `main`/`master` — that defeats the reason this skill exists.
