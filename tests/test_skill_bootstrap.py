"""Bootstrap tests use only local Git repositories, never remote GitHub or an app."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "skills/bmforge/scripts/manage.py"
SPEC = importlib.util.spec_from_file_location("bmforge_skill_manager", MANAGER)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def command(*args, cwd=None, env=None):
    return subprocess.run([str(value) for value in args], cwd=cwd, env=env,
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
        git(self.source, "init", "-q", "-b", "main")
        git(self.source, "config", "user.name", "BMForge Test")
        git(self.source, "config", "user.email", "test@example.invalid")
        git(self.project, "init", "-q")
        for name in module.SKILLS:
            folder = self.source / "skills" / name
            folder.mkdir(parents=True)
            original = ROOT / "skills" / name / "SKILL.md"
            (folder / "SKILL.md").write_bytes(original.read_bytes())
        manager = self.source / "skills/bmforge/scripts/manage.py"
        manager.parent.mkdir(parents=True)
        manager.write_bytes(MANAGER.read_bytes())
        for common in (*module.COMMON, module.HEALTH, *module.RELEASE_GUIDES,
                       *module.INSTALLATION_GUIDES):
            path = self.source / common
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {path.name}\n")
        for original in module.RELEASE_TEMPLATES.values():
            path = self.source / original
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / original).read_bytes())
        for name, (spec, references) in module.SKILLS.items():
            if spec:
                path = self.source / spec
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f'---\nspec_version: "0.1.0"\n---\n# {name}\n')
            for original in references:
                path = self.source / original
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# Frozen reference: {original}\n")
        for original in (module.DB_TEMPLATE, module.GIT_TEMPLATE, module.GIF_TEMPLATE, module.CONSTANTS_TEMPLATE,
                         module.LOCALIZER_TEMPLATE, module.TEXT_TEMPLATE, module.EN_CATALOG):
            path = self.source / original
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# Canonical template {original}\n")
        self.commit_source()

    def commit_source(self):
        git(self.source, "add", ".")
        git(self.source, "commit", "-qm", "Update source")

    def run_manager(self, action, *more):
        identity = ("--name", "AcmeApp", "--subtype", "Inventory") if action == "init" else ()
        source = ("--source", self.source) if action != "setup-branches" else ()
        return command("python3", MANAGER, action, "--project", self.project,
                       *source, *identity, *more)

    def initial_commit(self):
        git(self.project, "add", ".")
        git(self.project, "-c", "user.name=BMForge Test",
            "-c", "user.email=test@example.invalid", "commit", "-qm", "Initial scaffold")
        git(self.project, "branch", "-M", "main")

    def bootstrap(self, skills="bmforge-http,bmforge-db-server"):
        result = self.run_manager("init", "--components", skills)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_single_user_entry_point_is_bmforge(self):
        skill = (ROOT / "skills/bmforge/SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: bmforge\n"))
        self.assertIn("bmforge-http", skill)
        self.assertIn("bmforge-rca", skill)
        self.assertFalse((ROOT / "skills/bmforge-new-project").exists())
        self.assertIn("tree/main/skills/bmforge", (ROOT / "pages/codex-skills.md").read_text())

    def test_implementation_gate_is_in_entry_point_and_bootstrapped_guidance(self):
        self.bootstrap("")
        entry_point = (ROOT / "skills/bmforge/SKILL.md").read_text()
        project_skill = (self.project / ".agents/skills/bmforge-project/SKILL.md").read_text()
        agents = (self.project / "AGENTS.md").read_text()
        contract = (ROOT / "pages/engineering-contract.md").read_text()
        self.assertIn("## Implementation authorization gate", entry_point)
        self.assertIn("explicit go-ahead", entry_point)
        self.assertIn("**Implementation authorization gate:**", project_skill)
        self.assertIn("Implementation authorization gate:", agents)
        self.assertIn("A direct request to implement or fix counts", agents)
        self.assertIn("Permission to implement does not authorize", agents)
        self.assertIn("## Implementation authorization gate", contract)
        self.assertIn("Discussion is not authorization to implement.", contract)

    def test_creates_pinned_local_skills_and_no_application(self):
        result = self.bootstrap()
        self.assertIn("Installed 6 pinned", result.stdout)
        lock = json.loads((self.project / module.LOCK).read_text())
        self.assertEqual(set(lock["skills"]), {"bmforge-project", "bmforge-constants",
                                               "bmforge-localization", "bmforge-installation",
                                               "bmforge-http", "bmforge-db-server"})
        self.assertEqual(len(lock["source_commit"]), 40)
        self.assertEqual(lock["skills"]["bmforge-http"]["source_commit"], lock["source_commit"])
        self.assertTrue((self.project / "AGENTS.md").is_file())
        self.assertTrue((self.project / ".agents/skills/bmforge-db-server/assets/DbMgr.py").is_file())
        self.assertTrue((self.project / ".agents/skills/bmforge-http/references/specification.md").is_file())
        self.assertFalse((self.project / ".agents/skills/bmforge-zmq").exists())
        self.assertFalse((self.project / "app").exists())
        self.assertIn("Do not apply", (self.project / "AGENTS.md").read_text())

    def test_changelog_policy_is_in_generated_guidance_and_pinned_reference(self):
        self.bootstrap("")
        agents = (self.project / "AGENTS.md").read_text()
        self.assertIn("For EVERY completed logical change", agents)
        self.assertIn("CHANGELOG.md", agents)
        self.assertIn("### Summary", agents)
        skill = (self.project / ".agents/skills/bmforge-project/SKILL.md").read_text()
        self.assertIn("references/changelog-maintenance.md", skill)
        reference = self.project / ".agents/skills/bmforge-project/references/changelog-maintenance.md"
        self.assertTrue(reference.is_file())
        self.assertEqual(reference.read_text(),
                         (self.source / "pages/changelog-maintenance.md").read_text())

    def test_changelog_guidance_update_is_reported_without_overwriting_pin(self):
        self.bootstrap("")
        reference = self.project / ".agents/skills/bmforge-project/references/changelog-maintenance.md"
        old_content = reference.read_bytes()
        upstream = self.source / "pages/changelog-maintenance.md"
        upstream.write_text(upstream.read_text() + "\nNew changelog guidance.\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-project", result.stdout)
        self.assertIn("No updates were applied", result.stdout)
        self.assertEqual(reference.read_bytes(), old_content)

    def test_implementation_gate_contract_updates_only_notify(self):
        self.bootstrap("")
        installed = (self.project / ".agents/skills/bmforge-project/"
                     "references/engineering-contract.md")
        previous = installed.read_bytes()
        contract = self.source / "pages/engineering-contract.md"
        contract.write_text(contract.read_text() + "\nRevised authorization guidance.\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-project", result.stdout)
        self.assertIn("No updates were applied", result.stdout)
        self.assertEqual(installed.read_bytes(), previous)

    def test_http_design_references_are_pinned_with_selected_skill(self):
        self.bootstrap("bmforge-http")
        base = "bmdynip/bmdynip/server/static"
        installed_root = self.project / ".agents/skills/bmforge-http"
        for filename in ("index.html", "style.css"):
            installed = installed_root / "references/source" / base / filename
            upstream = self.source / "components/reference" / base / filename
            self.assertTrue(installed.is_file())
            self.assertEqual(installed.read_bytes(), upstream.read_bytes())
        self.assertFalse((self.project / ".agents/skills/bmforge-visualization").exists())
        self.assertIn("no pastels", (installed_root / "SKILL.md").read_text())

    def test_http_design_reference_updates_only_notify(self):
        self.bootstrap("bmforge-http")
        name = "bmdynip/bmdynip/server/static/style.css"
        installed = self.project / ".agents/skills/bmforge-http/references/source" / name
        old = installed.read_bytes()
        source = self.source / "components/reference" / name
        source.write_text(source.read_text() + "\nNew design snapshot.\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-http", result.stdout)
        self.assertEqual(installed.read_bytes(), old)

    def test_empty_component_selection_installs_all_baseline_skills(self):
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

    def test_check_uses_shared_cache_without_remote_access(self):
        self.bootstrap("")
        lock_file = self.project / module.LOCK
        lock = json.loads(lock_file.read_text())
        lock["repository"] = module.SOURCE_URL
        lock_file.write_text(json.dumps(lock))
        cache_home = self.project.parent / "cache-home"
        cache = cache_home / ".cache/bmforge-upstream"
        cache.parent.mkdir(parents=True)
        shutil.copytree(self.source, cache)
        env = os.environ.copy()
        env["HOME"] = str(cache_home)
        env.pop("BMFORGE_SOURCE", None)
        result = command("python3", MANAGER, "check", "--project", self.project,
                         env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("LOCAL SOURCE", result.stdout)
        self.assertIn("against the local source snapshot", result.stdout)

    def test_check_with_remote_lock_and_no_cache_is_unavailable_offline(self):
        self.bootstrap("")
        lock_file = self.project / module.LOCK
        lock = json.loads(lock_file.read_text())
        lock["repository"] = module.SOURCE_URL
        lock_file.write_text(json.dumps(lock))
        env = os.environ.copy()
        env["HOME"] = str(self.project.parent / "missing-home")
        env.pop("BMFORGE_SOURCE", None)
        result = command("python3", MANAGER, "check", "--project", self.project,
                         env=env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Local BMForge source unavailable", result.stderr)
        self.assertNotIn("Git clone", result.stderr)

    def test_check_can_use_explicit_local_source_environment(self):
        self.bootstrap("")
        lock_file = self.project / module.LOCK
        lock = json.loads(lock_file.read_text())
        lock["repository"] = module.SOURCE_URL
        lock_file.write_text(json.dumps(lock))
        env = os.environ.copy()
        env["HOME"] = str(self.project.parent / "missing-home")
        env["BMFORGE_SOURCE"] = str(self.source)
        result = command("python3", MANAGER, "check", "--project", self.project,
                         env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("LOCAL SOURCE", result.stdout)

    def test_unavailable_upstream_does_not_hide_local_modifications(self):
        self.bootstrap("")
        architecture = self.project / ".agents/skills/bmforge-project/SKILL.md"
        architecture.write_text(architecture.read_text() + "\nLocally edited architecture\n")
        lock_file = self.project / module.LOCK
        lock = json.loads(lock_file.read_text())
        lock["repository"] = module.SOURCE_URL
        lock_file.write_text(json.dumps(lock))
        env = os.environ.copy()
        env["HOME"] = str(self.project.parent / "missing-home")
        env.pop("BMFORGE_SOURCE", None)
        result = command("python3", MANAGER, "check", "--project", self.project,
                         env=env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("LOCALLY MODIFIED bmforge-project", result.stdout)
        self.assertIn("UPDATE CHECK UNAVAILABLE", result.stderr)
        self.assertIn("Locally edited architecture", architecture.read_text())

    def test_check_rejects_dirty_or_non_main_source(self):
        self.bootstrap("")
        skill = self.source / "skills/bmforge-http/SKILL.md"
        skill.write_text(skill.read_text() + "\nUncommitted source edit\n")
        dirty = self.run_manager("check")
        self.assertEqual(dirty.returncode, 2)
        self.assertIn("source has local changes", dirty.stderr)
        self.assertNotIn("UPDATE AVAILABLE", dirty.stdout)
        git(self.source, "restore", "skills/bmforge-http/SKILL.md")
        git(self.source, "switch", "-q", "-c", "feature")
        branch = self.run_manager("check")
        self.assertEqual(branch.returncode, 2)
        self.assertIn("source must be on main", branch.stderr)

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
        upstream = self.source / "skills/bmforge/scripts/manage.py"
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

    def test_attach_preserves_established_project_and_supports_add_check(self):
        (self.project / "AGENTS.md").write_text("R3el's own coding guidance\n")
        (self.project / "CHANGELOG.md").write_text("Established application history\n")
        (self.project / "scripts").mkdir()
        (self.project / "scripts/release.sh").write_text("original release\n")
        other_skill = self.project / ".agents/skills/other-agent"
        other_skill.mkdir(parents=True)
        (other_skill / "SKILL.md").write_text("Third-party skill\n")
        git(self.project, "add", ".")
        git(self.project, "-c", "user.name=BMForge Test", "-c", "user.email=test@example.invalid",
            "commit", "-qm", "Existing project")
        old_head = git(self.project, "rev-parse", "HEAD")

        result = self.run_manager("attach", "--components", "bmforge-rca")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Attached 1 pinned", result.stdout)
        lock = json.loads((self.project / module.LOCK).read_text())
        self.assertEqual(lock["mode"], "attached")
        self.assertEqual(set(lock["skills"]), {"bmforge-rca"})
        self.assertEqual(len(lock["source_commit"]), 40)
        self.assertTrue((self.project / module.MANAGER).is_file())
        self.assertTrue((self.project / ".agents/skills/bmforge-rca/SKILL.md").is_file())
        self.assertEqual((self.project / "AGENTS.md").read_text(), "R3el's own coding guidance\n")
        self.assertEqual((self.project / "CHANGELOG.md").read_text(), "Established application history\n")
        self.assertEqual((self.project / "scripts/release.sh").read_text(), "original release\n")
        self.assertEqual((other_skill / "SKILL.md").read_text(), "Third-party skill\n")
        self.assertFalse((self.project / "scripts/new-release.sh").exists())
        self.assertFalse((self.project / ".agents/skills/bmforge-project").exists())
        self.assertEqual(git(self.project, "rev-parse", "HEAD"), old_head)
        self.assertEqual(self.run_manager("check").returncode, 0)

        added = self.run_manager("add", "--components", "bmforge-zmq")
        self.assertEqual(added.returncode, 0, added.stderr)
        self.assertEqual(set(json.loads((self.project / module.LOCK).read_text())["skills"]),
                         {"bmforge-rca", "bmforge-zmq"})
        self.assertEqual(self.run_manager("check").returncode, 0)
        branches = self.run_manager("setup-branches", "--dry-run")
        self.assertEqual(branches.returncode, 2)
        self.assertIn("not attached repositories", branches.stderr)
        self.assertEqual(git(self.project, "branch", "--list", "dev"), "")

    def test_attach_requires_explicit_optional_skills(self):
        (self.project / "AGENTS.md").write_text("Leave this intact\n")
        for selection in ("", "bmforge-project", "bmforge-rca,bmforge-rca", "django"):
            result = self.run_manager("attach", "--components", selection)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((self.project / ".agents").exists())
        self.assertEqual((self.project / "AGENTS.md").read_text(), "Leave this intact\n")

    def test_attach_refuses_existing_managed_or_colliding_paths(self):
        other_skill = self.project / ".agents/skills/bmforge-rca"
        other_skill.mkdir(parents=True)
        (other_skill / "SKILL.md").write_text("User-owned RCA\n")
        conflict = self.run_manager("attach", "--components", "bmforge-rca")
        self.assertEqual(conflict.returncode, 2)
        self.assertIn("refusing overwrite", conflict.stderr)
        self.assertEqual((other_skill / "SKILL.md").read_text(), "User-owned RCA\n")
        self.assertFalse((self.project / module.LOCK).exists())
        self.assertFalse((self.project / module.MANAGER).exists())

        other_skill.rename(self.project / ".agents/skills/renamed-skill")
        (self.project / ".agents/bmforge").mkdir()
        managed = self.run_manager("attach", "--components", "bmforge-rca")
        self.assertEqual(managed.returncode, 2)
        self.assertIn("management directory already exists", managed.stderr)
        self.assertFalse((self.project / module.LOCK).exists())

    def test_attach_refuses_symlinked_skill_directory(self):
        destination = self.project.parent / "outside-skills"
        destination.mkdir()
        (self.project / ".agents").mkdir()
        (self.project / ".agents/skills").symlink_to(destination, target_is_directory=True)
        result = self.run_manager("attach", "--components", "bmforge-rca")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unsafe existing agent directory", result.stderr)
        self.assertEqual(list(destination.iterdir()), [])
        self.assertFalse((self.project / module.LOCK).exists())

    def test_attach_rolls_back_partial_copy_without_touching_existing_files(self):
        agents = self.project / ".agents"
        agents.mkdir()
        (agents / "other-file.txt").write_text("owned by project\n")
        def interrupted_copy(path, files):
            path.mkdir()
            (path / "partial.txt").write_text("incomplete")
            raise OSError("simulated copy failure")
        args = SimpleNamespace(project=self.project, source=self.source, components="bmforge-rca")
        with mock.patch.object(module, "copy_bundle", side_effect=interrupted_copy):
            with self.assertRaisesRegex(OSError, "simulated copy failure"):
                module.start_attach(args)
        self.assertEqual((agents / "other-file.txt").read_text(), "owned by project\n")
        self.assertFalse((agents / "skills").exists())
        self.assertFalse((agents / "bmforge").exists())


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
        self.assertTrue((root / "bmforge-installation/SKILL.md").is_file())
        self.assertTrue((root / "bmforge-installation/references/specification.md").is_file())
        self.assertTrue((root / "bmforge-installation/references/installation-scripts.md").is_file())
        self.assertTrue((root / "bmforge-installation/references/source/devlog/scripts/install-server.sh").is_file())
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
        for name in ("bmforge-localization", "bmforge-installation"):
            result = self.run_manager("init", "--components", name)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Unknown component", result.stderr)
            self.assertFalse((self.project / ".agents").exists())

    def test_bootstrap_installs_configured_release_tooling(self):
        result = self.bootstrap("")
        self.assertIn("scripts/new-release.sh", result.stdout)
        release = self.project / "scripts/new-release.sh"
        script = release.read_text()
        self.assertTrue(release.stat().st_mode & 0o111)
        self.assertIn('readonly project_name="AcmeApp"', script)
        self.assertIn('readonly version_file="acmeapp/constants/DAcmeApp.py"', script)
        self.assertNotIn("__PROJECT_", script)
        for name in ("install.sh", "upgrade.sh", "uninstall.sh"):
            file = self.project / "scripts" / name
            self.assertTrue(file.stat().st_mode & 0o111, name)
            self.assertEqual(command("bash", "-n", file).returncode, 0, name)
        for name in ("install.py", "check-cmdb.py"):
            self.assertTrue((self.project / "scripts" / name).is_file())
        changelog = self.project / "CHANGELOG.md"
        self.assertEqual(changelog.read_text(), (ROOT / "templates/project/CHANGELOG.md").read_text())
        constants = self.project / "acmeapp/constants/DAcmeApp.py"
        self.assertTrue(constants.is_file())
        self.assertIn("class DAcmeApp:", constants.read_text())
        self.assertIn('CMDB_SUBTYPE: Final[str] = "Inventory"', constants.read_text())
        self.assertNotIn("__PROJECT_", constants.read_text())
        self.assertEqual(command("bash", "-n", release).returncode, 0)
        help_result = command("bash", release, "--help")
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("Likely next version: 0.0.1", help_result.stdout)
        validate = command("python3", "-B", self.project / "scripts/check-cmdb.py",
                           "--name", "AcmeApp", "acmeapp/constants/DAcmeApp.py",
                           cwd=self.project)
        self.assertEqual(validate.returncode, 0, validate.stderr)
        self.assertTrue(git(self.project, "status", "--porcelain").startswith("??"))

    def test_release_scripts_preserve_upstream_logic(self):
        self.bootstrap("")
        expected = (ROOT / "templates/project/scripts/new-release.sh").read_text()
        actual = (self.project / "scripts/new-release.sh").read_text()
        self.assertEqual(actual, expected.replace("__PROJECT_NAME__", "AcmeApp")
                         .replace("__PROJECT_SLUG__", "acmeapp"))
        self.assertIn("git push --atomic", actual)
        self.assertIn("Create annotated tag", actual)

    def test_refuses_existing_release_file_without_writing_skills(self):
        (self.project / "CHANGELOG.md").write_text("Owner's changelog\n")
        result = self.run_manager("init")
        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing overwrite: CHANGELOG.md", result.stderr)
        self.assertEqual((self.project / "CHANGELOG.md").read_text(), "Owner's changelog\n")
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / "scripts").exists())

    def test_refuses_symlinked_release_script_parent(self):
        sibling = self.project.parent / "foreign-scripts"
        sibling.mkdir()
        (self.project / "scripts").symlink_to(sibling, target_is_directory=True)
        result = self.run_manager("init")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unsafe existing parent", result.stderr)
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(list(sibling.iterdir()), [])

    def test_invalid_project_name_and_placeholder_subtype(self):
        for options, message in (
            (("--name", "Bad-Name"), "canonical Python class name"),
            (("--subtype", "__PROJECT_SUBTYPE__"), "--subtype"),
        ):
            result = self.run_manager("init", *options)
            self.assertEqual(result.returncode, 2)
            self.assertIn(message, result.stderr)
            self.assertFalse((self.project / ".agents").exists())

    def test_new_release_template_update_is_notice_only(self):
        self.bootstrap("")
        release = self.project / "scripts/new-release.sh"
        before = release.read_bytes()
        new = self.source / "templates/project/scripts/new-release.sh"
        new.write_bytes(new.read_bytes() + b"\n# Updated upstream release template\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-project", result.stdout)
        self.assertIn("No updates were applied", result.stdout)
        self.assertEqual(before, release.read_bytes())

    def test_installation_policy_updates_are_notice_only(self):
        self.bootstrap("")
        spec = self.project / ".agents/skills/bmforge-installation/references/specification.md"
        original = spec.read_bytes()
        change = self.source / "pages/component-installation.md"
        change.write_text(change.read_text() + "\nNew version of installation guidance\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-installation", result.stdout)
        self.assertIn("No updates were applied", result.stdout)
        self.assertEqual(spec.read_bytes(), original)

    def test_branch_setup_requires_a_committed_scaffold(self):
        self.bootstrap("")
        result = self.run_manager("setup-branches")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Commit the bootstrap scaffold", result.stderr)
        self.assertEqual(git(self.project, "branch", "--list", "dev"), "")

    def test_branch_setup_dry_run_and_creation_do_not_commit_or_push(self):
        self.bootstrap("")
        self.initial_commit()
        initial_sha = git(self.project, "rev-parse", "main")
        check = self.run_manager("setup-branches", "--dry-run")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn("READY to create local dev", check.stdout)
        self.assertEqual(git(self.project, "branch", "--list", "dev"), "")
        result = self.run_manager("setup-branches")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No commit, remote branch, tag or push", result.stdout)
        self.assertEqual(git(self.project, "rev-parse", "main"), initial_sha)
        self.assertEqual(git(self.project, "rev-parse", "dev"), initial_sha)
        self.assertEqual(git(self.project, "rev-parse", "feat/maint-0.1.0"), initial_sha)
        self.assertEqual(git(self.project, "branch", "--show-current"), "feat/maint-0.1.0")
        self.assertEqual(git(self.project, "status", "--porcelain"), "")
        self.assertEqual(git(self.project, "remote"), "")

    def test_branch_setup_refuses_dirty_tree_and_existing_branches(self):
        self.bootstrap("")
        self.initial_commit()
        (self.project / "pending.txt").write_text("unfinished")
        dirty = self.run_manager("setup-branches")
        self.assertEqual(dirty.returncode, 2)
        self.assertIn("Commit or stash", dirty.stderr)
        self.assertEqual(git(self.project, "branch", "--list", "dev"), "")
        (self.project / "pending.txt").unlink()
        git(self.project, "branch", "dev", "main")
        existing = self.run_manager("setup-branches")
        self.assertEqual(existing.returncode, 2)
        self.assertIn("already exists", existing.stderr)
        self.assertEqual(git(self.project, "branch", "--show-current"), "main")

    def test_branch_setup_refuses_existing_remote_refs_and_wrong_branch(self):
        self.bootstrap("")
        self.initial_commit()
        git(self.project, "update-ref", "refs/remotes/origin/dev", "HEAD")
        remote = self.run_manager("setup-branches")
        self.assertEqual(remote.returncode, 2)
        self.assertIn("origin/dev already exists", remote.stderr)
        git(self.project, "update-ref", "-d", "refs/remotes/origin/dev")
        git(self.project, "switch", "-c", "other")
        wrong = self.run_manager("setup-branches")
        self.assertEqual(wrong.returncode, 2)
        self.assertIn("Switch to local main", wrong.stderr)

    def test_branch_setup_validates_feature_name_before_creating_refs(self):
        self.bootstrap("")
        self.initial_commit()
        for name in ("dev", "topic", "feat/../bad", "feat/invalid..name"):
            result = self.run_manager("setup-branches", "--feature", name)
            self.assertEqual(result.returncode, 2)
        self.assertEqual(git(self.project, "branch", "--list", "dev"), "")
        self.assertEqual(git(self.project, "branch", "--show-current"), "main")

    def test_optional_gif_skill_is_pinned_and_template_updates_only_notify(self):
        self.bootstrap("bmforge-gif-animation")
        skill = self.project / ".agents/skills/bmforge-gif-animation"
        self.assertTrue((skill / "references/specification.md").is_file())
        self.assertTrue((skill / "assets/GIFAnimation.py").is_file())
        self.assertTrue((skill / "references/source/snake-web-code/snakewebcode/activity/SimulationAnimation.py").is_file())
        self.assertEqual(self.run_manager("check").returncode, 0)
        original = (skill / "assets/GIFAnimation.py").read_bytes()
        path = self.source / module.GIF_TEMPLATE
        path.write_text(path.read_text() + "\nUpdated GIF template.\n")
        self.commit_source()
        check = self.run_manager("check")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-gif-animation", check.stdout)
        self.assertEqual((skill / "assets/GIFAnimation.py").read_bytes(), original)


    def test_optional_rca_skill_is_pinned_and_update_is_notification_only(self):
        self.bootstrap("bmforge-rca")
        directory = self.project / ".agents/skills/bmforge-rca"
        skill = directory / "SKILL.md"
        original = skill.read_bytes()
        self.assertIn(b"Never modify a remote host", original)
        self.assertFalse((directory / "references/specification.md").exists())
        self.assertEqual(self.run_manager("check").returncode, 0)
        upstream = self.source / "skills/bmforge-rca/SKILL.md"
        upstream.write_text(upstream.read_text() + "\nUpdated RCA guidance.\n")
        self.commit_source()
        result = self.run_manager("check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UPDATE AVAILABLE bmforge-rca", result.stdout)
        self.assertEqual(skill.read_bytes(), original)

    def test_full_catalog_installable(self):
        selection = ",".join(k for k in module.SKILLS if k not in module.BASE_SKILLS)
        self.bootstrap(selection)
        self.assertEqual(len(json.loads((self.project / module.LOCK).read_text())["skills"]), 11)
        self.assertEqual(self.run_manager("check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
