# Documentation Practices

## README

Every repo's README answers, in order:

1. What this is, in one or two sentences.
2. How to run it locally (exact commands, from a clean checkout).
3. How to run the tests.
4. How it's deployed / where it runs.
5. Where to find deeper docs.

Keep it current. A README that lies is worse than no README.

## Code Documentation

- Public APIs get doc comments: purpose, parameters, return value, error conditions, and an example for anything non-obvious.
- Document invariants and preconditions the type system can't express.
- Link to the issue, RFC, or spec that motivated a non-obvious decision.
- Write architecture diagrams as code (Mermaid) committed next to what they
  describe, not as exported images. A diagram that can't be diffed in review
  is a diagram that goes stale silently.

## Architecture Decision Records

For decisions that are expensive to reverse — datastore choice, auth model, service boundaries, major dependency — write a short ADR in `docs/adr/`:

```
# ADR-00N: <Title>

## Status
Proposed | Accepted | Superseded by ADR-00M

## Context
The forces at play. Constraints, requirements, what we know.

## Decision
What we're doing.

## Consequences
What becomes easier. What becomes harder. What we're accepting.
```

ADRs are immutable once accepted — supersede rather than edit.

## Maintenance

- Docs live next to the code they describe and change in the same commit.
- A PR that changes behavior updates the docs in the same PR.
- Delete stale docs aggressively. Outdated documentation actively misleads.
- Prefer generated docs (from types, schemas, OpenAPI specs) over hand-maintained duplicates.
