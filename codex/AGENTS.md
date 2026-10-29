# Engineering Rules (Global)

Apply these instructions to every project. Prefer correctness, clean design,
and robustness over speed or minimal changes. Friction and tedium are not
reasons to lower the quality bar.

## Communication

- Write all skills in English, including instructions, supporting
  documentation, and skill metadata, regardless of the conversation language.
- Care personally and challenge directly. Treat the user as a capable
  collaborator whose time and work matter.
- Disagree before implementing something you believe is wrong. Name flaws in
  code, ideas, or plans plainly, and critique the work rather than the person.
- Correct factual errors and flag unclear or contradictory requirements.
- Change your position when new evidence warrants it; otherwise explain the
  remaining disagreement.
- Avoid sycophancy, hedge-stacking, performative agreement, and apology
  inflation. Acknowledge, fix, and move on.

## Scope and completion

- Aim for production-grade output: match project conventions, cover meaningful
  edge cases, handle failure paths, lint and typecheck, and review the result.
- Complete every requested item and phase in the same turn. Do not pause at
  phase boundaries, defer tedious work, or leave placeholder `TODO`/`FIXME`
  comments instead of implementing the requested behavior.
- Stop early only for a genuine blocker: a design problem that invalidates the
  plan, unauthorized scope expansion, ambiguity that cannot be resolved from
  available evidence, or a failure that exposes an unanticipated design flaw.
- Pre-existing bugs and smells in files you touch are in scope to fix.

## Starting repository work

Before modifying an unfamiliar repository, read its README and developer guide
for build steps and conventions.

- Prefer the project's build targets (`task`, `make`, `npm run`, Gradle, Maven,
  or equivalent) over invoking underlying tools directly.
- Match the package manager to the lock file.
- Before inspecting installed dependencies, install them through the project's
  dependency target or package manager if they are missing.
- Generate missing protobuf, GraphQL, OpenAPI, sqlc, or similar sources through
  the project's generation target before retrying a build that needs them.

## Implementation

- Favor cohesive units, clear names, and small composable pieces over clever
  density. Validate boundaries and handle empty, zero, null, and error paths.
- Preserve existing invariants when replacing or moving code. Search for and
  update every caller when a signature, return shape, exception, ordering, or
  timing changes.
- Keep I/O, business logic, and formatting separate when their responsibilities
  differ. Extract real duplication without merging code that will evolve apart.
- Use the `engineering-change-workflow` skill for implementation, bug fixes,
  refactors, tests, planning, and final self-review.

## Validation

- Run every test you add or modify. Start with the affected tests, then run the
  project's full relevant suite before completion.
- Treat failures as real until logs and evidence establish the cause. Read the
  failure before rerunning; do not hide failures with retries or weaker checks.
- Fix every lint error you encounter during the build, even pre-existing ones.
  Run the project's lint target before committing and fix all reported errors.

## Comments

- Apply the [no-comments policy](skills/engineering-change-workflow/references/no-comments.md)
  to source changes. Express behavior through clear code, names, types, and
  tests; remove narration,
  redundant WHAT-comments, banners, and commented-out code.
- Keep the policy's exceptions: legal notices, public API contracts, verified
  external constraints, necessary tool directives, and justified suppressions.
- Investigate a comment's claimed constraint before deleting it. Preserve the
  invariant, encode internal constraints in code or tests where appropriate,
  and verify the result. Correct false comments; do not erase unresolved
  constraints or remove suppressions without addressing the underlying issue.

## Commits

- Lint before staging.
- Follow the repository's recent commit style; default to conventional commits
  when the style is unclear.
- For non-trivial commits, use a concise summary followed by Motivation,
  Modifications, and Result sections. Explain why the change exists, list the
  material modifications, and state the user-visible result. Wrap at 72
  characters unless the repository requires another format.

## Search and shell commands

- Prefer `rg` and `rg --files` for searches. Remember that ignored and hidden
  paths require an explicit path or appropriate `-u`/`--hidden` option.
- The shell is zsh. Pipeline statuses are in the lowercase, 1-indexed
  `pipestatus` array; read `${pipestatus[1]}` immediately for the first command.
- Quote globs intended for programs, such as `find -name '*.tsx'`, so zsh does
  not expand or reject them first.
- Pipe verbose commands through `tee` to retain a full log, and surface the
  upstream exit status immediately after the pipeline.
