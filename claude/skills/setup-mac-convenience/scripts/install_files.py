#!/usr/bin/env python3
import argparse
import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
INCLUDE = "~/.config/mac-convenience/gitconfig"


def append_line(content, line):
    if line in content.splitlines():
        return content
    return content.rstrip("\n") + ("\n" if content else "") + line + "\n"


def read_existing(path, home):
    if path.is_symlink():
        raise ValueError(f"Merge this symlink through its dotfiles manager: {path}")
    try:
        path.resolve().relative_to(home)
    except ValueError:
        raise ValueError(f"Target escapes the selected home: {path}") from None
    if path.exists() and not path.is_file():
        raise ValueError(f"Target is not a regular file: {path}")
    return path.read_bytes() if path.exists() else None


def plan(home):
    mappings = {
        ".local/bin/git-checkout-pr": ("bin/git-checkout-pr", 0o755),
        ".local/bin/git-done": ("bin/git-done", 0o755),
        ".local/bin/fasd": ("vendor/fasd/fasd", 0o755),
        ".local/share/mac-convenience/fasd-LICENSE": ("vendor/fasd/LICENSE", 0o644),
        ".config/mac-convenience/homebrew.zsh": ("homebrew.zsh", 0o644),
        ".config/mac-convenience/shell.zsh": ("shell.zsh", 0o644),
        ".config/mac-convenience/gitconfig": ("gitconfig", 0o644),
    }
    desired = {
        home / target: ((ASSETS / source).read_bytes(), mode)
        for target, (source, mode) in mappings.items()
    }
    for name, source in ((".zprofile", "homebrew.zsh"), (".zshrc", "shell.zsh")):
        path = home / name
        current = read_existing(path, home)
        line = f'source "$HOME/.config/mac-convenience/{source}"'
        content = append_line(current.decode() if current is not None else "", line)
        mode = stat.S_IMODE(path.stat().st_mode) if current is not None else 0o600
        desired[path] = (content.encode(), mode)
    gitconfig = home / ".gitconfig"
    current = read_existing(gitconfig, home)
    includes = []
    if current is not None:
        result = subprocess.run(
            ["git", "config", "--file", str(gitconfig), "--get-all", "include.path"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode not in (0, 1):
            raise ValueError(f"Cannot parse existing Git configuration: {gitconfig}")
        includes = result.stdout.splitlines()
    content = current.decode() if current is not None else ""
    if INCLUDE not in includes:
        content = content.rstrip("\n") + ("\n" if content else "")
        content += f"[include]\n\tpath = {INCLUDE}\n"
    mode = stat.S_IMODE(gitconfig.stat().st_mode) if current is not None else 0o600
    desired[gitconfig] = (content.encode(), mode)
    changes = []
    for path, (content, mode) in desired.items():
        old = read_existing(path, home)
        old_mode = stat.S_IMODE(path.stat().st_mode) if old is not None else None
        if old != content or old_mode != mode:
            changes.append((path, content, mode, old))
    return changes


def apply(home, changes):
    backup = None
    if any(old is not None for _, _, _, old in changes):
        backup_parent = home / ".local/state/mac-convenience/backups"
        read_existing(backup_parent / ".path-check", home)
        backup_parent.mkdir(parents=True, exist_ok=True)
        backup = Path(tempfile.mkdtemp(prefix="install-", dir=backup_parent))
        for path, _, _, old in changes:
            if old is not None:
                target = backup / path.relative_to(home)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
                target.chmod(0o600)
    for path, content, mode, _ in changes:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(
            prefix=".mac-convenience-", dir=path.parent
        )
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(content)
                os.fchmod(stream.fileno(), mode)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return backup


def main():
    parser = argparse.ArgumentParser(
        description="Install bundled shell/Git files; preview unless --apply is set."
    )
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    if not home.is_dir() or home == Path(home.anchor):
        parser.error("--home must be an existing non-root directory")
    try:
        changes = plan(home)
        for path, _, _, _ in changes:
            print(f"{'WRITE' if args.apply else 'WOULD WRITE'} {path}")
        if args.apply:
            backup = apply(home, changes)
            if backup:
                print(f"BACKUP {backup}")
        if not changes:
            print("Already installed; no files changed.")
    except (OSError, ValueError, UnicodeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
