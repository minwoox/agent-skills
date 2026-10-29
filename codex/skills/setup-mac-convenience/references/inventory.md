# Original Mac environment inventory — 2026-10-29

Survey date: 2026-10-29. This inventory was verified from files and installation metadata, then updated to reflect requested exclusions and changes. Installation does not establish active use or personal installation. Corporate management tools are listed separately.

## 1. Custom commands and shell configuration

| Command or setting | Purpose | Evidence location |
|---|---|---|
| `git-checkout-pr [query]` / `git checkout-pr [query]` | Fetch up to 50 open PRs ordered by most recently updated, select with fzf, and check out. Local branches use `pr-number-author-branch`. Requires `gh`, `jq`, and `fzf` | `~/.local/bin/git-checkout-pr` |
| `zz keyword` / `zi keyword` | Select a directory from zoxide history with fzf and navigate to it | `~/.zshrc` |
| `z keyword` | Navigate directly to the directory selected by zoxide. Existing fasd directory history was imported | `~/.zshrc` |
| `a`, `s`, `d`, `f`, `sd`, `sf` | fasd file and directory search: all entries, interactive search, directories, files, interactive directory selection, and interactive file selection, respectively | `~/.zshrc:108` |
| `j` | Alias for zoxide interactive navigation, `zi` | `~/.zshrc` |
| `ls` → `eza` | List files with eza | `~/.zshrc:107` |
| `l`, `ll`, `la`, `lsa` | File listing aliases provided by Oh My Zsh | `~/.oh-my-zsh/lib/directories.zsh` |
| Oh My Zsh | `robbyrussell` theme with `git` and `fasd` plugins. fasd preserves existing file and directory search aliases; navigation uses zoxide | `~/.zshrc:11`, `~/.zshrc:73` |
| zsh-autosuggestions | Suggest commands based on previous input | `~/.zshrc:77`, `~/.zsh/zsh-autosuggestions/` |
| fzf | Fuzzy search and shell completion; `Ctrl-R` for command history, `Ctrl-T` for file selection, and `Option-C` for directory selection | `source <(fzf --zsh)` in `~/.fzf.zsh` |
| Navigate by entering a directory path | Oh My Zsh `auto_cd` | `~/.oh-my-zsh/lib/directories.zsh` |
| `...`, `....`, `.....`, `......` | Shortcuts for ancestor directory paths | Same file |
| `-`, `1`–`9` | Navigate to the previous directory or entries in the directory stack | Same file |
| `md`, `rd` | Aliases for `mkdir -p` and `rmdir` | Same file |
| Shared shell history and duplicate handling | Oh My Zsh defaults, including shared history across terminals and suppression of consecutive duplicates | `~/.oh-my-zsh/lib/history.zsh` |
| User executable paths | Add `~/.local/bin` and `~/.cargo/bin` to PATH | `~/.zshrc:97` |
| Homebrew initialization | Configure Homebrew executable paths and environment | `~/.zprofile:5` |
| bison path precedence | Prepend Homebrew bison to PATH | `~/.zshrc:123` |

## 2. Git and GitHub convenience settings

| Item | Purpose or current setting | Evidence location |
|---|---|---|
| `git done` | Switch to `main` and delete the previous branch with `git branch -d`. Fall back to `master` if local `main` is absent. Exit if already on the target branch | `~/.gitconfig:17` |
| `gh co` | Alias for `gh pr checkout` | `~/.config/gh/config.yml:10` |
| `git subrepo` | Manage another repository in a subdirectory; initialize executable paths, manual pages, and completion | `~/.zshrc:124`, `~/IdeaProjects/git-subrepo/.rc` |
| `difft` / difftastic | Syntax-aware diff configured as Git's external diff tool | `~/.gitconfig:9` |
| GPG commit signing | `commit.gpgsign=true` | `~/.gitconfig:5` |
| pinentry-mac | Use a macOS dialog for GPG passphrase entry | `~/.gnupg/gpg-agent.conf` |
| Separate corporate and personal Git settings | Apply separate Git identity and signing settings to repositories under `~/ghe/` | `~/.gitconfig:15`, `~/.gitconfig-ghe` |
| Fast-forward-only pulls | `pull.ff=only` | `~/.gitconfig:7` |
| Keychain credential storage | `credential.helper=osxkeychain` | `~/.gitconfig` |
| Default Git editor | `/usr/bin/vim` | `~/.gitconfig:13` |

Common aliases from the Oh My Zsh `git` plugin:

| Alias | Command |
|---|---|
| `g` | `git` |
| `ga`, `gaa` | `git add`, `git add --all` |
| `gst`, `gss` | `git status`, `git status --short` |
| `gco`, `gcb`, `gcm` | Checkout, checkout a new branch, checkout the default branch |
| `gb`, `gba`, `gbd` | List branches, list all branches, delete a branch |
| `gd`, `gds`, `gdca` | Diff, staged diff, cached diff |
| `gcmsg`, `gcam` | Commit with a message, commit including tracked file changes |
| `gf`, `gl`, `gp` | Fetch, pull, push |
| `gpr` | Pull with rebase |
| `grb`, `grbi` | Rebase, interactive rebase |
| `gcp` | Cherry-pick |
| `glg`, `glgg`, `glo` | Log with statistics, graph log, one-line log |
| `grs`, `gstp` | Restore, stash pop |

Full plugin definitions: `~/.oh-my-zsh/plugins/git/git.plugin.zsh`. These aliases come from the enabled plugin; they were not individually written by the user.

## 3. Mac convenience apps and settings

| Item | Purpose or verified setting |
|---|---|
| Alfred | App launcher and file search. Installation and shortcut configuration files exist |
| Flycut | Clipboard history. Shortcut: `⌘⇧V`; its own launch-at-startup setting is false |
| Magnet | Window positioning and resizing. A login launch setting exists |
| KeepingYouAwake | Prevent Mac sleep. Configured to activate when the app launches |
| Rocket | Emoji input |
| DeepL | Translation app |
| MacWhisper | Audio transcription |
| CameraController | Adjust USB camera settings |
| Ammonite | Tag visualization and search |
| iTerm2 | Terminal. Left Option acts as Esc+; Option-Left/Right send Esc-b/Esc-f; 100,000-line scrollback; Monaco 12 |
| Screenshot location | Set to `~/Pictures/screenshots` |
| Finder | Saved default view is list view |
| User-installed fonts | Hack, Inter, LINE Seed Sans, LINE Seed JP |
| 1Password / Bitwarden | Password managers. 1Password native messaging integration files also exist for Chrome and Firefox |
| Google Drive / Box / OneDrive | File synchronization apps |

Evidence: `/Applications`, `~/Applications`, `~/Library/Preferences`, `~/Library/Containers/*/Data/Library/Preferences`, and `~/Library/Fonts`.

## 4. Development environment

| Item | Purpose or current state |
|---|---|
| SDKMAN! | Java version management with shell initialization enabled. Current version: `25.0.1-tem`; installed candidates include Java 8, 11, 13, 17, 18, 19, 20, 21, and 25 |
| Homebrew | CLI and selected GUI package management |
| `uv`, `uvx` | Python package management and tool execution. Installed in `~/.local/bin` |
| pipx | Isolated Python CLI installation. A selenium environment and wsdump executable link were found |
| pyenv | Installed, with a Python 2.7.18 environment. Initialization was not found in the inspected zsh startup files |
| JetBrains Toolbox | IDE management |
| IntelliJ IDEA / GoLand / CLion / PyCharm / WebStorm | Installed in the user's Applications directory |
| Docker Desktop | Executable links for Docker, Compose, kubectl, and related tools |

Global npm packages: `retire`, `ts-node`, `typescript`, and `npm`.
User CLI in the Cargo executable directory: `svgbob_cli`.

## 5. Findings from the installed environment

- eza 0.23.5 can produce empty output with noninteractive input when no path is supplied. This upstream behavior was verified. The `ls`, `l`, `ll`, `la`, and `lsa` aliases passed verification in a normal terminal. In scripts and noninteractive runs, supply a path such as `eza .` or `ls .`. Reference: [eza #1568](https://github.com/eza-community/eza/issues/1568).

- Update on 2026-10-29: exa was removed and replaced with eza 0.23.5; fzf was updated to 0.74.5; zoxide 0.10.0 was installed. A total of 264 valid directory entries were imported from fasd into zoxide, and `z`, `zz`, and `j` were migrated. fasd 1.0.1 and its plugin were retained to preserve `a`, `s`, `d`, `f`, `sd`, and `sf`. Dependency versions installed or updated by Homebrew are also reflected below.

- `direnv` is installed, but the inspected zsh startup files have no `direnv hook`. Automatic shell integration could not be established from this evidence.
- `stow` is installed. This survey found no evidence establishing whether it is actively used to manage dotfiles.
- `git-checkout-pr` was fixed after the survey. Changes addressed PR number detection, queries containing spaces, result selection, existing branch detection, and exit status handling, and were applied to the installed command. It passed 19 regression tests with local Git repositories, macOS default Bash compatibility checks, ShellCheck, and independent verification.
- The custom user script identified in `~/.local/bin` was `git-checkout-pr`. Other entries were installed programs or links.
- No additional user automation files were found in the inspected `~/Library/Services` or iTerm2 Scripts/DynamicProfiles directories.
- LaunchAgents included entries for Box, Google updates, JetBrains Toolbox, and Pulse Secure. No separate personal automation jobs were found there.
- Jamf/Self Service, Falcon, Cisco, Ivanti, and `nfvctl` may relate to corporate environments or device management; they were not classified as personal convenience settings.

## 6. Installed Homebrew packages

This list is based on installation metadata from `brew info --json=v2 --installed`, with requested exclusions applied. “Installed on request” is Homebrew's `installed_on_request` value; it does not identify who installed a package or establish active use. Library dependencies are included. Multiple versions include older versions retained by Homebrew; the active fzf version is 0.74.5.

| Package | Installed version | Installed on request | Description |
|---|---|---|---|
| `ada-url` | 3.4.4 | No | WHATWG-compliant and fast URL parser written in modern C++ |
| `ansible` | 11.1.0_1 | Yes | Automate deployment, configuration, and upgrading |
| `ant` | 1.10.15_1 | Yes | Java build tool |
| `aom` | 3.11.0 | Yes | Codec library for encoding and decoding AV1 video streams |
| `argocd` | 2.6.0 | Yes | GitOps Continuous Delivery for Kubernetes |
| `autoconf` | 2.72 | No | Automatic configure script builder |
| `bash` | 5.2 | Yes | Bourne-Again SHell, a UNIX command interpreter |
| `bazel` | 7.4.1 | Yes | Google's own build tool |
| `bison` | 3.8.2 | Yes | Parser generator |
| `bottom` | 0.6.8 | Yes | Yet another cross-platform graphical process/system monitor |
| `brotli` | 1.2.0 | No | Generic-purpose lossless compression algorithm by Google |
| `c-ares` | 1.34.6 | No | Asynchronous DNS library |
| `ca-certificates` | 2026-05-14, 2026-10-20 | No | Mozilla CA certificate store |
| `cairo` | 1.18.2 | No | Vector graphics library with cross-device output support |
| `certifi` | 2024.12.14 | No | Mozilla CA bundle for Python |
| `cffi` | 1.17.1_1 | No | C Foreign Function Interface for Python |
| `chafa` | 1.14.5 | Yes | Versatile and fast Unicode/ASCII/ANSI graphics renderer |
| `cmake` | 3.24.2 | Yes | Cross-platform make |
| `cryptography` | 44.0.0 | No | Cryptographic recipes and primitives for Python |
| `difftastic` | 0.36.1 | Yes | Diff that understands syntax |
| `direnv` | 2.32.1 | Yes | Load/unload environment variables based on $PWD |
| `docker-credential-helper` | 0.7.0 | Yes | Platform keystore credential helper for Docker |
| `dog` | 0.1.0 | Yes | Command-line DNS client |
| `expat` | 2.7.1 | No | XML 1.0 parser |
| `eza` | 0.23.5 | Yes | Modern, maintained replacement for ls |
| `fasd` | 1.0.1 | Yes | CLI tool for quick access to files and directories |
| `fmt` | 12.1.0 | No | Open-source formatting library for C++ |
| `fnt` | 1.8 | Yes | Apt for fonts, the missing font manager for macOS/linux |
| `fontconfig` | 2.15.0 | No | XML-based font configuration API for X Windows |
| `freetype` | 2.13.3 | No | Software library to render fonts |
| `fribidi` | 1.0.16 | No | Implementation of the Unicode BiDi algorithm |
| `fzf` | 0.33.0, 0.74.5 | Yes | Command-line fuzzy finder written in Go |
| `gd` | 2.3.3_6 | No | Graphics library to dynamically manipulate images |
| `gdk-pixbuf` | 2.42.12 | Yes | Toolkit for image loading and pixel buffer manipulation |
| `gettext` | 1.0 | No | GNU internationalization (i18n) and localization (l10n) library |
| `gh` | 2.36.0 | Yes | GitHub command-line tool |
| `ghz` | 0.120.0 | Yes | Simple gRPC benchmarking and load testing tool |
| `giflib` | 5.2.2 | No | Library and utilities for processing GIFs |
| `git-filter-repo` | 2.47.0 | Yes | Quickly rewrite git repository history |
| `git-number` | 1.0.1 | Yes | Use numbers for dealing with files in git |
| `glib` | 2.82.4 | No | Core application library for C |
| `gmp` | 6.3.0 | No | GNU multiple precision arithmetic library |
| `gnupg` | 2.4.7 | Yes | GNU Privacy Guard (OpenPGP) |
| `gnutls` | 3.8.4 | Yes | GNU Transport Layer Security (TLS) Library |
| `gradle` | 7.5.1_1 | Yes | Open-source build automation tool based on the Groovy and Kotlin DSL |
| `graphite2` | 1.3.14 | No | Smart font renderer for non-Roman scripts |
| `graphviz` | 12.2.1 | Yes | Graph visualization software from AT&T and Bell Labs |
| `grpcurl` | 1.9.3 | Yes | Like cURL, but for gRPC |
| `gts` | 0.7.6_3 | No | GNU triangulated surface library |
| `harfbuzz` | 10.1.0 | No | OpenType text shaping engine |
| `hdrhistogram_c` | 0.11.9 | No | C port of the HdrHistogram |
| `helm` | 3.11.1 | Yes | Kubernetes package manager |
| `highway` | 1.2.0 | No | Performance-portable, length-agnostic SIMD with runtime dispatch |
| `icu4c@75` | 75.1 | No | C/C++ and Java libraries for Unicode and globalization |
| `icu4c@76` | 76.1_1 | No | C/C++ and Java libraries for Unicode and globalization |
| `icu4c@78` | 78.3 | No | C/C++ and Java libraries for Unicode and globalization |
| `imath` | 3.1.12 | No | Library of 2D and 3D vector, matrix, and math operations |
| `jasper` | 4.2.4 | No | Library for manipulating JPEG-2000 images |
| `jpeg-turbo` | 3.1.0 | No | JPEG image codec that aids compression and decompression |
| `jpeg-xl` | 0.11.1 | Yes | New file format for still image compression |
| `jq` | 1.6 | Yes | Lightweight and flexible command-line JSON processor |
| `jwt-cli` | 6.2.0 | Yes | Super fast CLI tool to decode and encode JWTs built in Rust |
| `kubernetes-cli` | 1.26.1 | Yes | Kubernetes command-line interface |
| `lcdf-typetools` | 2.110 | No | Manipulate OpenType and multiple-master fonts |
| `libassuan` | 3.0.2 | No | Assuan IPC Library |
| `libavif` | 1.1.1 | Yes | Library for encoding and decoding .avif files |
| `libdeflate` | 1.22 | No | Heavily optimized DEFLATE/zlib/gzip compression and decompression |
| `libevent` | 2.1.12_1 | No | Asynchronous event library |
| `libgcrypt` | 1.10.3 | No | Cryptographic library based on the code from GnuPG |
| `libgit2` | 1.9.7_2 | No | C library of Git core methods that is re-entrant and linkable |
| `libgit2@1.8` | 1.8.4 | No | C library of Git core methods that is re-entrant and linkable |
| `libgpg-error` | 1.61 | No | Common error values for all GnuPG components |
| `libidn2` | 2.3.7 | No | International domain name library (IDNA2008, Punycode and TR46) |
| `libksba` | 1.6.7 | Yes | X.509 and CMS library |
| `libnghttp2` | 1.69.0 | No | HTTP/2 C Library |
| `libnghttp3` | 1.16.0 | No | HTTP/3 library written in C |
| `libngtcp2` | 1.23.0 | No | IETF QUIC protocol implementation |
| `libpng` | 1.6.45 | No | Library for manipulating PNG images |
| `librsvg` | 2.58.4 | Yes | Library to render SVG files using Cairo |
| `libsodium` | 1.0.20 | No | NaCl networking and cryptography library |
| `libssh` | 0.11.1 | No | C library SSHv1/SSHv2 client and server protocols |
| `libssh2` | 1.11.1, 1.11.1_7 | No | C library implementing the SSH2 protocol |
| `libtasn1` | 4.19.0 | No | ASN.1 structure parser library |
| `libtiff` | 4.7.0 | Yes | TIFF library and utilities |
| `libtool` | 2.5.4 | No | Generic library support script |
| `libunistring` | 1.4.2 | No | C string library for manipulating Unicode strings |
| `libusb` | 1.0.27 | No | Library for USB device access |
| `libuv` | 1.52.1 | No | Multi-platform support library with a focus on asynchronous I/O |
| `libvmaf` | 3.0.0 | No | Perceptual video quality assessment based on multi-method fusion |
| `libx11` | 1.8.10 | No | X.Org: Core X11 protocol client library |
| `libxau` | 1.0.12 | No | X.Org: A Sample Authorization Protocol for X |
| `libxcb` | 1.17.0 | No | X.Org: Interface to the X Window System protocol |
| `libxdmcp` | 1.1.5 | No | X.Org: X Display Manager Control Protocol library |
| `libxext` | 1.3.6 | No | X.Org: Library for common extensions to the X11 protocol |
| `libxrender` | 0.9.12 | No | X.Org: Library for the Render Extension to the X11 protocol |
| `libyaml` | 0.2.5 | No | YAML Parser |
| `little-cms2` | 2.16 | Yes | Color management engine supporting ICC profiles |
| `llhttp` | 9.4.1, 9.4.3 | No | Port of http_parser to llparse |
| `llvm` | 19.1.6 | No | Next-gen compiler infrastructure |
| `lz4` | 1.10.0 | No | Extremely Fast Compression algorithm |
| `lzo` | 2.10 | No | Real-time data compression library |
| `m4` | 1.4.19 | No | Macro processing language |
| `maven` | 3.9.9 | Yes | Java-based project management |
| `merve` | 1.2.2_1 | No | C++ lexer for extracting named exports from CommonJS modules |
| `mpdecimal` | 4.0.1 | No | Library for decimal floating point arithmetic |
| `nbytes` | 0.1.4 | No | Library of byte handling functions extracted from Node.js core |
| `ncurses` | 6.5 | No | Text-based UI library |
| `netpbm` | 11.02.11 | Yes | Image manipulation |
| `nettle` | 3.9.1, 3.10 | No | Low-level cryptographic library |
| `node` | 26.0.0 | Yes | Open-source, cross-platform JavaScript runtime environment |
| `npth` | 1.8 | No | New GNU portable threads library |
| `oniguruma` | 6.9.8 | No | Regular expressions library |
| `openexr` | 3.3.2 | No | High dynamic-range image file format |
| `openjdk` | 23.0.1 | Yes | Development kit for the Java programming language |
| `openjdk@11` | 11.0.25 | Yes | Development kit for the Java programming language |
| `openjdk@17` | 17.0.4.1 | No | Development kit for the Java programming language |
| `openjdk@21` | 21.0.5 | No | Development kit for the Java programming language |
| `openssl@1.1` | 1.1.1u | No | Cryptography and SSL/TLS Toolkit |
| `openssl@3` | 3.6.2 | No | Cryptography and SSL/TLS Toolkit |
| `openssl@4` | 4.1.0 | No | Cryptography and SSL/TLS Toolkit |
| `p11-kit` | 0.25.5 | No | Library to load and enumerate PKCS#11 modules |
| `pandoc` | 2.19.2 | Yes | Swiss-army knife of markup format conversion |
| `pango` | 1.56.0 | No | Framework for layout and rendering of i18n text |
| `pcre2` | 10.44 | No | Perl compatible regular expressions library with a new API |
| `pinentry` | 1.3.1_1 | No | Passphrase entry dialog utilizing the Assuan protocol |
| `pinentry-mac` | 1.3.1.1 | Yes | Pinentry for GPG on Mac |
| `pipx` | 1.7.1_1 | Yes | Execute binaries from Python packages in isolated environments |
| `pixman` | 0.44.2 | No | Low-level library for pixel manipulation |
| `pkgconf` | 2.5.1 | No | Package compiler and linker metadata toolkit |
| `pycparser` | 2.22_1 | No | C parser in Python |
| `pyenv` | 2.5.0 | Yes | Python version management |
| `pytest` | 8.4.2 | Yes | Simple powerful testing with Python |
| `python-packaging` | 24.2 | No | Core utilities for Python packages |
| `python@3.13` | 3.13.1 | Yes | Interpreted, interactive, object-oriented programming language |
| `python@3.14` | 3.14.0 | No | Interpreted, interactive, object-oriented programming language |
| `readline` | 8.3.3 | No | Library for command-line editing |
| `ripgrep` | 13.0.0 | Yes | Search tool like grep and The Silver Searcher |
| `rust` | 1.84.0 | Yes | Safe, concurrent, practical language |
| `selenium-server` | 4.27.0 | Yes | Browser automation for testing purposes |
| `simdjson` | 4.6.4 | No | SIMD-accelerated C++ JSON parser |
| `simdutf` | 9.0.0 | No | Unicode conversion routines, fast |
| `sqlite` | 3.53.1 | No | Command-line interface for SQLite |
| `step` | 0.30.6 | Yes | Crypto and x509 Swiss-Army-Knife |
| `stow` | 2.4.1 | Yes | Organize software neatly under a single directory tree (e.g. /usr/local) |
| `svgbob` | 0.7.2 | Yes | Convert your ascii diagram scribbles into happy little SVG |
| `telnet` | 64 | Yes | User interface to the TELNET protocol |
| `thrift` | 0.17.0 | Yes | Framework for scalable cross-language services development |
| `tig` | 2.5.10 | Yes | Text interface for Git repositories |
| `tree` | 2.0.4 | Yes | Display directories as trees (with optional color/HTML output) |
| `unbound` | 1.22.0 | Yes | Validating, recursive, caching DNS resolver |
| `uvwasi` | 0.0.23 | No | WASI syscall API built atop libuv |
| `webp` | 1.4.0 | Yes | Image format providing lossless and lossy compression for web images |
| `xorgproto` | 2024.1 | No | X.Org: Protocol Headers |
| `xz` | 5.8.3 | No | General-purpose data compression with high compression ratio |
| `yarn` | 1.22.19 | Yes | JavaScript package manager |
| `z3` | 4.13.4 | No | High-performance theorem prover |
| `zoxide` | 0.10.0 | Yes | Shell extension to navigate your filesystem faster |
| `zstd` | 1.5.7_1 | No | Zstandard is a real-time compression algorithm |
| `zx` | 8.8.5 | Yes | Tool for writing better scripts |

Internal tools whose installed files were found in the Cellar in addition to the Homebrew metadata output:

- `athenz-utils` (1.5.167660774): Athenz authentication CLI bundle. Executables: `athenz-conf`, `zms-svctoken`, `zpu`, `zts-accesstoken`, `zts-rolecert`, `zts-roletoken`, and `zts-svccert`.
- `vksctl` (1.20.2): Verda Kubernetes Service management CLI. Executable: `vksctl`.
- `zms-cli` (2.3.0-1): Athenz ZMS CLI. Executable: `zms-cli`.

Homebrew Casks:

| Item | Description |
|---|---|
| `ammonite` | Tag visualiser and search utility |
| `cameracontroller` | Control USB Cameras from an app |
| `docker-desktop` | App to build and share containerised applications and microservices |
| `google-drive` | Client for the Google Drive storage service |
| `keepingyouawake` | Tool to prevent the system from going into sleep mode |

This inventory is a reference for optional components. Follow SKILL.md for the installation sequence on a new Mac. Do not reproduce old versions, executable paths from the previous machine, or transitive dependencies verbatim.
