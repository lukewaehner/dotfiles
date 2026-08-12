# Rules

Engineering standards for this repo. Follow these unless the existing codebase has an established convention that conflicts — in that case, match the codebase and raise the conflict.

| File | Covers |
|---|---|
| [git.md](git.md) | Commit format (`feat`/`fix`/`perf`/...), branching, PR hygiene. **No co-author trailers.** |
| [coding.md](coding.md) | Design, naming, error handling, concurrency, dependencies, security, review |
| [testing.md](testing.md) | What to test, structure, mocking, coverage, flakiness, CI |
| [refactoring.md](refactoring.md) | Safe refactoring, smells, large migrations, deletion |
| [documentation.md](documentation.md) | READMEs, doc comments, ADRs |

## Non-Negotiables

1. Commits use Conventional Commit format with **no `Co-Authored-By` or tool-attribution trailers**.
2. Behavior changes and refactors go in separate commits.
3. Every bug fix ships with a regression test.
4. No secrets in source or in logs.
5. Never swallow an error silently.
