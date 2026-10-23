# Performance measurement

Use this procedure when the performance conditions in `SKILL.md` apply. The
unit of verification is the meaningful change or PR, not a Git commit.

## Define the comparison

- Name the affected user or system path, the expected cost change, and the
  metric: for example latency, throughput, peak memory, or I/O volume. Use
  representative data sizes, concurrency, and warm or cold cache conditions.
- Inspect the harness: identify what it times, counts, and excludes. Prefer
  the project's benchmark target and existing performance gates. Define the
  regression threshold before interpreting results when a gate needs one.
- Capture the baseline before editing the affected implementation. Identify
  both versions by revision and any uncommitted patch, and retain commands,
  inputs, settings, and raw results. If work has already started, reconstruct
  the baseline in an isolated checkout without disturbing current changes.

## Make the work and comparison valid

- Confirm that the timed work actually finishes and its result is consumed:
  requests reach the server, asynchronous work is awaited, and expected rows
  or bytes are processed. Count errors, rejections, timeouts, retries, and
  completed work; validate outputs, not just their presence.
- Use production-representative builds and settings. Keep hardware, workload,
  harness, and configuration comparable except for the intended change. For
  an adoption decision, tune each candidate appropriately before choosing one;
  for a configuration fix, retain the old setting as the explicit baseline.
- Check machine load using tools available on the current platform. Avoid
  overlapping measurements with builds, tests, or other agents using the same
  resources. If contention cannot be controlled, record it and treat results
  as inconclusive when it could change the conclusion.
- Separate warmup from measured runs for steady-state workloads. Measure cold
  startup or cold caches explicitly when those are part of the affected path.

## Measure and explain the result

- Use the project's established statistical method when available. Otherwise,
  alternate baseline and candidate runs, with at least five measured runs per
  side. Report the median and range of the chosen metric. A single run is
  suitable only for an explicitly requested rough estimate or an exploratory
  probe; it cannot establish a regression, improvement, or adoption decision.
- If the difference is comparable to run-to-run variation, report no
  measurable difference or inconclusive evidence. Use more samples or the
  harness's statistical analysis when the decision depends on a close result.
- Investigate the limiting resource when explaining a difference or an
  expected improvement that did not appear. Profile separately from reported
  timing runs, and verify the load generator is not the bottleneck. Check
  claimed gains against bandwidth, CPU capacity, and the fraction of total
  cost actually changed. Do not invent a causal explanation from timing alone.
- Pair microbenchmarks with a representative measurement of the affected
  end-to-end path. Report how much of the whole the changed component accounts
  for. If that path cannot be measured, state the limit and do not infer a
  user-visible gain from the microbenchmark alone.

## Verify the final state and reuse valid evidence

- Compare the baseline with the final candidate. Intermediate measurements
  are useful when they resolve an implementation decision, not because another
  commit was created.
- Reuse results while they still cover the final code and measurement
  conditions. Rerun affected measurements after changes to the measured path,
  relevant dependencies or configuration, workload, harness, or environment,
  or when failures or new evidence invalidate the result. An unrelated comment
  edit or commit alone does not invalidate performance evidence.
- Follow existing project performance gates even when this policy would not
  otherwise require a new benchmark. Treat failed gates as failures; do not
  hide them with selective reruns, discarded samples, or weaker thresholds.
- Report the verdict, before/after values with units, run counts and spread,
  tested revisions, workload, commands or artifact locations, and relevant
  limitations. Distinguish measured results from explanations. If work counts,
  output correctness, or comparison conditions are unverified, the result is
  inconclusive. State blocked required checks rather than claiming success.

## Source

Adapted from the pstack-claude
[benchmark checklist](https://github.com/michael-denyer/pstack-claude/blob/1dba27e50e8f18f146bb80f137f0690f8d773c2e/plugins/pstack/skills/benchmark-checklist/SKILL.md).
The conditional trigger and reuse policy here govern this local workflow;
this does not import the broader per-PR performance requirement from its
multi-phase playbook.
