# Observable and independent verification

Use for implementation, bug fixes, and refactors. Keep the existing automated
regression tests, full relevant suite, lint, and review requirements. Performance
measurement applies only under the conditions in `SKILL.md`.

## Exercise the real entry point

- Before editing, define the scenario and pass condition at the surface the
  user or consumer actually uses: a UI interaction, CLI invocation, public API,
  library call, or background job. Check the end state, including persistence
  or downstream effects when relevant, rather than stopping at a success code.
- For a bug, reproduce the symptom on that surface before the fix and repeat
  the same scenario afterward. This supplements the automated failing-then-
  passing reproducer. If original-surface reproduction is infeasible, record
  why, use the strongest controlled alternative, and state what remains
  unverified. Distinguish an observed failure in a controlled reproducer from
  reproduction on the original user surface; do not claim the latter when
  only the controlled check ran.
- For a new feature absent from the baseline, verify the new acceptance
  criteria and adjacent existing behavior. Record that no equivalent old flow
  exists instead of inventing a before/after result.
- Build or start the actual candidate with the project's targets. Confirm
  that the browser, device, process, or endpoint is using that artifact rather
  than an old build or another checkout. Use representative configuration and
  isolated test data; do not require production access to prove a local change.
- Existing integration or end-to-end tests count when they exercise the real
  path and assert its outcome. Add a focused manual or automated check for any
  missing interaction or integration. A mocked helper or static inspection
  alone does not prove the application's behavior.
- Retain useful logs, output, screenshots, or recordings as evidence without
  exposing secrets or personal data. Use tools available in the environment;
  do not depend on pstack-specific drivers or a particular operating system.
- Classify missing tools, devices, credentials, or services as blocked
  verification when they prevent a required check. Complete independent work
  and feasible alternatives, but do not silently mark that check passed or
  inapplicable. Do not claim completion while required verification is blocked.

## Use an independent verifier

- After the candidate is ready, assign verification to a fresh subagent that
  did not implement it. Provide the user request and later constraints,
  applicable instructions, repository location, exact candidate and baseline,
  and setup or reproduction information. The verifier derives its checks from
  those inputs and the code. The author's report is a pointer, not proof.
- Give delegated authors separate worktrees when working in a Git repository.
  Give the verifier its own checkout of the exact candidate, or an isolated
  copy for a non-Git project. Include relevant uncommitted and untracked files;
  checking only `HEAD` must not silently omit the actual fix. Preserve unrelated
  user work. Do not reset shared branches or delete another agent's work.
- The verifier reads the actual diff, affected code, and tests; checks that
  the tests establish the intended contract; and independently runs the
  load-bearing reproducer or acceptance scenario and relevant boundaries.
  It checks raw evidence for the remaining required suite, lint, and other
  gates against the candidate, rerunning checks when evidence is absent,
  insufficient, or stale. CI alone is not the independent verdict.
- The verifier may run builds, tests, and isolated probes, but does not edit
  the implementation or weaken tests to obtain a pass. Return the candidate
  identity, checks performed, evidence, and confirmed failures or unresolved
  concerns. Use PASS only when all required evidence is adequate; otherwise
  return FAIL for demonstrated defects or BLOCKED for missing verification.
- The author fixes confirmed in-scope problems. Investigate plausible concerns
  and resolve them with evidence; do not dismiss them because tests are green.
  Re-verify affected scenarios after fixes. A verifier that has not edited the
  implementation may recheck the updated candidate with the complete current
  brief. If it becomes an author, assign a different verifier. Continue until
  required checks pass or a genuine blocker remains, without an arbitrary
  fixed number of fix rounds.
- If delegation is unavailable, record independent verification as blocked;
  self-review or sequential role-playing is not an independent verdict.
  Continue other useful work and report the missing gate explicitly.
- Keep `deep-review` unchanged when that review is requested or required.
  Its candidate verification and gap sweep assess code; this verification
  additionally establishes runtime behavior. Do not shorten its phases or
  replace either result with the other. A reviewer subject to its read-only
  boundary must not run builds that write into the reviewed tree; assign
  runtime verification separately in an isolated checkout when needed.

## Record the exact state covered by evidence

Maintain a concise verification record in the task notes or a linked artifact;
do not require a new tracked repository file. Include:

- Scope and identity: repository, baseline/base revision, candidate HEAD, and
  whether the worktree is clean. A dirty worktree needs a reproducible snapshot
  of the relevant staged, unstaged, and untracked content, with a diff or file
  manifest and content hashes. `HEAD` alone does not identify uncommitted work.
  For a non-Git project, use a file manifest with hashes of the verified inputs.
- Conditions: runtime/build artifact and source mapping, dependency versions,
  relevant configuration, test data, environment, and commands needed to
  interpret or reproduce the checks. Include relevant generated inputs.
- Results: each required check's PASS, FAIL, BLOCKED, or N/A status, tested
  state, command or scenario, observed result, and evidence location. Give a
  reason for N/A and explain limits of substitutes for unavailable checks.
- Independence: verifier identity, the exact state it examined, its verdict,
  findings, and their resolution. Keep code review and runtime evidence
  distinguishable even when they support the same conclusion.

## Reconcile with the final state

- Compare the final diff and artifacts with the verified state before declaring
  completion and, when authorized, before committing, pushing, or creating or
  updating a PR. Do not let concurrent writers change the candidate during
  verification or publication; coordinate their writes and re-read the state.
- Reuse checks that still cover the final candidate. A commit, amend, or
  metadata-only rewrite does not alone require another full suite. Map a new
  commit back to the tested snapshot only after confirming content and relevant
  conditions match; note any excluded working-tree changes.
- Later edits invalidate the checks whose behavior, inputs, or environment
  changed. Rerun those checks and obtain an updated independent verdict when
  its coverage changed. New tests must be run even if runtime code is unchanged.
  Preserve valid results for unaffected parts rather than repeating all checks.
- After a rebase, merge, conflict resolution, base change, or dependency
  update, inspect the resulting code and integration context. A matching diff
  or stable patch ID is insufficient when the base or dependencies changed.
  Re-verify affected integration and behavior; if applicability is uncertain,
  rerun the relevant checks before carrying evidence forward.
- Report the submitted commit or PR head and the state each result actually
  tested. Label a carried-forward result and why it still applies; do not
  claim a command ran on a new SHA when it ran on an earlier equivalent state.
  Keep unresolved required checks visible. This workflow grants no additional
  commit, push, PR, or merge authority; honor the user's existing instructions,
  including human-only merging when specified.

## Sources

Adapted from pstack-claude's
[refactoring](https://github.com/michael-denyer/pstack-claude/blob/1dba27e50e8f18f146bb80f137f0690f8d773c2e/plugins/pstack/skills/poteto-mode/playbooks/refactoring.md)
and [shipping](https://github.com/michael-denyer/pstack-claude/blob/1dba27e50e8f18f146bb80f137f0690f8d773c2e/plugins/pstack/skills/poteto-mode/playbooks/shipping.md)
playbooks. Only the verification mechanisms are adopted; existing local rules
govern implementation quality, comments, performance scope, and authorization.
