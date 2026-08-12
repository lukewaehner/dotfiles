# Coding Practices

## Core Principles

- **Make it work, make it right, make it fast — in that order.** Don't optimize before profiling.
- **Optimize for reading.** Code is read far more often than it's written. Clarity beats cleverness every time.
- **Least surprise.** A function should do what its name says and nothing else. No hidden I/O, no hidden mutation, no hidden globals.
- **YAGNI.** Build for today's requirement. Don't add abstraction layers for hypothetical futures.
- **Rule of three.** Duplicate twice before abstracting. Premature abstraction is more expensive than duplication.

## Design

- Prefer composition over inheritance.
- Depend on interfaces/traits, not concrete implementations, at module boundaries.
- Push side effects (I/O, network, clock, randomness) to the edges. Keep the core pure and easy to test.
- Make illegal states unrepresentable — use enums, sum types, and constructors that validate rather than runtime `if` checks scattered everywhere.
- Keep functions short and single-purpose. If you need a comment to explain a block, extract it into a named function.
- Minimize public surface area. Default to private; widen visibility only when required.

## Naming

- Names describe intent, not implementation: `pendingOrders`, not `list2`.
- Booleans read as predicates: `isValid`, `hasExpired`, `shouldRetry`.
- Avoid abbreviations except universally understood ones (`id`, `url`, `db`).
- Function names are verbs; type names are nouns.
- Be consistent within a codebase — match existing conventions over personal preference.

## Error Handling

- Never swallow errors silently. No empty `catch` blocks.
- Fail fast at boundaries; validate inputs at the point of entry.
- Use typed/structured errors, not string matching.
- Error messages include context: what was being attempted, with which inputs, and what went wrong.
- Distinguish expected failures (return a result type) from bugs (panic/throw).
- Clean up resources deterministically — `defer`, RAII, `with`, `try-with-resources`.

## Comments & Documentation

- Comment **why**, not **what**. The code says what.
- Document non-obvious invariants, tradeoffs, and links to the issue or spec that motivated a decision.
- Public APIs get doc comments: purpose, parameters, return value, errors raised.
- Delete commented-out code. Version control remembers it.
- `TODO` comments include an owner and a ticket reference or they get deleted.

## State & Concurrency

- Prefer immutable data. Mutate only where it's measurably necessary.
- Narrow variable scope to the smallest block that works.
- Avoid shared mutable state; if unavoidable, guard it with a single clearly documented lock strategy.
- Never hold a lock across an `await`/blocking call.
- Make concurrency explicit and bounded — use worker pools and backpressure, not unbounded spawning.

## Dependencies

- Every dependency is a liability: supply chain risk, upgrade burden, binary size. Justify each one.
- Pin versions with a lockfile committed to the repo.
- Wrap third-party libraries behind a thin internal interface when they're used in more than a few places.
- Prefer the standard library when it's adequate.

## Performance

- Measure before optimizing. Profile, don't guess.
- Optimize algorithmic complexity before micro-optimizing.
- Watch for N+1 queries, unnecessary allocations in hot loops, and repeated work that could be hoisted or cached.
- Document any non-obvious optimization with a comment explaining the measurement that justified it.

## Security

- Validate and sanitize all external input at the boundary.
- Parameterize queries — never build SQL by string concatenation.
- Secrets come from the environment or a secret manager, never from source.
- Log identifiers, not payloads. Never log credentials, tokens, PII, or full request bodies.
- Apply least privilege to credentials, file permissions, and network access.

## Code Review

- Review for correctness, readability, and test coverage — not style. Style is the linter's job.
- Distinguish blocking concerns from suggestions; label nits as nits.
- Comment on the code, not the author.
- If a change needs a verbal explanation to be understood, the code or the comments need work.
