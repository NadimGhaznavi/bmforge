"""Verify the installation component contract and frozen DevLog role references."""

import ast
from hashlib import sha1
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "pages/component-installation.md"
INSTALL = ROOT / "templates/project/scripts/install.py"
REF = ROOT / "components/reference/devlog"
ORIGINALS = {
    "scripts/deploy.py": "b471bc86f596c8c34b67e7b44da0f0ab0c9908dd",
    "scripts/install.sh": "3170a935f65a9a749d7f420934de453e83c1ba72",
    "scripts/install-server.sh": "ea0bfcd0d602995937f83545a0f61383e7faa221",
    "scripts/upgrade.sh": "003be8a1eb522c8b32a7b2f9f2752316d96c8e64",
    "tests/test_deployment.py": "f6a366b6f090af8fc0b5aea68d856d8da56a63ac",
    "docs/architecture.md": "c1b16241dcb06300e3a33c18b3facb64a63e2270",
}


def blob_hash(contents: bytes) -> str:
    return sha1(b"blob " + str(len(contents)).encode() + b"\0" + contents).hexdigest()


class InstallationContractTests(unittest.TestCase):
    def test_installation_is_baseline_and_component_is_versioned(self):
        spec = SPEC.read_text()
        self.assertIn('component_id: "bmforge.installation"', spec)
        self.assertIn('spec_version: "0.1.2"', spec)
        self.assertIn("## Approved implementation technology", spec)
        self.assertIn("install-server.sh", spec)
        self.assertIn(".deployment-version", spec)
        self.assertIn(".installation-manifest.json", spec)
        self.assertIn("/opt/prod/", spec)
        self.assertIn("uninstall.sh", spec)
        self.assertIn("library", spec)
        self.assertIn("not contain", spec.lower())
        self.assertIn('DEPLOYMENT_READY = False', spec)
        self.assertIn("pages/component-installation.md", (ROOT / "index.md").read_text())
        agent = (ROOT / "AGENTS.md").read_text()
        self.assertIn("pages/component-installation.md", agent)

    def test_canonical_install_helper_keeps_approved_imports_and_marker(self):
        program = INSTALL.read_text()
        tree = ast.parse(program)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.add(node.module)
        self.assertEqual(imported,
                         {"argparse", "importlib.util", "json", "os", "pathlib",
                          "shutil", "subprocess", "tempfile"})
        self.assertIn(
            'BMFORGE_COMPONENT = {"id": "bmforge.installation", "spec_version": "0.1.2"}',
            program)
        self.assertIn("DEPLOYMENT_READY = False", program)
        self.assertIn('VERSION_MARKER = ".deployment-version"', program)
        self.assertIn('MANIFEST = ".installation-manifest.json"', program)

    def test_devlog_examples_are_frozen_unchanged(self):
        for relative, expected in ORIGINALS.items():
            path = REF / relative
            self.assertTrue(path.is_file(), relative)
            self.assertEqual(blob_hash(path.read_bytes()), expected, relative)
        deploy = (REF / "scripts/deploy.py").read_text()
        self.assertIn('actions.add_parser("install-server"', deploy)
        self.assertIn('actions.add_parser("upgrade"', deploy)
        self.assertIn('installation.json', deploy)
        self.assertIn('"role": role', deploy)
        self.assertIn('BASE / "releases"', deploy)
        self.assertIn('"systemctl"', deploy)
        self.assertIn("tests/test_deployment.py", SPEC.read_text())
        # DevLog at this pinned revision does not implement uninstall.
        self.assertFalse((REF / "scripts/uninstall.sh").exists())

    def test_role_specific_command_preflight_is_required(self):
        contract = SPEC.read_text()
        self.assertIn("Operation-specific dependency preflight", contract)
        self.assertIn("same prerequisite checks", contract)
        self.assertIn("mariadb", contract)
        skill = (ROOT / "skills/bmforge-installation/SKILL.md").read_text()
        self.assertIn("role-and-operation-specific", skill)
        self.assertIn("--check", skill)

    def test_baseline_skill_bundles_spec_and_reference(self):
        manager = (ROOT / "skills/bmforge-new-project/scripts/manage.py").read_text()
        self.assertIn('"bmforge-installation": ("pages/component-installation.md"', manager)
        self.assertIn('BASE_SKILLS = ("bmforge-project", "bmforge-constants", '
                      '"bmforge-localization", "bmforge-installation")', manager)
        self.assertIn("INSTALLATION_GUIDES", manager)
        self.assertIn("def start_check(args):", manager)
        self.assertNotIn("def start_upgrade(", manager)
        skill = (ROOT / "skills/bmforge-installation/SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\nname: bmforge-installation\ndescription:"))
        self.assertIn("references/specification.md", skill)
        self.assertIn("uninstall", skill)
        self.assertIn(".deployment-version", skill)


if __name__ == "__main__":
    unittest.main()
