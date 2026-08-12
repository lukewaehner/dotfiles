# Refactoring Practices

## Ground Rules

- **Refactoring never changes behavior.** If behavior changes, it's a feature or a fix — commit it separately.
- Have passing tests before you start. No tests means characterization tests first: capture current behavior, including the bugs.
- Refactor in small, reversible steps. Run the tests after each one.
- Separate commits: `refactor:` for structure, `feat:`/`fix:` for behavior. Never mix them — a reviewer can't spot a logic change buried in a 500-line move.

## When to Refactor

- Immediately before adding a feature, to make the change easy (then make the easy change).
- When you touch code you don't understand and have to reverse-engineer it — leave it clearer than you found it.
- When the same fix has to be applied in three places.

## When Not To

- Purely because the style differs from your preference.
- In the same PR as an urgent fix.
- Across a wide file surface right before a release or a freeze.
- When you can't articulate what improves. "Cleaner" is not a justification.

## Common Smells

| Smell | Response |
|---|---|
| Long function | Extract named sub-functions |
| Long parameter list | Introduce a parameter object |
| Duplicated logic (3rd occurrence) | Extract shared function |
| Feature envy — method uses another object's data more than its own | Move the method |
| Primitive obsession — raw strings/ints carrying domain meaning | Introduce a value type |
| Boolean flag parameter | Split into two functions |
| Deep nesting | Guard clauses and early returns |
| Shotgun surgery — one change touches many files | Consolidate the responsibility |
| Comment explaining a block | Extract the block into a named function |

## Large Refactors

- Prefer strangler-fig: build the new path alongside the old, migrate callers incrementally, delete the old path last.
- Use feature flags to decouple deploy from cutover.
- Keep the branch mergeable at every step — long-lived refactor branches rot and get abandoned.
- Write down the end state and the migration steps before starting. Share it before writing code.
- **Lean on the compiler.** In a typed language, change the type signature
  first and let the errors enumerate the call sites. The compiler produces a
  complete work list; grep produces a guess.

## Deleting Code

- Delete dead code rather than commenting it out. Git has it.
- Unused exports, feature flags past cutover, deprecated endpoints past their sunset date, tests for removed behavior — all should go.
- Deletion is the highest-leverage refactor available. Prefer it.
