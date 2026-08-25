---
name: git-branch-cleanup
description: Use when a repo (or list of repos) has accumulated local branches and you need to decide which are safe to delete, which look stale or abandoned, and which are still active — especially where merges are done via rebase or squash, so a plain `git branch --merged` check misses branches whose commit SHAs no longer match main.
---

# Git Branch Cleanup

## Overview

`git branch --merged` only catches branches that are a direct ancestor of
main. It misses anything rebase-merged or squash-merged, because those
change the commit SHAs — the content is in main, the hashes aren't. This
skill categorizes local branches into three buckets using a stricter check,
and never deletes anything itself; it only produces a report for you to act on.

## When to Use

- Cleaning up local branches across one or more repos.
- The remote's merge strategy is rebase (or squash) rather than merge commits,
  so `--merged` undercounts what's actually landed.
- You need to avoid deleting a branch that just hasn't been pushed yet, or one
  that's behind its own remote (still active elsewhere).

## Algorithm

For each local branch (excluding main), in order:

1. **Not in sync with its remote tracking branch** (ahead, behind, or no
   upstream at all) → **active**, skip further checks. An out-of-sync branch
   is presumed to be in-progress work, not a cleanup candidate.
2. **Direct ancestor of main** (`git merge-base --is-ancestor`) → **safe**
   (merged via fast-forward or merge commit).
3. **Patch-equivalent to commits in main** (`git cherry main branch` — this
   is the check that survives rebase, since `git cherry` compares patch
   content, not SHAs) → **safe** (rebase-merged).
4. **Merged PR found** via `gh pr list --state merged --search "head:<branch>"`
   → **safe**, noted as likely squash-merged (squash produces one commit
   whose patch-id won't match the originals, so step 3 can't catch it —
   this is the fallback).
5. Otherwise, unmerged. Score staleness by days since last commit and commits
   behind main:
   - Old and/or far behind → **stale** (needs human review before deleting).
   - Recent and close to main → **active**.

## Usage

```bash
~/.claude/skills/git-branch-cleanup/analyze-branches.sh [options] [repo-path ...]
```

Options: `--stale-days N` (default 30), `--behind-threshold N` (default 50).
No args → analyzes the current directory. Pass multiple repo paths to sweep
several repos in one report. Requires `gh` on PATH for step 4; without it,
squash-merged branches fall into the stale bucket instead (safe default —
never a false "delete this").

The script only reads (`git fetch --prune`, `log`, `rev-list`, `cherry`) — it
never deletes a branch. Review the "safe to delete" list, then run the
`git branch -d` commands yourself.

## Output

Three sections per repo: **Safe to delete**, **Stale / possibly abandoned**,
**Active**, each with a one-line reason per branch.

## Common Mistakes

- **Trusting `git branch --merged` alone.** It's silent on rebase- and
  squash-merged branches — exactly the branches worth cleaning up.
- **Deleting a branch just because it's unmerged and old.** Age plus
  divergence is a signal for review, not proof of abandonment — that's why
  step 5 lands in "stale," not "safe."
- **Skipping the remote-sync check.** A branch with unpushed local commits
  will look "not merged" and could get flagged for deletion if you don't
  check ahead/behind against its own upstream first.
