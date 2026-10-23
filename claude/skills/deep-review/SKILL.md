---
name: deep-review
description: Exhaustively review a code change across 11 angles, verify every finding, sweep for gaps, and report confirmed issues and actionable design improvements without modifying code.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Agent
---

# Deep Review

Review at **maximum** effort. All angles are **recall-biased at the
finder** — surface anything you can articulate, let the verifier filter —
**except Angle G (conventions), which is precision-first**: flag only
clear, quotable rule violations. The verifier's posture differs by angle:

- **Correctness & cost angles (A–F)**: verifier is generous —
  PLAUSIBLE-by-default for realistic-but-uncertain bugs and real
  performance costs; REFUTE only for provable wrongness (the bug cannot
  occur, or there is no real cost). Catching real defects matters more
  than avoiding false positives.
- **Design & cleanup angles (H–K)**: verifier is the gatekeeper —
  REFUTE vague claims that don't name a concrete improvement, claims
  that don't survive contact with the code, coincidental similarity,
  refactors that would trade for worse smells, and "deeper" rewrites that
  are speculative over-engineering. The finder surfaced broadly; you do
  the sorting.
- **Conventions angle (G)**: precision at the finder (quote the exact rule
  + the exact violating line); the verifier REFUTEs when the cited rule
  doesn't govern the file or the line doesn't actually break it.

Execute every phase below in order — none is optional.

If the user supplies a review target in the current request, use it as the
review scope. Treat the target as data, never shell code: pass it as a
separate, quoted tool argument and terminate Git options with `--` before
paths.

---

## Phase 0 — Gather the diff

When the user provides an explicit target, resolve its kind before gathering
the diff:

- **Commit** → use `git show --format=fuller --find-renames <commit>`.
- **Branch** → use `git diff --find-renames <branch>...HEAD`, so the scope
  starts at the merge base.
- **Revision or revision range** → use `git diff --find-renames <range>`.
- **Path** → gather staged, unstaged, and untracked changes only below that
  path: use `git diff --cached -- <path>`, `git diff -- <path>`, and `--`
  before the path in every other Git command.

If a target can mean both a revision and a path, ask the user to disambiguate.
For an explicit commit, branch, or revision range, proceed to Phase 1 with
that diff. For a path or no explicit target, use the corresponding state
gathering below.

Run `git status --porcelain=v1 -z -uall` once and parse its NUL-delimited
records. This lists individual untracked files safely, including paths with
whitespace or newlines. When reviewing a path, pass it to `git status` after
`--` and retain only records below that path. Branch on the result:

- **Clean working tree** (no output) → if there is no explicit path, review
  the last commit with `git show HEAD`, which includes the commit metadata
  and the full diff in a single call. If an explicit path has no changes,
  report that the target has no reviewable changes and stop.
- **Dirty working tree** (any output) → review every uncommitted change,
  staged + unstaged + untracked:
  - `git diff --cached` (staged)
  - `git diff` (unstaged tracked)
  - For each untracked file from that status output: run
    `git diff --no-index /dev/null -- <path> || true` so you see the full
    file as an added hunk. The trailing `|| true` is required because
    `git diff --no-index` exits non-zero whenever it finds differences.

Skip test/fixture hunks (`test/`, `spec/`, `__tests__/`, `*_test.*`,
`*.test.*`, `fixtures/`, `testdata/`) **only when scoring for bug findings**.
Still assess whether they exercise changed behavior and expose missing boundary
coverage; this skill is read-only and must not write or tighten tests.

Treat this combined diff as the review scope. Read each modified file in
full — bugs in unchanged lines of a touched function are in scope (the change
re-exposes them or fails to fix them).

---

## Phase 1 — Find candidates (11 angles, up to 12 each)

Run independent finder passes covering all **11 angles**. Use available
subagents in batches within the concurrency limit; otherwise perform the
passes directly and sequentially. Do not depend on a particular subagent type
or invocation API. Each pass surfaces **up to 12 candidate findings** with
`file`, `line`, and a one-line `summary`. The fourth required field depends on
the angle:

- **Angles A–G** (correctness, efficiency, conventions): `failure_scenario`
  — the concrete wrong output or crash (A–E), the wasted work / resource
  cost (F), or the quoted rule + violating line (G).
- **Angles H–K** (design, duplication, altitude, public-API design):
  `value_statement` — see each angle for examples of strong and weak forms.

You are reviewing at **maximum** effort. Do not pad to reach 12; if an
angle has fewer real candidates, return fewer.

Do NOT let one angle's conclusions suppress another's — if two angles flag the
same line for different reasons, record both. For A–F, surface every candidate
with a nameable `failure_scenario`; the verifier is the filter. For H–K,
surface candidates only when you can name a concrete target structure and a
specific benefit. **Angle G is the exception** — it is precision-first, so
flag only clear, quotable rule violations, never half-believed ones.

### Angle A — line-by-line diff scan
Read every hunk in the diff, line by line. Then read the enclosing function
for each hunk. For every line ask: what input, state, timing, or platform
makes this line wrong? Look for inverted/wrong conditions, off-by-one,
null/undefined deref, missing `await`, falsy-zero checks, wrong-variable
copy-paste, error swallowed in catch, unescaped regex metachars.

### Angle B — removed-behavior auditor
For every line the diff DELETES or replaces, name the invariant or behavior
it enforced, then search the new code for where that invariant is
re-established. If you can't find it, that's a candidate: a removed guard,
a dropped error path, a narrowed validation, a deleted test that was
covering a real case.

### Angle C — cross-file tracer
For each function the diff changes, find its callers (Grep for the symbol)
and check whether the change breaks any call site: a new precondition, a
changed return shape, a new exception, a timing/ordering dependency. Also
check callees: does a parallel change in the same diff make a call unsafe?

### Angle D — language-pitfall specialist
Scan for the classic pitfalls of the diff's language/framework — for
example: JS falsy-zero, `==` coercion, closure-captured loop var; Python
mutable default args, late-binding closures; Go nil-map write, range-var
capture; SQL injection; timezone/DST drift; float equality. Flag any
instance the diff introduces.

### Angle E — wrapper/proxy correctness
When the diff adds or modifies a type that wraps another (cache, proxy,
decorator, adapter): check that every method routes to the wrapped instance
and not back through a registry/session/global — e.g. a caching provider
holding a `delegate` field that resolves IDs via `session.get(...)` instead
of `delegate.get(...)` will re-enter the cache or recurse. Also check that
the wrapper forwards all the methods the callers actually use.

### Angle F — efficiency & wasted work
Flag performance costs the diff introduces: redundant computation or
repeated I/O, independent operations run sequentially that could overlap,
blocking work added to startup or a hot path, an O(n²)-or-worse pattern on
data that can grow. Also flag long-lived objects built from closures or
captured environments — they pin the whole enclosing scope in memory for
the object's lifetime (a leak when that scope holds large values); prefer a
struct/class that copies only the fields it needs. Name the cheaper
alternative.

**Required `failure_scenario`**: the concrete cost — what is recomputed,
re-fetched, serialized, or retained, and at what scale or frequency it
bites ("re-parses the 2 MB manifest on every keystroke"; "the timeout
closure captures the 50 MB response, keeping it alive for 30 s"). Surface
the candidate whenever you can name the wasted work, even without a
benchmark; the verifier filters.

### Angle G — conventions (applicable instructions)
Find the instruction files that govern the changed code in the current Claude
Code context: `~/.claude/CLAUDE.md`, applicable project `CLAUDE.md`,
`.claude/CLAUDE.md`, `CLAUDE.local.md`, and `.claude/rules/` files, plus any
instruction file the environment explicitly supplies or imports. Apply only
instructions that govern the changed path, including path-scoped rules.
Consider `AGENTS.md` or `AGENTS.override.md` only when the current environment
explicitly makes them applicable.
Read each governing file, then check the diff for clear violations of its
rules. This angle is **precision-first, not recall-biased**: flag a violation
ONLY when you can quote the exact rule and the exact line that breaks it — no
style preferences or "spirit of the doc" inferences. If no instruction file
applies, return nothing for this angle.

**Required `failure_scenario`**: name the governing instruction file, quote
the rule, then quote the line that breaks it ("`CLAUDE.md`: 'Quote every glob
the program should receive as-is' — line 88 passes `--include=*.ts`
unquoted"). The verifier REFUTEs when the cited instruction does not govern
the file or the line does not actually violate it.

### Angle H — refactoring, design & simplification
Look at the diff with a designer's eye. Surface concrete refactorings that
would yield cleaner, more cohesive design: misplaced responsibilities,
leaky abstractions, primitive obsession, long parameter lists,
feature-envy, anaemic helpers wrapping a single call, mixing of concerns
(I/O + business logic + formatting in one function), conditional logic
that should be polymorphism, and modules that grew responsibilities the
name no longer advertises. Also surface unnecessary complexity the diff
adds: redundant or derivable state (a field that could be computed from
data already present), and deep nesting or needless control flow that a
guard clause or early return would flatten. For each, name the smell, the
location, and the specific refactor (extract, move, inline, rename, replace
conditional, introduce parameter object, compute-don't-store, flatten,
etc.).

**Required `value_statement`**: one sentence naming the improvement.
Strong examples — what gets easier, what stops drifting, what stops
surprising a reader, what becomes mechanically impossible to get wrong:

- "extracts the shared validation so the three handlers can't drift, and
  centralizes the error message"
- "replaces the type-switch with polymorphism, so adding a variant no
  longer requires updating three sites"
- "derives the total from the line items instead of storing it, so the two
  can no longer fall out of sync"

### Angle I — duplication, reuse & single-callsite
Three sub-searches — within the diff, against the files the diff touches,
and (for reuse) against the helpers the wider codebase already provides:

- **Duplication to extract.** Flag any case where the diff introduces (or
  leaves untouched in a touched file) two or more near-identical fragments.
  For each, name the duplicated mechanism, the locations, and the shape of
  the extracted helper. The verifier will decide whether extraction
  actually helps (three or more usually does; two depends on whether the
  call sites read better after) and whether the similarity is real vs.
  coincidental (two domains that happen to look alike right now but will
  evolve independently).
- **Reuse over reinvention.** Flag new code that re-implements a helper,
  utility, or pattern the codebase already provides (Grep for the
  capability before assuming it's new) — name the existing symbol to call
  instead. Also flag dead code the diff leaves behind: a branch the change
  made unreachable, a helper or import it orphaned.
- **Single-callsite inlining.** Flag classes, structs, types, methods, or
  functions added or touched by the diff that have exactly one caller, and
  recommend inlining. The verifier will decide whether the construct
  actually earns its keep — documents intent, provides a test seam, or
  otherwise contributes to clean design.

**Required `value_statement`**: one sentence naming the improvement.
Strong examples:

- "three identical 8-line blocks collapse into one helper, so the next fix
  happens in one place instead of three"
- "this single-caller class is a thin shell around `serialize()` and
  inlining removes a level of indirection without losing any test seam"
- "the two near-identical branches differ only in the field name; a small
  helper parameterized on the field reads more cleanly than the
  side-by-side blocks"

### Angle J — altitude & root-cause depth
Check that each change is made at the right depth, not bolted on as a
fragile bandaid. A special case layered on shared infrastructure, a guard
that patches one symptom of a more general bug, or a fix the *next* similar
input would slip straight past — each signals the fix isn't deep enough.
Prefer generalizing the underlying mechanism over accreting special cases.
For each, name the shallow fix, the general mechanism it belongs in, and
the class of input the current depth still gets wrong.

**Required `value_statement`**: one sentence naming what the right depth
buys — which class of future bug it forecloses, or how many special cases
collapse into one mechanism ("handling the empty range inside the iterator
removes the three caller-side guards and the fourth that was forgotten").
The verifier REFUTEs when the "deeper" version is speculative
over-engineering, or trades a clear, correct local fix for a murky
abstraction.

### Angle K — public-API design
Fires **only when the diff adds or changes a public, consumer-facing API
surface**: an exported/public function, method, class, or type; an
HTTP/RPC/GraphQL endpoint or its request/response shape; a CLI flag or
subcommand; a config-file or environment-variable schema; a published event
or message payload; a library's entry point. Internal-only refactors that no
external caller sees belong to Angle H, not here. If the diff changes no such
surface, return nothing for this angle.

For each surface it touches, judge whether the **contract itself** could be
better — because callers depend on it and it is expensive to change once
released, so a newly-added, not-yet-shipped surface is the highest-leverage
place to get the shape right. Look for: naming that is unclear or
inconsistent with sibling APIs already in the codebase (Grep the existing
surface before proposing); a bare boolean/positional parameter that should be
a named enum or options object; primitive obsession at the boundary (a raw
string/int where a domain type belongs); leaking internal representation
callers will get coupled to; error signaling that invites misuse (returning
`null`/`-1`/an empty value for "not found" where callers will silently treat
it as a valid result); parameter orders that are easy to transpose or forget;
asymmetry with a sibling endpoint or overload; an overly broad surface
(exports/knobs that should stay internal); a missing seam for a knob that
will predictably need to grow; and a **breaking** change to an existing
contract that could instead be made additive/backward-compatible (new
optional field, overload, or versioned path). Propose the concrete better
signature or shape — not just "improve the API."

**Required `value_statement`**: one sentence naming the better contract and
what it buys at the call site or over time. Strong examples:

- "replaces `getUser(id, true, false)` with `getUser(id, { includeArchived,
  withPosts })`, so call sites read at the point of use and the next optional
  knob stays additive instead of a fourth positional arg"
- "returns a typed `Result`/throws `NotFoundError` instead of `null`, so
  callers can't silently treat 'not found' as an empty success"
- "aligns the new endpoint's pagination with the existing `?cursor=`
  convention, so consumers don't have to learn a second scheme"
- "keeps the existing `parse(str)` signature and adds `parseWithOptions`,
  turning a breaking change into an additive one so current callers don't
  break"

Weak forms the verifier will REFUTE: "nicer API," "more RESTful," "cleaner
naming" with no named replacement; a proposal that doesn't survive contact
with the existing convention (the codebase already does it the proposed way,
or the "inconsistency" is with an unrelated surface); or a redesign of a
stable, widely-consumed contract whose churn cost dwarfs the ergonomic gain.

---

## Phase 2 — Verify (1-vote)

Dedup near-duplicates (same defect, same location, same reason → keep one).
Tiebreak by picking the candidate with the most concrete `failure_scenario`
(A–G) or the strongest `value_statement` (H–K). For each remaining candidate,
run an independent verification pass. Use subagents when available and batch
candidates from the same file and angle to limit repeated context, but require
a separate verdict and evidence for every candidate. Otherwise perform a
fresh verification pass directly. The verifier returns exactly one of
CONFIRMED / PLAUSIBLE / REFUTED, using the rubric that matches the candidate's
angle.

### Rubric for angles A–F (correctness & cost)

- **CONFIRMED** — can name the inputs/state that trigger it and the wrong
  output or crash; for F, the concrete wasted work or retained memory and
  the scale/frequency at which it bites. Quote the line.
- **PLAUSIBLE** — mechanism is real, trigger is uncertain (timing, env,
  config, scale). State what would confirm it.
- **REFUTED** — factually wrong (code doesn't say that), provably
  impossible (type/constant/invariant — show it), already handled in this
  diff (cite the guard), or pure style with no observable effect; for F,
  no real cost (the work is trivial, off any hot path, or the captured
  scope holds nothing large).

**PLAUSIBLE by default for A–F** — do not refute a candidate for being
"speculative" or "depends on runtime state" when the state is realistic:
concurrency races, nil/undefined on a rare-but-reachable path (error
handler, cold cache, missing optional field), falsy-zero treated as
missing, off-by-one on a boundary the code does not exclude, retry
storms / partial failures, regex/allowlist that lost an anchor, and — for
F — a cost that bites only at a scale the input can plausibly reach (a list
that grows unbounded, a hot path hit per keystroke or per request). These
are PLAUSIBLE.

**Never grounds for REFUTED** — the *age* of the code (pre-existing or
freshly-landed) and its *test coverage* (a
test exists, or passes — a green test can assert the bug or never hit the
case) say nothing about correctness. Neither can carry a REFUTED, and pairing
one with a real reason adds nothing; refute only on a substantive, code-level
reason from the list above.

### Rubric for angles H–K (design / duplication / altitude / API design)

The finder surfaced broadly — **you are the filter**. Read the
candidate's `value_statement` as the improvement claim and judge whether
it holds. **Do not default to PLAUSIBLE for H–K** — that posture
applies to A–F only. For H–K you must be able to reconstruct a
concrete improvement to keep the finding; otherwise REFUTE.

- **CONFIRMED** — the refactor/extraction/inline would clearly improve
  the code today; you can name the resulting structure; you can point to
  the specific file(s) and line(s) the change touches; and the
  `value_statement` accurately describes what gets better.
- **PLAUSIBLE** — would improve the code in the common case but depends
  on taste or on future direction the verifier can't see, OR the
  improvement is real and reconstructable but applying it would expand the
  change's scope or carry regression risk the verifier can't validate now
  (extract a shared module, split a type that grew several responsibilities,
  restructure a subsystem) — a worth/scope/risk judgment a human should
  make. The `value_statement` is concrete enough to evaluate; the benefit
  is just judgment- (or scope-) dependent. Such a refactor is PLAUSIBLE and
  belongs in Phase 4's Design & cleanup suggestions with clear pros, cons,
  and a recommendation.
- **REFUTED** — any of:
  - coincidental similarity (not real duplication);
  - the single-callsite construct actually documents intent or earns a
    test seam;
  - the refactor would trade one smell for a worse one (e.g. a shared
    helper that needs so many config knobs it reads worse than the focused
    copies);
  - the altitude finding's "deeper" version is speculative
    over-engineering, or trades a clear, correct local fix for a murkier
    abstraction;
  - the `value_statement` is vague ("cleaner," "DRY," "more idiomatic"
    with no specific benefit) AND you cannot reconstruct a concrete
    improvement from the candidate, the diff, or the touched files;
  - the `value_statement` is specific but doesn't survive contact with
    the code — the claimed benefit isn't actually delivered.

  **Scale is never grounds for REFUTED.** A refactor whose benefit is real
  and reconstructable does not become REFUTED because it is big, risky, or
  spans many files — that is exactly a scope or risk judgment (kept as
  PLAUSIBLE and reported with pros, cons, and a recommendation). REFUTE only
  when the improvement itself fails on one of
  the reasons above (not-real, worse-smell trade, vague/unreconstructable,
  doesn't-survive-contact), not because the change is large.

### Rubric for angle G (conventions)

Angle G is precision-first, so the verifier mostly confirms what the finder
already quoted.

- **CONFIRMED** — the cited instruction file genuinely governs the changed
  file AND the quoted line breaks the quoted rule. Both quotes are present
  and accurate.
- **PLAUSIBLE** — the rule governs and the line looks like a violation, but
  whether it actually breaks the rule turns on a reading the verifier can't
  settle alone. State the ambiguity.
- **REFUTED** — the cited instruction does not govern this file, the line
  does not actually violate it, or the "rule" is the finder's own style
  preference rather than something the governing instruction states.

### Both rubrics — verify before you judge

**A verdict that CLOSES a finding must rest on something you confirmed in the
code, not assumed — in both directions.** This single gate governs every
refute and every refactor call:

- **Before you REFUTE** (any angle): the refutation's premise — "this path is
  unreachable," "the library strips the trailing newline," "these two blocks are
  coincidental and will diverge" — must be *confirmed*, not asserted. Read the
  implementation, or run a throwaway probe that exercises the exact case, and
  cite the evidence. If you cannot confirm it, do NOT refute: keep the finding
  (PLAUSIBLE for A–G; for H–K keep it as a steering candidate) and note what
  needs checking.
- **Before you keep a refactor as a real improvement** (PLAUSIBLE here or in
  Phase 4's Design & cleanup suggestions): confirm it is *feasible*. Sketch
  the concrete target
  (the new signature / module boundary / resulting structure) and check it (1)
  actually delivers the `value_statement`, (2) does not trade for a worse smell,
  and (3) is mechanically applicable from what you can see. An unworkable target
  — won't compile cleanly, the consumers can't all route through it, the unified
  version reads worse — is REFUTE ("doesn't survive contact"), not a finding to
  carry forward or a decision to hand a human.

The throughline: never DROP a finding on an unverified premise, and never ASK a
human to decide on (or carry forward) a refactor you have not shown can be done.
When unsure, verify — don't guess a verdict.

Keep CONFIRMED and PLAUSIBLE in the working list. Remove REFUTED candidates
from that list, but retain their concise evidence for Phase 4's transparency
section. Run Phase 3 before carrying the verified working list into Phase 4.

---

## Phase 3 — Sweep for gaps

Run **one more finder** as a fresh reviewer who has the verified list.
Re-read the diff and enclosing functions looking ONLY for gaps not
already listed across all eleven angles. Do not re-derive or re-confirm
anything already there — the job is gaps.

Focus on what the first pass tends to miss:

- **Correctness gaps**: moved/extracted code that dropped a guard or
  anchor; second-tier footguns (dataclass default evaluated once,
  `hash()` non-determinism, lock-scope shrink, predicate methods with
  side effects); setup/teardown asymmetry in tests; config defaults
  flipped.
- **Design / duplication / API gaps**: smells the H/I finders missed
  because they focused on the diff hunks rather than the touched file as a
  whole; a duplicated block or single-callsite construct that sits
  outside the changed hunks but inside a touched file; a public-API surface
  the K finder overlooked (an exported symbol, endpoint, flag, or config
  key the diff changed whose contract could be better).
- **Efficiency / altitude / conventions gaps**: a wasted-work or
  memory-retention pattern, a shallow bandaid a deeper fix would
  generalize, or a clear applicable-instruction violation that sits outside
  the changed hunks but inside a touched file.

Surface **up to 12 additional candidates** total, using `failure_scenario`
for correctness, efficiency, and conventions gaps and `value_statement` for
design, duplication, altitude, and API-design gaps (same field rules as
Phase 1;
surface broadly — the verifier is the filter, except conventions, where you
flag only clear, quotable violations). Run survivors through Phase 2 with
the matching rubric. If nothing new, return an empty sweep — do not pad.

---

## Phase 4 — Final report

After verification + sweep, you have the working list. **Keep every
CONFIRMED or PLAUSIBLE finding** — no cap. Rank most-severe first. As a
cross-class tiebreak at equal confidence: correctness bugs (A–E) and real
performance costs (F) outrank design, duplication, altitude, and API-design
improvements (H, I, J, K) — a shipped defect beats a cleanup; a CLAUDE.md
violation (G) ranks by the severity of the rule it breaks. Among the
design-tier suggestions, an API-design finding (K) on a newly-added,
not-yet-released surface ranks first — the contract is cheapest to fix now.

Route A–G CONFIRMED findings to Confirmed findings and A–G PLAUSIBLE findings
to Plausible findings. Route every non-REFUTED H–K finding to Design & cleanup
suggestions, retaining its CONFIRMED or PLAUSIBLE verdict.

Verification may use read-only inspection or probes that do not modify the
repository, its tracked or untracked files, or external systems. **Do not
modify any files.** This is a read-only review. Output the report and stop.

Generate the final report in this exact shape:

```
## Deep Review — <target description>

### Confirmed findings (N)
Bugs and issues that are definitively real. Fix these.
1. <file>:<line> — [CONFIRMED] <one-line summary>. <explanation of the
   failure scenario, 1–2 sentences>.
…

### Plausible findings (M)
Likely issues where the trigger is uncertain (timing, env, config, scale).
Investigate and fix these unless the scenario can be ruled out.
1. <file>:<line> — [PLAUSIBLE] <one-line summary>. <explanation of the
   mechanism and what would confirm it, 1–2 sentences>.
…

### Design & cleanup suggestions (P)
Improvements that would make the code cleaner, safer, or easier to evolve.
Apply at your discretion.
1. <file>:<line> — [CONFIRMED/PLAUSIBLE · DESIGN/DUPLICATION/ALTITUDE/API]
   <one-line summary>.
   <value_statement and how to apply, 1–2 sentences>.
…

### Refuted (Q)
Candidates that were ruled out after verification. Listed for transparency.
1. <file>:<line> — <summary>. <one-line proof of why it was refuted>.
…
```

If a section has zero items, still emit it as "(0)" with "None." — do not
omit any section.
