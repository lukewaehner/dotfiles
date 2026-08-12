# Git Practices

## Commit Messages

Use Conventional Commits:

```
<type>(<optional scope>): <description>

<optional body>

<optional footer>
```

### Types

| Type | Use for |
|------|---------|
| `feat` | New user-facing capability |
| `fix` | Bug fix |
| `perf` | Performance improvement with no behavior change |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or correcting tests |
| `docs` | Documentation only |
| `build` | Build system, dependencies, packaging |
| `ci` | CI configuration and scripts |
| `chore` | Maintenance that doesn't touch src or tests |
| `style` | Formatting only (whitespace, semicolons) — never logic |
| `revert` | Reverts a previous commit |

### Rules

- Subject line: imperative mood, lowercase after the colon, no trailing period, ≤ 72 chars.
  - Good: `fix(parser): handle empty input arrays`
  - Bad: `Fixed the parser so it handles empty arrays.`
- Breaking changes: append `!` after the type/scope (`feat(api)!: drop v1 endpoints`) and add a `BREAKING CHANGE:` footer explaining the migration.
- Body explains **why**, not what. The diff already shows what.
- Wrap body at 72 chars.
- Reference issues in the footer: `Refs: #123`, `Closes: #456`.

### Never Include

- **No `Co-Authored-By` trailers.** Do not add co-author lines for AI assistance.
- No "Generated with" / tool attribution footers.
- No emoji in commit messages.
- No `WIP` commits on shared branches — squash them before pushing.

## Branching

- Branch names: `<type>/<short-kebab-description>` — e.g. `feat/order-book-cache`, `fix/null-deref-on-retry`.
- Branch from the current default branch; keep branches short-lived.
- Rebase onto the base branch to stay current; merge commits only when integrating a completed branch.
- Never force-push a shared branch. `--force-with-lease` on your own branch only.

## Stacked PRs

For a feature that naturally splits into dependent layers (e.g. backend wiring → API endpoint → frontend rendering), use `gh stack` (`gh extension install github/gh-stack`) instead of one long-lived branch or one giant PR.

- Each layer is its own branch and its own PR, based on the layer below it — reviewers see a small, focused diff per layer instead of the whole feature at once.
- Use it when the layers are genuinely sequential and each is independently reviewable (backend model/schema → API route → UI consuming it). Don't force unrelated work into a stack just to avoid opening separate PRs.
- Typical flow: `gh stack init <bottom-branch>` → implement and commit → `gh stack add <next-branch>` for each subsequent layer → `gh stack submit` to open the linked PR chain.
- Keep the stack rebased with `gh stack rebase` (or `gh stack sync`) as lower layers change from review feedback — don't let upper layers drift.
- When a lower PR merges, `gh stack sync --prune` to fast-forward the stack and clean up the merged branch.
- Still apply normal commit hygiene (atomic commits, Conventional Commit messages, no mixed concerns) within each branch of the stack — stacking branches doesn't replace disciplined commits.

## Commit Hygiene

- One logical change per commit. If the message needs "and", split it.
- Commits must build and pass tests independently — this keeps `git bisect` usable.
- Keep formatting/lint churn in a separate `style:` commit from logic changes.
- Never commit secrets, credentials, `.env` files, or large binaries. Check `git diff --staged` before every commit.
- Stage deliberately (`git add -p`), not `git add .`.

## Pull Requests

- Title follows the same Conventional Commit format as the squash commit.
- Description covers: what changed, why, how it was verified, and any risk/rollback plan.
- Keep PRs small — under ~400 lines of diff where possible. Large PRs get shallow reviews.
- Rebase and re-run tests before merging.
