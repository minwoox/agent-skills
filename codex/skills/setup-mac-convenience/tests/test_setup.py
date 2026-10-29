import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install_files.py"


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mac-setup-test-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home with spaces"
        self.home.mkdir()
        self.env = {
            "HOME": str(self.home),
            "XDG_CONFIG_HOME": str(self.home / ".config"),
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "Fixture",
            "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Fixture",
            "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        }

    def install(self, apply=True):
        args = [sys.executable, str(INSTALLER), "--home", str(self.home)]
        if apply:
            args.append("--apply")
        return subprocess.run(
            args, env=self.env, text=True, capture_output=True, timeout=10, check=False
        )

    def git(self, *args, cwd=None, check=True):
        return subprocess.run(
            ["git", *args],
            env=self.env,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=check,
            timeout=10,
        )

    def test_preview_does_not_create_files(self):
        result = self.install(apply=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WOULD WRITE", result.stdout)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_homebrew_environment_is_initialized_when_brew_is_already_on_path(self):
        binary_dir = self.home / "bin"
        binary_dir.mkdir()
        brew = binary_dir / "brew"
        brew.write_text(
            '#!/bin/sh\n[ "$1" = shellenv ] || exit 2\n'
            'printf "%s\\n" "export HOMEBREW_PREFIX=/fixture-prefix"\n'
        )
        brew.chmod(0o755)
        env = self.env | {"PATH": str(binary_dir) + os.pathsep + self.env["PATH"]}
        result = subprocess.run(
            [
                "/bin/zsh",
                "-fc",
                'source "$1"; print -r -- ${HOMEBREW_PREFIX-unset}',
                "zsh",
                str(ROOT / "assets/homebrew.zsh"),
            ],
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "/fixture-prefix")

    def test_fresh_install_is_executable_and_git_include_works(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("git-checkout-pr", "git-done", "fasd"):
            path = self.home / ".local/bin" / name
            self.assertTrue(os.access(path, os.X_OK))
        self.assertEqual(
            self.git(
                "config", "--global", "--includes", "--get", "pull.ff"
            ).stdout.strip(),
            "only",
        )
        self.assertEqual(
            self.git(
                "config", "--global", "--includes", "--get", "diff.external"
            ).stdout.strip(),
            "difft",
        )
        expected = (ROOT / "assets/bin/git-checkout-pr").read_bytes()
        self.assertEqual(
            (self.home / ".local/bin/git-checkout-pr").read_bytes(), expected
        )
        for path in [
            self.home / ".zshrc",
            self.home / ".zprofile",
            *self.home.glob(".config/mac-convenience/*.zsh"),
        ]:
            subprocess.run(
                ["/bin/zsh", "-n", str(path)], check=True, capture_output=True
            )

    def test_reinstall_has_no_writes_or_new_backups(self):
        self.assertEqual(self.install().returncode, 0)
        before = {
            p.relative_to(self.home): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in self.home.rglob("*")
            if p.is_file()
        }
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no files changed", result.stdout)
        after = {
            p.relative_to(self.home): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in self.home.rglob("*")
            if p.is_file()
        }
        self.assertEqual(before, after)

    def test_existing_settings_are_preserved_and_backed_up(self):
        zshrc = self.home / ".zshrc"
        zshrc.write_text("export EXISTING_SETTING=fixture")
        gitconfig = self.home / ".gitconfig"
        gitconfig.write_text("[user]\n\tname = Existing User\n")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            zshrc.read_text().startswith("export EXISTING_SETTING=fixture\n")
        )
        self.assertEqual(
            self.git(
                "config", "--global", "--includes", "--get", "user.name"
            ).stdout.strip(),
            "Existing User",
        )
        backups = list(self.home.glob(".local/state/mac-convenience/backups/install-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(
            (backups[0] / ".zshrc").read_text(), "export EXISTING_SETTING=fixture"
        )
        self.assertEqual(stat.S_IMODE(backups[0].stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE((backups[0] / ".zshrc").stat().st_mode), 0o600)

    def test_symlink_refused_before_any_installation(self):
        external = Path(self.temp.name) / "external"
        external.write_text("keep me\n")
        (self.home / ".zshrc").symlink_to(external)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr)
        self.assertEqual(external.read_text(), "keep me\n")
        self.assertFalse((self.home / ".local").exists())

    def test_escaping_parent_symlink_refused_before_writes(self):
        external = Path(self.temp.name) / "external"
        external.mkdir()
        (self.home / ".local").symlink_to(external, target_is_directory=True)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("escapes", result.stderr)
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse((self.home / ".zshrc").exists())

    def test_malformed_git_config_refused_before_writes(self):
        (self.home / ".gitconfig").write_text("[broken\n")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot parse", result.stderr)
        self.assertFalse((self.home / ".local").exists())

    def test_missing_execute_bit_is_repaired(self):
        self.assertEqual(self.install().returncode, 0)
        command = self.home / ".local/bin/git-checkout-pr"
        command.chmod(0o600)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.access(command, os.X_OK))

    def repository(self, base):
        self.assertEqual(self.install().returncode, 0)
        repo = self.home / "repository"
        repo.mkdir()
        self.git("init", "-q", "-b", base, cwd=repo)
        self.git(
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--allow-empty",
            "-qm",
            "Base",
            cwd=repo,
        )
        self.env["PATH"] = str(self.home / ".local/bin") + os.pathsep + self.env["PATH"]
        return repo

    def test_git_done_switches_to_main_and_deletes_merged_branch(self):
        repo = self.repository("main")
        self.git("checkout", "-qb", "topic", cwd=repo)
        self.git("done", cwd=repo)
        self.assertEqual(
            self.git("branch", "--show-current", cwd=repo).stdout.strip(), "main"
        )
        self.assertNotEqual(
            self.git(
                "show-ref", "--verify", "refs/heads/topic", cwd=repo, check=False
            ).returncode,
            0,
        )

    def test_git_done_master_and_already_on_base(self):
        repo = self.repository("master")
        self.git("checkout", "-qb", "topic", cwd=repo)
        self.git("done", cwd=repo)
        self.assertEqual(
            self.git("branch", "--show-current", cwd=repo).stdout.strip(), "master"
        )
        self.assertIn("Already on master", self.git("done", cwd=repo).stdout)

    def test_git_done_preserves_unmerged_branch(self):
        repo = self.repository("main")
        self.git("checkout", "-qb", "topic", cwd=repo)
        self.git(
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--allow-empty",
            "-qm",
            "Topic",
            cwd=repo,
        )
        result = self.git("done", cwd=repo, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            self.git("show-ref", "--verify", "refs/heads/topic", cwd=repo).returncode, 0
        )

    def test_git_done_preserves_detached_head(self):
        repo = self.repository("main")
        self.git("checkout", "--detach", "-q", cwd=repo)
        result = self.git("done", cwd=repo, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(
            self.git("branch", "--show-current", cwd=repo).stdout.strip(), ""
        )


if __name__ == "__main__":
    unittest.main()
