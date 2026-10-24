"""Bootstrap tests use only local Git repositories, never remote GitHub or an app."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "skills/bmforge-new-project/scripts/manage.py"
SPEC = importlib.util.spec_from_file_location("bmforge_skill_manager", MANAGER)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def command(*args, cwd=None):
    return subprocess.run([str(value) for value in args], cwd=cwd,
                          capture_output=True, text=True)


def git(repo, *args):
    result = command("git", "-C", repo, *args)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


class SkillBootstrapTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="bmforge-skills-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.source = root / "bmforge"
        self.project = root / "new-app"
        self.source.mkdir()
        self.project.mkdir()
        git(self.source, "init", "-q")
        git(self.source, "config", "user.name", "BMForge Test")
        git(self.source, "config", "user.email", "test@example.invalid")
        git(self.project, "init", "-q")
        for name in module.SKILLS:
            folder = self.source / "skills" / name
            folder.mkdir(parents=True)
            original = ROOT / "skills" / name / "SKILL.md"
            (folder / "SKILL.md").write_bytes(original.read_bytes())
        manager = self.source / "skills/bmforge-new-project/scripts/manage.py"
        manager.parent.mkdir(parents=True)
        manager.write_bytes(MANAGER.read_bytes())
        for common in (*module.COMMON, module.HEALTH):
            path = self.source / common
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {path.name}\n")
        for name, (spec, references) in module.SKILLS.items():
            if spec:
                path = self.source / spec
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f'---\nspec_version: "0.1.0"\n---\n# {name}\n')
            for original in references:
                path = self.source / original
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# Frozen reference: {original}\n")
        for original in (module.DB_TEMPLATE, module.GIT_TEMPLATE, module.CONSTANTS_TEMPLATE,
                         module.LOCALIZER_TEMPLATE, module.TEXT_TEMPLATE, module.EN_CATALOG):
            path = self.source / original
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# Canonical template {original}\n")
        self.commit_source()

    def commit_source(self):
        git(self.source, "add", ".")
        git(self.source, "commit", "-qm", "Update source")

    def run_manager(self, action, *more):
        return command("python3", MANAGER, action, "--project", self.project,
                       "--source", self.source, *more)

    def bootstrap(self, skills="bmforge-http,bmforge-db-server"):
        result = self.run_manager("init", "--components", skills)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_creates_pinned_local_skills_and_no_application(self):
        result = self.bootstrap()
        self.assertIn("Installed 5 pinned", result.stdout)
        lock = json.loads((self.project / module.LOCK).read_text())
        self.assertEqual(set(lock["skills"]), {"bmforge-project", "bmforge-constants",
                                               "bmforge-localization", "bmforge-http", "bmforge-db-server"})
        self.assertEqual(len(lock["source_commit"]), 40)
        self.assertEqual(lock["skills"]["bmforge-http"]["source_commit"], lock["source_commit"])
        self.assertTrue((self.project / "AGENTS.md").is_file())
        self.assertTrue((self.project / ".agents/skills/bmforge-db-server/assets/DbMgr.py").is_file())
        self.assertTrue((self.project / ".agents/skills/bmforge-http/references/specification.md").is_file())
        self.assertFalse((self.project / ".agents/skills/bmforge-zmq").exists())
        self.assertFalse((self.project / "app").exists())
        self.assertIn("Do not apply", (self.project / "AGENTS.md").read_text())

    def test_empty_component_selection_installs_architecture_only(self):
        self.bootstrap("")
        lock = json.loads((self.project / module.LOCK).read_text())
        self.assertEqual(set(lock["skills"]), set(module.BASE_SKILLS))

    def test_read_only_check_is_idempotent(self):
        self.bootstrap()
        paths = [self.project / module.LOCK,
                 self.project / module.MANAGER,
                 self.project / ".agents/skills/bmforge-http/SKILL.md"]
        before = [(p.read_bytes(), p.stat().st_mtime_ns) for p in paths]
        check = self.run_manager("check")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn("All pinned BMForge skills are current", check.stdout)
        self.assertEqual(before, [(p.read_bytes(), p.stat().st_mtime_ns) for p in paths])

    def test_changed_upstream_is_reported_never_applied(self):
        self.bootstrap()
        local = self.project / ".agents/skills/bmforge-db-server/references/specification.md"
        first = local.read_bytes()
        (self.source / "pages/component-db-server.md").write_text('---\nspec_version: "0.2.0"\n---\nChanged!\n')
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-db-server: installed 0.1.0, available 0.2.0", result.stdout)
        self.assertIn("No updates were applied", result.stdout)
        self.assertEqual(local.read_bytes(), first)

    def test_changed_skill_without_spec_version_bump_is_reported(self):
        self.bootstrap()
        skill = self.source / "skills/bmforge-http/SKILL.md"
        skill.write_text(skill.read_text() + "\nNew instruction.\n")
        self.commit_source()
        output = self.run_manager("check")
        self.assertIn("UPDATE AVAILABLE bmforge-http", output.stdout)
        self.assertNotIn("UPDATE AVAILABLE bmforge-db-server", output.stdout)

    def test_unrelated_upstream_commit_does_not_issue_skill_update(self):
        self.bootstrap()
        (self.source / "UNRELATED.md").write_text("Changelog-only edit\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("UPDATE AVAILABLE", result.stdout)
        self.assertIn("All pinned BMForge skills are current", result.stdout)

    def test_bootstrap_manager_update_is_reported_not_applied(self):
        self.bootstrap()
        local = self.project / module.MANAGER
        old = local.read_bytes()
        upstream = self.source / "skills/bmforge-new-project/scripts/manage.py"
        upstream.write_bytes(old + b"\n# Nonfunctional update\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE manager", result.stdout)
        self.assertEqual(local.read_bytes(), old)

    def test_dirty_installed_copy_reports_and_refuses_implicit_replacement(self):
        self.bootstrap()
        skill = self.project / ".agents/skills/bmforge-http/SKILL.md"
        skill.write_text(skill.read_text() + "\nLocal edit\n")
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("LOCALLY MODIFIED bmforge-http", result.stdout)
        self.assertIn("Local edit", skill.read_text())

    def test_init_refuses_existing_agent_instructions_without_changes(self):
        (self.project / "AGENTS.md").write_text("User authored\n")
        result = self.run_manager("init", "--components", "bmforge-http")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Refusing to overwrite", result.stderr)
        self.assertEqual((self.project / "AGENTS.md").read_text(), "User authored\n")
        self.assertFalse((self.project / ".agents").exists())

    def test_add_selective_skill_does_not_replace_older_skill(self):
        self.bootstrap("bmforge-db-server")
        existing = self.project / ".agents/skills/bmforge-db-server/SKILL.md"
        content = existing.read_bytes()
        result = self.run_manager("add", "--components", "bmforge-zmq")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.project / ".agents/skills/bmforge-zmq/SKILL.md").is_file())
        self.assertEqual(existing.read_bytes(), content)
        lock = json.loads((self.project / module.LOCK).read_text())
        self.assertIn("bmforge-zmq", lock["skills"])
        self.assertEqual(len(lock["skills"]["bmforge-zmq"]["source_commit"]), 40)
        repeat = self.run_manager("add", "--components", "bmforge-zmq")
        self.assertEqual(repeat.returncode, 2)
        self.assertEqual(existing.read_bytes(), content)

    def test_invalid_component_and_missing_remote_fail_without_mutation(self):
        fail = self.run_manager("init", "--components", "bmforge-http,django")
        self.assertEqual(fail.returncode, 2)
        self.assertIn("Unknown component", fail.stderr)
        self.assertFalse((self.project / ".agents").exists())
        self.bootstrap()
        unavailable = command("python3", MANAGER, "check", "--project", self.project,
                              "--source", str(self.project.parent / "nonexistent"))
        self.assertEqual(unavailable.returncode, 2)
        self.assertIn("UPDATE CHECK UNAVAILABLE", unavailable.stderr)
        self.assertTrue((self.project / module.LOCK).is_file())

    def test_baseline_constants_and_localization_are_pinned(self):
        self.bootstrap("")
        root = self.project / ".agents/skills"
        self.assertTrue((root / "bmforge-constants/assets/DProject.py").is_file())
        self.assertTrue((root / "bmforge-localization/assets/Localizer.py").is_file())
        self.assertTrue((root / "bmforge-localization/assets/DText.py").is_file())
        self.assertTrue((root / "bmforge-localization/assets/en.json").is_file())
        self.assertEqual(self.run_manager("check").returncode, 0)

    def test_new_baseline_skill_changes_only_notify(self):
        self.bootstrap("")
        local = self.project / ".agents/skills/bmforge-localization/assets/en.json"
        frozen = local.read_bytes()
        source = self.source / module.EN_CATALOG
        source.write_text(source.read_text() + "New string")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-localization", result.stdout)
        self.assertNotIn("UPDATE AVAILABLE bmforge-constants", result.stdout)
        self.assertEqual(local.read_bytes(), frozen)

    def test_default_skills_are_not_selectable_twice(self):
        result = self.run_manager("init", "--components", "bmforge-localization")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unknown component", result.stderr)
        self.assertFalse((self.project / ".agents").exists())

    def test_full_catalog_installable(self):
        selection = ",".join(k for k in module.SKILLS if k not in module.BASE_SKILLS)
        self.bootstrap(selection)
        self.assertEqual(len(json.loads((self.project / module.LOCK).read_text())["skills"]), 8)
        self.assertEqual(self.run_manager("check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
