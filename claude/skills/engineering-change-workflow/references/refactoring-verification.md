# Refactoring verification

Establish the observable contract before moving structure, then verify that
the intended behavior survives the change. Compilation and lint alone do not
establish equivalence.

## Pin the contract before editing

- Identify affected entry points and consumers. Cover relevant outputs,
  errors, side effects, persistence, ordering, resource lifetimes, and timing
  guarantees, not just return values. Inspect comments for contract information
  before restructuring. Apply [no-comments](no-comments.md),
  preserving required exceptions and verifying internal constraints before
  replacing their prose with code or tests.
- Run existing tests that adequately capture the contract. Reuse them rather
  than adding duplicate tests. Where coverage is missing, add meaningful
  characterization tests, reviewed snapshots, or an old-versus-new equivalence
  harness, and run them on the original implementation before restructuring.
- Choose representative cases and boundaries, including relevant empty,
  invalid, concurrent, and failure inputs. Normalize nondeterministic values
  only when they are outside the contract; do not hide ordering or timing
  differences that callers observe.
- Record the baseline revision or snapshot and results using
  [verification.md](verification.md). If editing has already started, recover
  the original implementation in an isolated checkout and run the same checks.
- Existing behavior is evidence, not automatically the intended contract.
  Confirm suspected defects against requirements, callers, or other evidence.
  Fix confirmed defects in touched files under the existing bug-fix workflow;
  do not postpone them merely to keep the refactor pure. Separate their failing
  reproducers and intended behavior changes from the equivalence assertions.
  Seek clarification only when the intended contract cannot be established.

## Preserve behavior through the change

- Name the target structure and the concrete design problem it addresses.
  Refactor in coherent steps, running affected contract checks after steps
  that could change behavior. Keep I/O, business logic, and formatting separate
  where their responsibilities differ; preserve necessary test seams.
- Trace all affected callers and representations, including configuration,
  reflection, serialization, generated interfaces, and string-based lookups
  when relevant. Preserve supported compatibility contracts; do not remove a
  compatibility path simply because the upstream playbook prefers removal.
- Investigate any baseline/candidate mismatch. Classify it as an intended bug
  fix, a demonstrated non-contract difference, or a regression to fix. Do not
  update expected outputs just to make the comparison pass.

## Verify the final candidate

- Run the contract checks and the project's full relevant suite, lint, and
  other applicable checks. For broader changes, compare old and new artifacts
  on the same inputs or replay a recorded workload, including side effects.
- Exercise the affected real entry point and obtain independent verification
  under [verification.md](verification.md). Reuse existing end-to-end evidence
  when it covers the same contract and candidate.
- Report the preserved contract, baseline and candidate identities, evidence
  of equivalence, and any intentional behavior changes with their reproducers.
  Performance measurement remains conditional on the triggers in `SKILL.md`;
  refactoring alone does not require a benchmark.

## Source

Adapted from the pstack-claude
[refactoring playbook](https://github.com/michael-denyer/pstack-claude/blob/1dba27e50e8f18f146bb80f137f0690f8d773c2e/plugins/pstack/skills/poteto-mode/playbooks/refactoring.md).
Existing local rules govern tests, comment exceptions, compatibility, and
defects in touched files.
