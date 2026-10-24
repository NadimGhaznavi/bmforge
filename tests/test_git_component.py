"""Integration tests for the self-contained Git component template."""

import fcntl
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bmforge_git", ROOT / "components/templates/git/Git.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
Git = MODULE.Git


class GitComponentTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="bmforge-git-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "checkout"
        self.git(self.root, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.git(self.root, "clone", str(self.remote), str(self.repo))
        self.git(self.repo, "config", "user.name", "Test")
        self.git(self.repo, "config", "user.email", "test@example.invalid")
        (self.repo / "README.md").write_text("original\n")
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-m", "Initialize")
        self.git(self.repo, "push", "-u", "origin", "main")
        self.client = Git(self.repo, managed_paths=("index.md", "reports/report.csv"))

    @staticmethod
    def git(directory, *args):
        return subprocess.run(["git", "-C", str(directory), *args],
                              check=True, capture_output=True, text=True).stdout.strip()

    def test_commit_stages_everything_and_pushes(self):
        (self.repo / "README.md").write_text("changed\n")
        (self.repo / "new.txt").write_text("added\n")
        staged, committed = self.client.commit("Record changes")
        self.assertIn("new.txt", staged)
        self.assertIn("Record changes", committed)
        self.assertEqual(self.git(self.remote, "show", "main:README.md"), "changed")
        self.assertEqual(self.git(self.remote, "show", "main:new.txt"), "added")

    def test_commit_without_changes_fails_visibly(self):
        with self.assertRaisesRegex(RuntimeError, "Git commit failed"):
            self.client.commit("Nothing to commit")

    def test_commit_push_failure_is_not_reported_as_success(self):
        (self.repo / "new.txt").write_text("added\n")
        hook = self.remote / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        with self.assertRaisesRegex(RuntimeError, "Git push failed"):
            self.client.commit("Local commit remains")
        self.assertEqual(self.git(self.repo, "log", "-1", "--pretty=%s"), "Local commit remains")

    def test_publish_managed_files_and_skip_unchanged(self):
        content = {"index.md": "hello\n", "reports/report.csv": "a,b\n1,2\n"}
        self.assertTrue(self.client.publish(content, "Publish site"))
        remote_head = self.git(self.remote, "rev-parse", "main")
        self.assertFalse(self.client.publish(content, "Publish site"))
        self.assertEqual(remote_head, self.git(self.remote, "rev-parse", "main"))
        self.assertEqual(self.git(self.remote, "show", "main:index.md"), "hello")

    def test_publish_refuses_dirty_checkout_and_other_paths(self):
        (self.repo / "unexpected.txt").write_text("do not overwrite\n")
        with self.assertRaisesRegex(RuntimeError, "must be clean"):
            self.client.publish({"index.md": "hello\n"}, "Publish")
        (self.repo / "unexpected.txt").unlink()
        with self.assertRaisesRegex(ValueError, "Not a managed publishing path"):
            self.client.publish({"unexpected.txt": "hello\n"}, "Publish")

    def test_publish_retries_failed_push_without_new_commit(self):
        hook = self.remote / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        with self.assertRaisesRegex(RuntimeError, "Git push failed"):
            self.client.publish({"index.md": "hello\n"}, "Publish")
        local_head = self.git(self.repo, "rev-parse", "HEAD")
        hook.unlink()
        self.assertTrue(self.client.publish({"index.md": "hello\n"}, "Publish"))
        self.assertEqual(local_head, self.git(self.remote, "rev-parse", "main"))

    def test_publish_refuses_wrong_branch(self):
        self.git(self.repo, "switch", "-c", "dev")
        with self.assertRaisesRegex(RuntimeError, "must be on main"):
            self.client.publish({"index.md": "hello\n"}, "Publish")

    def test_publish_refuses_concurrent_worker(self):
        with (self.repo / ".git/bmforge-git-publish.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(BlockingIOError):
                self.client.publish({"index.md": "hello\n"}, "Publish")


if __name__ == "__main__":
    unittest.main()
