# Self-review checklist

Review each changed hunk and its enclosing function against these defect
classes. A nearby defect re-exposed by the change is part of the review.

## Correctness and boundaries

- Check inverted conditions, off-by-one errors, wrong-variable copy/paste,
  swallowed errors, missing awaits, unhandled rejections, races, and narrowed
  lock scopes.
- Check reachable null or undefined values, cold caches, missing optional
  fields, and accidental treatment of valid `0` or empty-string values as
  absent.
- Check regex anchors and escaping, validation boundaries, allowlists, and the
  purpose of every removed or relocated guard. Preserve constraints that remain
  valid; verify that intentional changes match the requested behavior and have
  test coverage for the new contract.

## Ripple effects

- Update all callers after changes to signatures, return values, exceptions,
  timing, or ordering.
- Check callees and concurrent changes for assumptions that are no longer safe.
- Ensure wrappers, caches, proxies, decorators, and adapters call the wrapped
  instance rather than a registry or global path that can re-enter recursively.
  Forward every method callers use.

## Language footguns

Apply these checks using the project's language version and configuration.

- JavaScript/TypeScript: falsy zero or empty strings, coercive equality,
  captured loop variables, and unhandled promises.
- Python: mutable default arguments, late-binding closures, and shared
  dataclass defaults.
- Go: nil-map writes, unchecked errors, and loop-variable capture under the
  project's language semantics. Under Go 1.22+ language semantics, variables
  declared by the loop get a new instance per iteration; assigning to an
  existing variable still reuses it.
- SQL and data: string interpolation, timezone or DST drift, float equality,
  nondeterministic hashes, and iteration order.

## Design

- Apply [no-comments](no-comments.md) to scoped source comments.
  Confirm that removed explanations are reflected in clear code or meaningful
  checks where needed, retained comments meet an exception, and directives or
  suppressions were not mistaken for inert prose.
- Keep responsibilities cohesive and avoid braiding I/O, business logic, and
  formatting.
- Extract duplication when the call sites become clearer and are expected to
  evolve together. Leave coincidental similarity alone.
- Judge abstractions by the responsibility or boundary they clarify, not by
  caller count alone. Preserve useful intent, test seams, resource lifetimes,
  and error-handling boundaries; inline constructs that add only indirection.
- Watch for primitive obsession, long parameter lists, feature envy, anemic
  helpers, repeated type switches, and modules that have outgrown their names.

## Final audit

- Re-read the request or approved plan and compare it with the actual diff.
- Confirm every file, test, verification step, schema or generated update,
  import, call site, and downstream consumer is accounted for.
- Confirm the review mode selected under [code-review.md](code-review.md),
  the independent reviewer's evidence and findings when required, and their
  resolution. Check that review coverage includes later fixes and their effects.
- Verify that recorded checks cover the final state and that blocked or
  inapplicable checks are distinguished from successful ones.
- Check applicable real-flow and refactoring-equivalence evidence, the
  independent verifier's findings, and the tested revision or snapshot. After
  later edits or integration changes, confirm which results remain valid and
  rerun affected checks; a matching patch alone does not prove applicability.
- Close every actionable gap before reporting completion. Report remaining
  blockers and their impact; do not claim completion while required work remains.
