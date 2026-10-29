# Apps, macOS Preferences, and Development Tools

## GUI apps

For a full environment restoration, install the baseline GUI bundle. Preserve existing apps and check current cask names, supported OS versions, and availability with `brew info --cask`. If a cask is unavailable, continue installing available items and use the affected app's official distribution channel.

```sh
brew bundle install --file "$skill_dir/assets/Brewfile.apps" --no-upgrade
```

| Tool | Installation and behavior to restore |
|---|---|
| Alfred | Launcher; transfer Powerpack licenses/workflows after confirming ownership |
| Flycut | Clipboard history on `⌘⇧V`; previous app-level launch-at-startup setting was false |
| Magnet | Install through the Mac App Store using the existing purchase; launch at login |
| KeepingYouAwake | Activate when the app launches |
| Rocket | Emoji input; grant Accessibility permissions through the app's instructions when needed |
| DeepL | Translation; sign in if required |
| MacWhisper | Transcription; prepare the selected models and license separately |
| iTerm2 | Apply the key mappings, scrollback, and font settings below |
| CameraController, Ammonite | Check the previous cask names `cameracontroller` and `ammonite`; if unavailable, check official distribution and hardware compatibility, and report any unresolved installation |
| 1Password / Bitwarden | Select the product actually used, then use the `1password` / `bitwarden` cask or official distribution; do not automatically merge accounts or vaults |
| Google Drive / Box / OneDrive | Choose `google-drive`, `box-drive`, or `onedrive`, or official distributions, according to required shared storage; each needs its own login |

Raycast, Maccy, BetterDisplay, OrbStack, and mise were evaluated alternatives, not adopted defaults. Preserve the user's existing choices unless a replacement is requested. The excluded display-resolution app is not part of the installation list.

## macOS preferences

Screenshot location:

```sh
mkdir -p "$HOME/Pictures/screenshots"
defaults write com.apple.screencapture location -string "$HOME/Pictures/screenshots"
defaults read com.apple.screencapture location
```

Restart SystemUIServer if needed and verify the saved location of an actual screenshot. Do not delete existing user files.

Finder's preferred list view:

```sh
defaults write com.apple.finder FXPreferredViewStyle -string Nlsv
defaults read com.apple.finder FXPreferredViewStyle
```

Verify in a new Finder window. Per-folder view settings may still take precedence.

Configure individual settings in the iTerm2 profile actually used. Replacing the whole plist can also copy unrelated profiles, sessions, and tokens.

- Text → Font: Monaco 12.
- Terminal → Scrollback: 100,000 lines.
- Keys → Left Option key: Esc+.
- Option-Left: Send Escape Sequence `b`; Option-Right: Send Escape Sequence `f`.
- Verify word navigation and fzf Option-C in a new session.

The fonts are Hack, Inter, LINE Seed Sans, and LINE Seed JP. Check current Homebrew font casks or install from official distributions. Do not make an unlisted Nerd Font mandatory. iTerm2 uses Monaco separately.

## Development tools

The full previous installation inventory is in `inventory.md`. A direct-request flag does not prove active use. Do not blindly reproduce transitive dependencies, old JDKs, Python 2.7, or codec libraries.

| Area | Installation and conditions |
|---|---|
| Java | Follow the [official SDKMAN! installation](https://sdkman.io/install/). The previous default was Temurin 25; installed majors also included 8/11/13/17/18/19/20/21/25. Select vendors and versions required by projects, using current patch releases. Omit unused historical JDKs |
| SDKMAN! shell integration | Preserve the official installer's `SDKMAN_DIR` and `sdkman-init.sh` source. Keep initialization at the end as required by SDKMAN!, without duplicates. Verify `java -version`, `JAVA_HOME`, and IDE/Gradle toolchain agreement |
| Python | Install baseline uv/uvx. Use `uv tool install` or `uvx` for new Python 3 CLIs. Restore the former pipx selenium/wsdump environment only when those commands are needed, after checking packages and additional dependencies. Restore Python 2.7 separately with pyenv only for a legacy project that requires it |
| IDE | Install JetBrains Toolbox, then select and sign into IntelliJ IDEA, GoLand, CLion, PyCharm, or WebStorm |
| Node | Install `node` and `yarn` when needed. Previous global packages included retire, ts-node, and typescript; prefer project dependencies and lockfiles in new projects. Do not separately reproduce the global npm package |
| Docker | The adopted choice is Docker Desktop (`docker-desktop`). Verify corporate licensing, VPN, registry, and Compose behavior. Do not automatically replace it with OrbStack or Colima |
| Build tools | Install ant, bazel, bison, cmake, maven, gradle, or thrift as projects require. Prefer repository wrappers. If bison is needed, prepend `$(brew --prefix bison)/bin` to PATH |
| git-subrepo | Clone the [official repository](https://github.com/ingydotnet/git-subrepo) into a user path such as `$HOME/.local/share/git-subrepo` and source its `.rc` once. Do not hardcode the previous Mac's `IdeaProjects` path. Reuse an existing clone after checking its remote |
| Diagnostic and utility CLIs | Select actually used tools from the inventory, such as ansible, argocd, bottom, dog, fnt, ghz, git-filter-repo, git-number, graphviz, grpcurl, helm, jq, jwt-cli, kubernetes-cli, pandoc, rust, selenium-server, step, svgbob, telnet, tig, tree, unbound, and zx. Verify current formula availability before installing |
| Corporate tools | Use current corporate deployment procedures for athenz-utils, vksctl, zms-cli, Jamf, Falcon, Cisco, and Ivanti. Do not guess old tap names or authentication details |

Cargo's `svgbob_cli` and Homebrew's `svgbob` can provide overlapping commands; select the required provider. Likewise, use `command -v` to check for conflicting executables from uv, pipx, pyenv, and Homebrew Python. Distinguish SDKMAN! JDKs from Homebrew JDK dependencies.

Existing `~/.fasd`, zoxide databases, and shell history are personal data and are not bundled. If the user transfers them separately, use only paths that exist on the new Mac.
