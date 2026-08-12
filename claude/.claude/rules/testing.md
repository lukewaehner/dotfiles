# Testing Practices

## What to Test

- Test **behavior**, not implementation. Tests should survive a refactor that preserves behavior.
- Every bug fix starts with a failing test that reproduces the bug.
- Prioritize: business logic and invariants > boundary conditions > integration seams > glue code.
- Don't test the language, the framework, or third-party libraries.
- Don't test private methods directly. If a private method needs its own test, it probably wants to be its own unit.

## Test Structure

Arrange–Act–Assert, with visual separation:

```
// arrange
const account = Account.withBalance(100);

// act
const result = account.withdraw(150);

// assert
expect(result).toEqual(Err(InsufficientFunds));
```

- One logical assertion per test. Multiple `expect` calls are fine if they verify one behavior.
- Test names state the scenario and expected outcome:
  - Good: `withdraw_returns_insufficient_funds_when_amount_exceeds_balance`
  - Bad: `testWithdraw2`
- No conditionals or loops in tests. Branching logic in a test means it should be two tests, or a parameterized/table-driven test.
- No sleeps. Use fake clocks, deterministic scheduling, or explicit synchronization.

## Test Pyramid

- **Unit tests** — the bulk. Fast (milliseconds), no I/O, no network, no filesystem.
- **Integration tests** — verify real boundaries: database queries, HTTP handlers, serialization. Use real dependencies in containers where practical, not mocks.
- **End-to-end tests** — a thin layer covering critical user paths only. Slow and brittle; keep the count low.

## Test Data & Isolation

- Tests must be independent and order-independent. No shared mutable state between tests.
- Each test creates the data it needs and cleans up after itself (or runs in a transaction that rolls back).
- Use builders or factories with sensible defaults; override only the fields relevant to the test.
- Prefer explicit literal values over computed ones — a test that duplicates production logic to compute the expected value tests nothing.

## Mocking

- Mock at architectural boundaries you don't own: external HTTP APIs, payment processors, email senders.
- Don't mock what you own. Use the real implementation or a lightweight fake.
- Prefer fakes (in-memory implementations of an interface) over mocks with expectation chains.
- If a test needs more than two or three mocks, the unit under test has too many dependencies. Fix the design, not the test.

## Coverage

- Coverage is a diagnostic, not a target. High coverage with weak assertions is worse than honest gaps.
- Uncovered branches are a prompt to ask "should this be tested?" — sometimes the answer is no.
- Never write tests solely to raise a coverage number.

## Flakiness

- A flaky test is a broken test. Fix it or delete it — never retry-loop around it.
- Common causes: time dependence, ordering assumptions, shared state, real network calls, unawaited async work.
- Quarantine flakes out of the required CI gate immediately, with a ticket and an owner.

## CI

- The full suite runs on every push. A red build blocks merge.
- The suite must be fast enough that people run it locally — parallelize and split slow suites.
- Tests run against the same versions of dependencies as production.
- No test-only branches in production code (`if (isTest)`). Inject the difference instead.
