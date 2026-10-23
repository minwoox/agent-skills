# Independent code review

Use this procedure in addition to the author's [self-review.md](self-review.md).
Choose the mode for the meaningful change, not for each commit, and record the
choice briefly with the verification results.

## Choose the review mode

- **Self-review only:** pure documentation, comment, or formatting changes
  that do not alter behavior, operational contracts, or governing instructions,
  unless the user or applicable rules require independent review.
- **Independent subagent review:** implementation, bug fixes, refactors, and
  changes to tests or governing instructions that affect what is required or
  verified. Refactors still need independent review when behavior is intended
  to remain unchanged.
- **Full deep review:** use the available `deep-review` skill when the user
  requests it, applicable rules require it, or the change adds or alters a
  public API or compatibility contract, concurrency or shared-state behavior,
  security boundaries, data-integrity guarantees, or contracts across modules.
  Judge the affected behavior and failure paths; merely touching a file in
  one of these areas does not make a cosmetic edit high-risk.

For full deep review, read and follow [deep-review](../../deep-review/SKILL.md).
Run every existing phase, including candidate verification and the gap sweep.
It satisfies the independent code-review requirement; do not add a redundant
ordinary review. It does not replace the author's self-review or the runtime
verification required by [verification.md](verification.md).

## Assign an independent reviewer

- Use a fresh subagent that did not implement the change. Give it the user
  request and constraints, applicable instructions, repository location,
  baseline and exact candidate snapshot, and the explicit review scope.
  Include relevant staged, unstaged, and untracked changes; do not silently
  review only `HEAD` or include unrelated user changes.
- Provide the actual diff and access to affected code, callers, and tests.
  Have the reviewer derive its conclusions from these inputs. The author's
  rationale and passing checks are supporting evidence, not a verdict for
  the reviewer to adopt. Avoid supplying the author's conclusions as the
  starting point when a fresh context is available.
- For ordinary review, apply [self-review.md](self-review.md) to the diff and
  enclosing functions, trace affected contracts, and assess test coverage.
  Report concrete findings with locations, triggering conditions or design
  benefits, evidence, and remaining uncertainty. Return no findings when none
  are supported; do not invent issues to fill a quota.
- For deep review, have the reviewer coordinate the skill's full workflow,
  using available subagents within the concurrency limit. Its read-only
  boundary and instruction to report and stop apply to the review task;
  the parent continues the implementation task after receiving the report.
- Reviewers do not edit files or run commands that write into the reviewed
  tree. Assign runtime verification under [verification.md](verification.md)
  separately when needed. The ordinary reviewer may also serve as the runtime
  verifier if it did not author the change, uses the required isolated
  candidate, and keeps code-review findings and runtime evidence distinct.

## Resolve findings and cover the final state

- The parent checks the evidence, fixes confirmed in-scope defects, and
  investigates plausible concerns. Close findings with code-level evidence
  or an appropriate reproducer, not merely green tests or author confidence.
  Evaluate design suggestions for concrete benefit and regression risk;
  request user input only when necessary work exceeds existing authorization
  or the intended contract cannot be resolved from available evidence.
- Run affected checks after fixes and have an independent reviewer recheck
  the changed portions and their effects. Reuse valid findings and coverage
  for unchanged portions. If fixes introduce a new high-risk contract, widen
  the review accordingly. A reviewer who edits the implementation becomes an
  author and must be replaced for independent review.
- Record the reviewed snapshot, reviewer, findings, resolutions, and remaining
  limits alongside the checks for the final state. Continue until actionable
  in-scope defects are resolved or a genuine blocker remains; do not stop the
  implementation task merely because the reviewer has returned a report.

When subagents are unavailable, this code-review policy permits direct
review as a fallback. Explicitly record the missing independence; do not call
it an independent verdict. Still run all `deep-review` phases directly when
that mode is required and the skill is available. If the required `deep-review`
skill itself is unavailable, mark that review BLOCKED and perform the strongest
feasible direct review without claiming its full procedure ran. The fallback
does not waive stricter project gates or the separate independent runtime
verification requirement in [verification.md](verification.md); report any
remaining required gate as blocked.
