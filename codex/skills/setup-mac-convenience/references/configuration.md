# Shell and Git Configuration

## File installer

`scripts/install_files.py` does not change the network, Homebrew installation, accounts, or macOS defaults. Use `--home <directory>` to install into an isolated home. Changed existing files are copied into `~/.local/state/mac-convenience/backups/install-*/`. To restore them, copy only the required backed-up files to their original relative paths and remove newly added source/include entries as appropriate. After a failure, inspect the reported WRITE entries and actual files before rerunning. The installer does not guarantee an atomic rollback across all files.

Installed files:

| Location | Purpose |
|---|---|
| `~/.local/bin/git-checkout-pr` | Bundled original Bash command; requires `gh`, `jq`, `fzf`, and `git` |
| `~/.local/bin/git-done` | Preserves the former `git done` alias implementation as a standalone executable |
| `~/.local/bin/fasd` | fasd 1.0.1 compatibility for file visit history search |
| `~/.local/share/mac-convenience/fasd-LICENSE` | MIT license for the bundled source |
| `~/.config/mac-convenience/homebrew.zsh` | Homebrew discovery and PATH entries for `.local/bin` and `.cargo/bin` |
| `~/.config/mac-convenience/shell.zsh` | Initializes Oh My Zsh, suggestions, search, and navigation |
| `~/.config/mac-convenience/gitconfig` | Fast-forward-only pulls, difftastic, vim, and Keychain |

Home paths containing spaces are supported. The installer prints paths rather than existing configuration contents. It does not duplicate an identical source line already present in `.zshrc`. Rerunning updates managed files to the bundled versions, so keep personal additions in separate files.

## Merge with an existing shell

A fresh setup loads `~/.oh-my-zsh` with the `robbyrussell` theme and git plugin. An already loaded Oh My Zsh instance is reused with its existing plugins and theme. Add git to `plugins` if it is missing from an existing setup.

If `~/.fzf.zsh`, a fasd plugin, or zoxide initialization already exists, establish which configuration owns initialization. The bundled configuration skips fzf initialization when its widgets are already registered; an old widget loaded first would therefore remain active. Remove or modernize old initialization and verify in a fresh shell. Use zoxide for `z`, `zz`, and `j`, while retaining fasd for `a`, `s`, `d`, `f`, `sd`, and `sf`.

Although fasd's upstream is archived, its source is bundled to preserve file history search. zoxide only handles directories. The bundled fasd is the Homebrew-installed release of `clvv/fasd` 1.0.1, preserving the [original source](https://github.com/clvv/fasd/tree/1.0.1) and MIT license. Retain existing comments in vendored source.

The original inventory did not show an active direnv hook. Do not enable it automatically in the baseline installation. When requested, add the following once and allow only project `.envrc` files the user trusts.

```zsh
eval "$(direnv hook zsh)"
```

## Git commands and authentication

`git-checkout-pr` supports:

```sh
git checkout-pr
git checkout-pr 123
git checkout-pr 'author:someone fix bug'
```

It lists up to 50 open PRs ordered by recent updates. It selects a single result directly or uses fzf for multiple results. Local branches are named `pr-number-author-branch`. If that branch already exists, the command switches to it. Authentication comes from `gh`'s per-host login configuration; this skill contains no credentials.

`git done` switches from the current branch to local main and deletes the previous branch with `git branch -d`. It falls back to master when main is absent and exits if already on the target branch. It does not fetch, pull, or force deletion; Git's merge checks determine whether an unmerged branch is retained. An existing `alias.done` takes precedence over the executable, so verify its definition.

The Git include does not copy identity or signing settings. If the user already uses 1Password or another credential helper, adapt the managed file to preserve that choice rather than blindly adding osxkeychain. Preserve existing includeIf ordering and repository-local settings.

Configure Git identity and GPG signing with the user's actual values. Do not substitute a new key for an existing identity or put private keys/passwords in the skill or shell files. After securely transferring or preparing the GPG key, configure:

- `user.name`, `user.email`, and `user.signingkey` for the target account.
- `commit.gpgsign=true` after checking the selected private key and pinentry.
- `pinentry-program` in `~/.gnupg/gpg-agent.conf`, using the actual path resolved as `$(brew --prefix)/bin/pinentry-mac`. Preserve other directives and merge duplicate entries.
- Run `gpgconf --reload gpg-agent`, then verify a signed commit in a temporary repository with `git verify-commit HEAD`.
- Separate corporate and personal identities with the user-selected directory and configuration file, using a condition such as `includeIf "gitdir:~/ghe/"`. `~/ghe/` is the previous convention; adapt it to the new machine.

Use the official login or deployment processes for password managers, cloud synchronization, and corporate tools.
