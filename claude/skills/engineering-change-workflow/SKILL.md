---
name: engineering-change-workflow
description: Apply a rigorous workflow when implementing features, fixing bugs, refactoring code, changing tests, cleaning up or auditing source comments, or planning and validating a code change. Do not use for read-only explanations or status reports.
---

# Engineering Change Workflow

Produce a complete, robust change that follows the repository's own build,
test, and style conventions.

## Establish the working context

- Read applicable repository instructions, the README, and the developer guide
  before editing an unfamiliar project.
- Inspect the working tree and existing diff before editing. Preserve unrelated
  user changes; do not overwrite or revert them to simplify the task.
- Identify the repository's official build, generation, lint, typecheck, and
  test targets. Use its package manager and lock file for dependencies, and its
  generation targets for required generated sources.

## Investigate before editing

- Read the relevant code until the behavior, invariants, callers, and failure
  paths are understood. Do not infer a root cause from symptoms alone.
- Search callers and callees before changing a signature, return shape,
  exception, timing, ordering, validation rule, or shared state.
- For every removed or relocated guard or branch, identify its purpose.
  Preserve invariants that remain valid. When the requested behavior changes
  a constraint, make the new contract explicit and cover it with tests.

## Plan observable and independent verification

For implementation, bug fixes, and refactors, read
[references/verification.md](references/verification.md) before editing. Name
the real entry point, expected observable outcome, applicable checks, and how
an independent verifier will inspect and exercise the candidate. Verify bugs
on the affected surface before the fix where feasible, as well as with the
automated reproducer below. Record which code and artifact each check covers.

Pure documentation, comment, or formatting changes do not require launching
an unrelated application or an independent verifier unless existing rules or
the user require one. Use the checks appropriate to the actual change.

## Pin behavior before refactoring

Before behavior-preserving structural changes, read
[references/refactoring-verification.md](references/refactoring-verification.md).
Define the contract and run existing coverage that establishes it; add
characterization tests or an equivalence harness where coverage is missing.
Keep intended bug fixes explicit rather than freezing known defects into the
contract. Verify equivalence again on the final implementation.

## Assess performance impact before editing

Decide whether performance measurement is needed for the task or PR, rather
than for each commit. Measure when any of these conditions applies:

- The task investigates a performance improvement or regression, or makes a
  quantitative performance claim.
- There is a concrete, plausible mechanism for a material change in latency,
  throughput, memory, or resource use. Examples include hot-path algorithms,
  repeated I/O or queries, caching, allocations, concurrency, startup or
  rendering paths, and relevant runtime settings or dependencies.
- The project's existing rules require a performance check.

Name the affected path and why its cost could change. Documentation, comments,
renames, formatting, and structural changes with unchanged execution costs do
not require a new benchmark unless an existing project gate requires one.
Do not treat all code changes as performance-sensitive. When a plausible
impact is uncertain, use a focused measurement or profile to decide the scope.

When measurement is needed, read
[references/performance-measurement.md](references/performance-measurement.md)
and capture a baseline before changing the affected implementation. Record the
scope decision briefly with the verification results. Performance checks do
not replace the required tests, lint, or other correctness checks.

## Fix bugs with a reproducer

Follow this order for bug fixes:

1. Explain the root cause from the code.
2. Add an automated test that reproduces the bug.
3. Run it and confirm it fails for the expected reason. Revise a test that
   passes or fails for another reason.
4. Fix the root cause rather than suppressing the symptom.
5. Run the reproducer and confirm it passes.

For bugs that depend on hardware, external services, or rare timing, first try
to build a controlled reproducer or a suitable test seam. If automated
reproduction remains infeasible, perform the strongest feasible alternative
verification and add useful automated coverage where possible. Record the
obstacle, evidence for the root cause, checks actually performed, and their
limits.
Do not describe a test as a reproducer unless it failed for the expected reason
before the fix. Do not claim the bug is verified fixed when the available
evidence is insufficient.

## Test meaningful behavior

- Add happy-path coverage for new behavior and edge cases exposed by the
  change, including relevant empty, zero, negative, large, concurrent, missing,
  and error cases.
- Assert observable behavior. Do not write tests that merely repeat a mock's
  configured return value or otherwise pass regardless of the implementation.
- Run every added or modified test, then the project's full relevant suite.
  Include affected components and downstream consumers of changed contracts;
  explain the selected scope in the verification record.
- Read logs and stack traces before rerunning a failure. Investigate the change
  as the primary suspect without ruling out other causes.
- Exercise the affected real entry point through its observable end state,
  following [references/verification.md](references/verification.md). Existing
  end-to-end tests may supply this evidence when they actually cover that flow;
  unit tests with mocked integrations alone do not establish it.

## Plan and execute completely

In plan mode, name the known files to add, edit, or delete; enumerate expected
call-site and generated-file changes; specify tests and verification commands;
and include a final self-audit. Record assumptions, unresolved investigation
items, and conditions that would require revising the plan.

Once the plan is approved, execute it without pausing at phase boundaries.
Update the plan as implementation reveals new details within the authorized
scope. Revisit the approach when new evidence invalidates it, and seek user
input when necessary work exceeds existing authorization. Routine implementation
discoveries do not require renewed approval.

## Apply the no-comments policy

For source changes or a source-comment audit, read and apply
[references/no-comments.md](references/no-comments.md) while editing and before
code review. Remove narration and redundant comments, express
internal behavior in code and tests, and preserve the policy's exceptions.
Use the active task's scope; prose documents are not source comments. The
independent code reviewer may perform the comment audit in the same pass.

## Review before completion

Read and apply [references/self-review.md](references/self-review.md) to every
changed hunk and its enclosing function. Also follow
[references/code-review.md](references/code-review.md): use an independent
subagent for implementation, bug fixes, and refactors, and the full
`deep-review` workflow for high-risk changes or when requested. Pure changes
to documentation, comments, or formatting need only self-review unless they
alter an operational contract or governing instructions, or another rule or
the user requires independent review.

Confirm the actual diff covers the request and any approved plan, then
complete the repository's applicable lint, typecheck, tests, build, and
necessary manual verification.

- Resolve review findings under [references/code-review.md](references/code-review.md).
  The parent agent owns fixes and subsequent validation; read-only review
  does not end the implementation task.
- Obtain the independent runtime verification required by
  [references/verification.md](references/verification.md). Runtime verification
  complements code review; neither substitutes for the other. Preserve
  `deep-review`'s full phases and read-only boundary.
- Record the commands, their scope, and results for the final state of the
  change. Follow the verification record in
  [references/verification.md](references/verification.md) to identify tested
  commits or uncommitted snapshots, artifacts, and the independent verdict.
  Identify checks that do not apply and explain why.
- Reuse successful checks that still cover the final state. Rerun affected
  checks when later edits, failures, or new evidence invalidate that coverage;
  do not repeat unchanged checks merely to mark another phase complete.
- Fix failures rather than weakening checks. If required verification is
  blocked, state the cause, what remains unverified, and the resulting
  uncertainty. Do not present blocked checks as passed or claim completion
  while required work remains.

When the user asks to create or amend a commit, also read
[references/commits.md](references/commits.md).
