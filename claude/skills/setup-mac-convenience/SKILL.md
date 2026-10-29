---
name: setup-mac-convenience
description: Install or restore the user's shell, Git, and development convenience environment on a new Mac, including eza, zoxide, fzf, fasd file search, bundled git-checkout-pr source, apps, and macOS preferences. Use for new-computer setup or reinstalling this environment.
---

# Set Up Mac Convenience Tools

This entire folder is a portable installation package. It does not require access to the previous Mac or its `/private/tmp` files. For Windows or Linux requests, establish the appropriate scope before applying any macOS-specific settings.

## Establish scope

The baseline is **Oh My Zsh + the git plugin + zsh-autosuggestions + eza + zoxide + fzf**, existing fasd search aliases, Git tools, and custom commands. The actual `git-checkout-pr` and `git-done` sources are in [assets/bin](assets/bin). The fasd 1.0.1 source and license are bundled in [assets/vendor/fasd](assets/vendor/fasd).

For a full environment restoration, also follow [references/apps-and-development.md](references/apps-and-development.md). For a partial request, install only the requested scope. Installation history does not establish active use; choose account, corporate, and optional development tools based on the request and the new Mac's purpose. Consult [references/inventory.md](references/inventory.md) for the previous inventory.

Do not request approval again at each stage of an already authorized installation. Record items that actually need user input, such as login, licensing, or corporate deployment, and continue independent work. A request to write or review this skill does not authorize installing the environment on the current computer.

## Installation

Set `$skill_dir` below to the **actual absolute directory containing this SKILL.md** on the target Mac.

1. Inspect the macOS version, CPU, Homebrew location, shell startup files, and existing Git configuration. Do not print complete environment variables, tokens, or keys. Resolve tool paths with `brew --prefix`. Only when Homebrew itself is missing from PATH, search its standard Apple Silicon `/opt/homebrew` and Intel `/usr/local` locations.
2. If Homebrew is absent, follow its [official installation procedure](https://brew.sh/). Complete Xcode Command Line Tools installation when needed. Download and inspect network installation scripts before executing them. Do not run an unrestricted `brew upgrade` across existing packages.
3. Install the baseline tools. Use current compatible stable releases rather than pinning the recorded 2026 versions.

   ```sh
   brew bundle install --file "$skill_dir/assets/Brewfile.core" --no-upgrade
   ```

   Upgrade an outdated fzf with `brew upgrade fzf`. This configuration uses `fzf --zsh` and zoxide's interactive search. The verified baseline was fzf 0.74.5, zoxide 0.10.0, and eza 0.23.5; fzf must be at least 0.51.0. Follow any higher requirement in the documentation for the installed zoxide release.
4. If Oh My Zsh is absent, clone it as follows. Reuse an existing installation. This avoids overwriting the user's `.zshrc`.

   ```sh
   git clone --depth=1 https://github.com/ohmyzsh/ohmyzsh.git "$HOME/.oh-my-zsh"
   ```

5. Read [references/configuration.md](references/configuration.md) and inspect existing initialization and user settings for conflicts. For standard paths, use the bundled file installer. Its default invocation only previews changes; run `--apply` within the user's authorized installation scope.

   ```sh
   python3 "$skill_dir/scripts/install_files.py"
   python3 "$skill_dir/scripts/install_files.py" --apply
   ```

   The installer copies executables and dedicated configuration files, adds source lines to `.zprofile` and `.zshrc`, and adds an include to `.gitconfig`. It backs up changed existing files in a directory with restricted permissions. Repeated runs do not duplicate identical files, source lines, or includes. It stops before writing when a target file is a symlink or a target path escapes the selected home. In those cases, merge through the existing dotfiles management approach. Also adapt to the actual configuration files when `ZDOTDIR`, `GIT_CONFIG_GLOBAL`, or XDG Git configuration is in use.
6. Apply `gh alias set co 'pr checkout'`. If an existing `co` differs, inspect its definition and merge according to the user's intent. Use `gh auth status` to check authentication for the required GitHub hosts. This skill does not supply tokens.
7. Complete Git identity, GPG signing, corporate includes, SDKMAN!, GUI apps, and macOS preferences using the relevant references. Do not infer names, email addresses, key IDs, or corporate hosts from unrelated old files.
8. Only if the user has brought existing visit history, check that the paths are valid on the new Mac and run `zoxide import --merge fasd` once. Do not run the import at every shell startup or populate a fresh Mac with paths from the previous machine.

## Verify and finish

- Run `zsh -n` separately on the generated `.zprofile`, `.zshrc`, and dedicated `.zsh` files.
- In a **fresh zsh using a real PTY**, exercise `ls`, `l`, `ll`, `la`, `lsa`, `z`, `zi`, `zz`, and `j`. Check navigation to a temporary directory containing spaces, fzf selection and cancellation, and Ctrl-R/Ctrl-T/Option-C. Check fasd file search and ensure reload does not duplicate hooks.
- With noninteractive stdin, eza 0.23.x may produce empty output when no path is supplied. Use explicit paths such as `eza .` in automated checks, and separately verify bare `ls` in an interactive terminal. See [upstream #1568](https://github.com/eza-community/eza/issues/1568).
- Inspect the effective values of `git config --get pull.ff`, `git config --get diff.external`, and `git config --get core.editor`, and check `command -v git-checkout-pr git-done`. Existing global or conditional settings can override included values.
- These tests use temporary homes, local Git repositories, fixture GitHub responses, and **real fzf**. They do not create branches in real remote repositories.

  ```sh
  python3 -m unittest discover -s "$skill_dir/tests" -v
  python3 "$skill_dir/tests/checkout_pr.py" "$skill_dir/assets/bin/git-checkout-pr"
  ```

- Start live GitHub verification with authenticated read requests. Test PR checkout in a temporary clone with a clean worktree rather than switching an existing working branch.
- Report installed versions and commands, optional selections, outstanding login or licensing steps, and backup locations. Copying configuration does not complete login, GPG signing, or permission grants. Explain that an existing shell needs `source ~/.zshrc` or a new terminal.

## Transfer to another Mac

Copy this **entire folder** to `~/.claude/skills/setup-mac-convenience/` on the new Mac, then invoke `/setup-mac-convenience Install my convenience environment on this new Mac` in Claude Code. For Codex, use `~/.codex/skills/setup-mac-convenience/` and invoke `$setup-mac-convenience`. Copying only `SKILL.md` omits the command sources and configuration assets. For another agent, instruct it to read this folder's SKILL.md directly.
