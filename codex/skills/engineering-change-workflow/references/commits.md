# Commit guidance

Before staging, run the repository's lint target and fix all reported errors.
Inspect recent `git log` entries and follow the repository's established style.
Default to conventional commits only when the style is unclear.

For source changes, confirm the [no-comments](no-comments.md) pass
covers the final staged scope. Reuse a valid audit; a new commit alone does not
require another pass. Review later comment or code edits that change its
conclusions before carrying that result forward.

Before committing, reconcile the selected files with the verified snapshot
using [verification.md](verification.md). After creating or amending a commit,
record its SHA and confirm its content matches that snapshot; a commit does
not include unstaged or untracked work automatically. Carry results forward
only when their coverage remains valid. A changed SHA alone does not require
rerunning every check, but changed code, dependencies, or integration context
may invalidate affected checks. Report what the new commit actually covers.

For a non-trivial change, use this structure unless the repository provides a
conflicting template:

```text
<One-line summary>

Motivation:

Explain why the change is needed and what problem it solves.

Modifications:

- Describe the material modifications.

Result:

- Include `Closes #<issue>` when applicable.
- Describe the consequences users will observe after the change is merged.
```

Keep a blank line after the summary, explain the why rather than repeating the
diff, and wrap prose at 72 characters unless the repository requires another
format. A one-line message is sufficient for a typo or another self-evident
change.
