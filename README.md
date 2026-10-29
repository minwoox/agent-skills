# Personal agent skills

Personal skills, commands, and global work rules for Claude Code and Codex.
This repository stores copies of installed files. It does not automatically
synchronize with the home directory.

## Layout

| Repository path | Installation path | Contents |
| --- | --- | --- |
| `claude/skills/` | `~/.claude/skills/` | Claude skills and supporting files |
| `claude/commands/` | `~/.claude/commands/` | Git, PR, and test commands |
| `claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | Claude global work rules |
| `codex/skills/` | `~/.codex/skills/` | Codex skills and supporting files |
| `codex/AGENTS.md` | `~/.codex/AGENTS.md` | Codex global work rules |
| `agents/skills/` | `~/.agents/skills/` | Git and PR skills migrated to Codex |

Both tools have these personal skills:

- `engineering-change-workflow`: implementation, validation, and review rules.
- `deep-review`: code review adapted to each tool's instruction files.
- `setup-mac-convenience`: Mac environment restoration, including configuration
  assets, command sources, an installer, and isolated tests.

Keep each skill's entire directory when copying it. Supporting files include
scripts, tests, metadata, reference documents, and vendored source licenses.
The engineering workflow is identical in both tools.

Plugin caches, built-in Codex skills, credentials, session records, and backups
are excluded. Source attribution links and vendored licenses are retained.

## Install the skills

Run these commands from the repository root. They overwrite files at matching
destination paths.

```sh
mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.agents"
cp -R claude/. "$HOME/.claude/"
cp -R codex/. "$HOME/.codex/"
cp -R agents/. "$HOME/.agents/"
```

Check skill discovery in a new session. In Claude, use `/deep-review` for a
review. Copying `setup-mac-convenience` installs the skill; invoke it separately
to restore the Mac environment.

## Save changes

If you edit an installed skill, copy its changed files to the corresponding
repository path above. If you edit the repository copy, copy the changed files
to their installation paths. Apply deletions and renames to both locations.

Review the changes, then commit and push only the intended files.

```sh
git diff
git status --short
git add -- <changed-files>
git commit
git push
```

## Validate the Mac setup package

On macOS, install Python 3, Git, jq, and fzf before running the tests. The tests
also use the system Bash and zsh. From the repository root, run both copies:

```sh
python3 -B -m unittest discover -s codex/skills/setup-mac-convenience/tests -v
python3 -B codex/skills/setup-mac-convenience/tests/checkout_pr.py codex/skills/setup-mac-convenience/assets/bin/git-checkout-pr
python3 -B -m unittest discover -s claude/skills/setup-mac-convenience/tests -v
python3 -B claude/skills/setup-mac-convenience/tests/checkout_pr.py claude/skills/setup-mac-convenience/assets/bin/git-checkout-pr
```

These tests use temporary directories, local Git repositories, fixture GitHub
responses, and real fzf. They do not install applications or modify the current
Mac's shell configuration. Full environment installation has additional manual
checks described in the skill.

## Existing command dependencies

Git and PR commands retain their installed content. The following referenced
helpers are absent from the source environment and are not included here.
Provide the helpers or update their references before using those commands.

- PR creation and description updates reference `github-context.sh` and a
  `_pr-description-generator` agent.
- Migrated Codex skills reference `~/.Codex/scripts/` and `~/.Codex/commands/`.
- Commit commands reference a `how-to-commit` rule. Current commit guidance is
  in each tool's global rules and
  `engineering-change-workflow/references/commits.md`.
