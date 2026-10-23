# No comments

Prefer code that explains its behavior through names, types, structure, and
meaningful tests. Comments are exceptions, not a substitute for clear code.
Apply this policy within the user's task; it does not authorize a repository-
wide cleanup or weaken existing correctness, test, or review requirements.

## Scope and timing

- Use explicit files or a diff supplied by the caller. Otherwise use the
  active task's source changes, including relevant staged, unstaged, and
  untracked files and the surrounding code needed to understand them. Resolve
  the actual base instead of assuming `main`. Preserve unrelated user changes.
- Apply the policy as source is edited and check the final candidate before
  review or an authorized commit. Reuse an audit that still covers the same
  content; a commit alone does not require another pass.
- Prose documents, examples of literal comment text in data or fixtures, and
  generated or vendored files are not targets for mechanical deletion. When
  an authorized task needs generated output changed, edit its owned generator
  or source and regenerate through the project's target.

## Remove or express in code

- Remove step-by-step narration, redundant WHAT-comments, section banners,
  change-history notes, and commented-out code. Do not replace them with
  shorter narration or add trivial helpers merely to avoid a comment.
- An explanation of a surprise in code we own is a signal to inspect the
  design. Name the relevant symbol and the concrete improvement: a clearer
  name, simpler control flow, better type, cohesive extraction, or an invariant
  asserted by a meaningful test. Confirm that the improvement actually helps
  before changing the design; an abstraction is not justified by comment count.
- Investigate `IMPORTANT`, `do not remove`, workaround explanations, and
  similar constraints against the implementation, callers, history, tests, or
  authoritative documentation. Preserve the behavior that remains required.
  Encode a valid internal constraint before deleting its only explanation.
  Do not turn a suspected defect into a permanent test expectation.
- Fix false claims and stale comments. When a claim is unresolved, retain
  only the necessary constraint explanation provisionally and report the
  evidence still needed; do not use uncertainty as a reason to erase it.
  Follow the existing workflow for a genuine blocker or an out-of-scope
  redesign. This provisional retention is not a blanket WHAT-comment exception.

## Keep only justified exceptions

- Legal, copyright, license, and attribution notices that must remain.
- Public API documentation that defines a consumer contract, including
  meaningful preconditions, effects, errors, and compatibility guarantees.
  Remove boilerplate that merely repeats the signature when the docs tooling
  and repository rules do not require it.
- Verified non-obvious constraints imposed by a dependency, platform, vendor,
  or protocol that this task cannot reshape. Keep relevant issue, spec, or RFC
  links explaining a constraint that code alone cannot communicate. Keep the
  explanation accurate and concise; internal awkwardness alone is no exception.
- Required compiler, build, generation, documentation, or other tool directives
  expressed as comments, such as build tags. Preserve their semantics. Treat
  a directive change as a behavior/configuration change, not cosmetic cleanup.
- Formatting directives such as `prettier-ignore`, and narrowly scoped lint
  or type suppressions only when the rule is demonstrably faulty, style-only,
  or the directive is part of an intentional negative test. Confirm its purpose
  and the tool's semantics instead of trusting the comment's label.

## Handle suppressions at the root cause

Inspect `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `noqa`, and similar
directives in scope. When a suppression masks a real correctness or safety
problem, fix the underlying issue and remove the suppression together. Do not
silence the failure elsewhere, weaken tests, disable the rule globally, or
merely remove the directive and leave a broken build. A valid negative type
test may deliberately require an error and its assertion directive; retain it
and verify the test. If a false positive cannot be eliminated appropriately,
keep the narrowest justified suppression and its required explanation.

## Audit, implement, and verify

1. Inspect comments and their code, then use an independent subagent to audit
   the scoped candidate. An existing independent code reviewer may perform
   this pass explicitly; do not spawn a redundant reviewer for the same work.
   When already acting as that reviewer, perform the audit directly without
   recursively delegating. Return file/line evidence, proposed removals,
   concrete code improvements, and justified exceptions. The auditor is
   read-only; the parent owns edits. If delegation is unavailable, audit
   directly and label the missing independence, honoring stricter review gates.
2. Check the report against the code. Reject unsupported claims, lost
   exceptions, scope expansion, and speculative refactors. Implement accepted
   changes under [engineering-change-workflow](../SKILL.md),
   including behavior pinning for refactors and a failing reproducer for bugs.
   Existing authorization covers ordinary in-scope edits; do not ask again
   merely because a comment's constraint is being encoded.
3. Run the applicable tests, lint, typecheck, build, or generated-documentation
   checks. Recheck any directive changes with the tools that interpret them.
   Use risk-appropriate checks for inert prose deletions; changing executable
   code, directives, or operational contracts triggers the corresponding
   review and runtime-verification requirements. Have the reviewer recheck
   affected portions after fixes and record the final verified state.
4. Summarize material removals, code improvements, retained exceptions, and
   unresolved constraints with evidence. Do not optimize for a deletion quota
   or claim the pass fully resolved while required work remains.

Source: pstack-claude's [no-comments](https://github.com/michael-denyer/pstack-claude/blob/1dba27e50e8f18f146bb80f137f0690f8d773c2e/plugins/pstack/skills/no-comments/SKILL.md) and [comment auditor](https://github.com/michael-denyer/pstack-claude/blob/1dba27e50e8f18f146bb80f137f0690f8d773c2e/plugins/pstack/agents/comment-sicko.md).
