import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(sys.argv.pop(1)).resolve()
BASH = os.environ.get("CHECKOUT_PR_BASH", "/bin/bash")
REAL_GIT = "/usr/bin/git"
REAL_FZF = shutil.which("fzf")
if REAL_FZF is None:
    raise SystemExit("Install fzf before running these integration tests.")

GH_FIXTURE = r"""#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
args = sys.argv[1:]
with open(os.environ['PR_CALL_LOG'], 'a') as log:
    log.write(json.dumps(['gh', *args]) + '\n')
operation = args[:2]
if operation == ['pr', 'list']:
    if os.environ.get('PR_LIST_ERROR'):
        print('fixture: PR list failed', file=sys.stderr)
        sys.exit(7)
    print(Path(os.environ['PR_LIST_JSON']).read_text())
elif operation == ['pr', 'view']:
    if os.environ.get('PR_VIEW_ERROR'):
        print('fixture: PR view failed', file=sys.stderr)
        sys.exit(8)
    print(json.dumps({'headRepositoryOwner': None if os.environ.get('PR_DELETED_OWNER') else {'login': 'fixture'}, 'headRefName': 'topic', 'url': 'https://example.invalid/pull/' + args[2]}))
elif operation == ['pr', 'checkout']:
    if os.environ.get('PR_CHECKOUT_ERROR'):
        print('fixture: PR checkout failed', file=sys.stderr)
        sys.exit(9)
    subprocess.run(['/usr/bin/git', 'fetch', '-q', 'origin', 'refs/heads/topic'], check=True)
    subprocess.run(['/usr/bin/git', 'checkout', '-q', '-b', args[4], 'FETCH_HEAD'], check=True)
else:
    print('unexpected gh arguments: ' + repr(args), file=sys.stderr)
    sys.exit(99)
"""

FZF_FIXTURE = r"""#!/usr/bin/env python3
import json, os, sys
with open(os.environ['PR_CALL_LOG'], 'a') as log:
    log.write(json.dumps(['fzf', *sys.argv[1:]]) + '\n')
if os.environ.get('PR_CANCEL'):
    sys.exit(130)
os.execv(os.environ['PR_REAL_FZF'], ['fzf', *sys.argv[1:], '--filter', os.environ.get('PR_SELECT', '#102 ')])
"""


class CheckoutPrTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared = tempfile.TemporaryDirectory(
            prefix="checkout-pr-fixture-", dir="/private/tmp"
        )
        cls.root = Path(cls.shared.name)
        cls.bin = cls.root / "bin"
        cls.bin.mkdir()
        for name, content in [("gh", GH_FIXTURE), ("fzf", FZF_FIXTURE)]:
            path = cls.bin / name
            path.write_text(content)
            path.chmod(0o755)
        cls.base_env = os.environ.copy()
        for name in list(cls.base_env):
            if name.startswith(("GIT_", "GH_", "GITHUB_", "FZF_")):
                cls.base_env.pop(name)
        cls.base_env.update(
            {
                "PATH": str(cls.bin)
                + os.pathsep
                + os.environ.get("PATH", "/usr/bin:/bin"),
                "PR_REAL_FZF": REAL_FZF,
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "Fixture",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            }
        )
        cls.upstream = cls.root / "upstream"
        cls.upstream.mkdir()
        cls.git(cls.upstream, "init", "-q", "-b", "main")
        (cls.upstream / "file").write_text("base\n")
        cls.git(cls.upstream, "add", "file")
        cls.git(cls.upstream, "-c", "commit.gpgsign=false", "commit", "-qm", "Base")
        cls.base_commit = cls.git(cls.upstream, "rev-parse", "HEAD")
        cls.git(cls.upstream, "checkout", "-qb", "topic")
        (cls.upstream / "file").write_text("pull request\n")
        cls.git(
            cls.upstream, "-c", "commit.gpgsign=false", "commit", "-qam", "PR change"
        )
        cls.pr_commit = cls.git(cls.upstream, "rev-parse", "HEAD")
        cls.git(cls.upstream, "checkout", "-q", "main")

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    @classmethod
    def git(cls, directory, *args):
        return subprocess.run(
            [REAL_GIT, *args],
            cwd=directory,
            env=cls.base_env,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.repo = self.work / "repo"
        self.git(self.work, "clone", "-q", str(self.upstream), str(self.repo))
        self.calls_file = self.work / "calls.jsonl"
        self.prs_file = self.work / "prs.json"
        self.env = self.base_env | {
            "PR_CALL_LOG": str(self.calls_file),
            "PR_LIST_JSON": str(self.prs_file),
        }
        self.prs(1)

    def prs(self, count, title="Fix feature"):
        self.prs_file.write_text(
            json.dumps(
                [
                    {"number": 101 + i, "title": title, "author": {"login": "fixture"}}
                    for i in range(count)
                ]
            )
        )

    def run_script(self, *args):
        return subprocess.run(
            [BASH, str(SCRIPT), *args],
            cwd=self.repo,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )

    def calls(self):
        return (
            [json.loads(line) for line in self.calls_file.read_text().splitlines()]
            if self.calls_file.exists()
            else []
        )

    def assert_checkout(self, result, number):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.git(self.repo, "branch", "--show-current"),
            f"pr-{number}-fixture-topic",
        )
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD"), self.pr_commit)
        self.assertEqual((self.repo / "file").read_text(), "pull request\n")

    def assert_unchanged(self):
        self.assertEqual(self.git(self.repo, "branch", "--show-current"), "main")
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD"), self.base_commit)
        self.assertFalse(
            any(call[:3] == ["gh", "pr", "checkout"] for call in self.calls())
        )

    def test_numeric_id_bypasses_search(self):
        self.assert_checkout(self.run_script("1234"), "1234")
        self.assertFalse(any(c[:3] == ["gh", "pr", "list"] for c in self.calls()))

    def test_long_numeric_id_is_preserved(self):
        number = "123456789012345678901234567890"
        self.assert_checkout(self.run_script(number), number)

    def test_zero_is_forwarded_to_github(self):
        self.assert_checkout(self.run_script("0"), "0")
        self.assertEqual(self.calls()[0][:4], ["gh", "pr", "view", "0"])

    def test_equals_is_a_search_keyword(self):
        self.assert_checkout(self.run_script("="), "101")
        self.assertEqual(self.calls()[0][-1], "is:open sort:updated-desc =")

    def test_single_result(self):
        self.assert_checkout(self.run_script(), "101")
        self.assertFalse(any(c[0] == "fzf" for c in self.calls()))

    def test_search_preserves_spaces_and_globs(self):
        query = "author:fixture fix * [bug]"
        self.assert_checkout(self.run_script(query), "101")
        self.assertEqual(self.calls()[0][-1], "is:open sort:updated-desc " + query)

    def test_ten_results_require_selection(self):
        self.prs(10)
        self.assert_checkout(self.run_script(), "102")
        self.assertTrue(any(c[0] == "fzf" for c in self.calls()))

    def test_two_results_select_with_real_fzf(self):
        self.prs(2)
        self.assert_checkout(self.run_script(), "102")

    def test_title_keeps_literal_backslashes(self):
        self.prs(2, title=r"Fix \n and \t and \c")
        self.assert_checkout(self.run_script(), "102")

    def test_no_results_is_an_error_without_checkout(self):
        self.prs(0)
        result = self.run_script("not-found")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No open pull requests", result.stderr)
        self.assert_unchanged()

    def test_list_error_preserves_failure(self):
        self.env["PR_LIST_ERROR"] = "1"
        result = self.run_script("feature")
        self.assertEqual(result.returncode, 7)
        self.assertIn("PR list failed", result.stderr)
        self.assert_unchanged()

    def test_cancel_does_not_checkout(self):
        self.prs(2)
        self.env["PR_CANCEL"] = "1"
        self.assertEqual(self.run_script().returncode, 130)
        self.assert_unchanged()

    def test_view_failure_does_not_checkout(self):
        self.env["PR_VIEW_ERROR"] = "1"
        self.assertEqual(self.run_script("999").returncode, 8)
        self.assert_unchanged()

    def test_checkout_error_is_preserved(self):
        self.env["PR_CHECKOUT_ERROR"] = "1"
        self.assertEqual(self.run_script("999").returncode, 9)
        self.assertEqual(self.git(self.repo, "branch", "--show-current"), "main")

    def test_existing_branch_is_success(self):
        self.git(self.repo, "branch", "pr-999-fixture-topic", self.pr_commit)
        self.assert_checkout(self.run_script("999"), "999")
        self.assertFalse(any(c[:3] == ["gh", "pr", "checkout"] for c in self.calls()))

    def test_already_on_branch_is_success(self):
        self.git(self.repo, "checkout", "-qb", "pr-999-fixture-topic", self.pr_commit)
        self.assert_checkout(self.run_script("999"), "999")

    def test_similar_branch_is_not_a_match(self):
        self.git(self.repo, "branch", "pr-999-fixture-topic-extra")
        self.assert_checkout(self.run_script("999"), "999")

    def test_deleted_owner_stops_before_checkout(self):
        self.env["PR_DELETED_OWNER"] = "1"
        self.assertNotEqual(self.run_script("999").returncode, 0)
        self.assert_unchanged()

    def test_extra_arguments_fail_before_api_calls(self):
        result = self.run_script("one", "two")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stderr)
        self.assertEqual(self.calls(), [])
        self.assert_unchanged()


if __name__ == "__main__":
    unittest.main(verbosity=2)
