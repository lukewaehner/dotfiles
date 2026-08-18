# Rules

Engineering standards for this repo.

| File | Covers |
|---|---|
| [git.md](git.md) | Commit format (`feat`/`fix`/`perf`/...), branching, PR hygiene. **No co-author trailers.** |
| [coding.md](coding.md) | Design, naming, error handling, concurrency, dependencies, security, review |
| [testing.md](testing.md) | What to test, structure, mocking, coverage, flakiness, CI |
| [refactoring.md](refactoring.md) | Safe refactoring, smells, large migrations, deletion |
| [documentation.md](documentation.md) | READMEs, doc comments, ADRs |

## When These Conflict With the Codebase

Match the codebase, then say so. Specifically:

- **Editing existing code** — follow local convention, even where it violates a
  rule here. A file where every error is a bare string gets one more bare
  string, not a lone typed error that matches nothing around it.
- **New file inside an existing module** — follow the module.
- **New module, or a greenfield repo** — follow these rules.
- **Bug fixes** — the regression test is non-negotiable regardless of local
  convention. Write it in whatever style the existing suite already uses.

Raise the conflict in one line when you hit it ("this repo string-matches on
errors, so I matched it rather than introducing one typed error in isolation"),
then keep going. Don't stop to ask. Don't refactor the surrounding code to
satisfy a rule — that's a separate commit, and only if asked.

## Non-Negotiables

1. Commits use Conventional Commit format with **no `Co-Authored-By` or tool-attribution trailers**.
2. Behavior changes and refactors go in separate commits.
3. Every bug fix ships with a regression test.
4. No secrets in source or in logs.
5. Never swallow an error silently.
