"""Check the contract, navigation and local component reference inventory."""
from pathlib import Path
import ast
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = {
    "http": "bmforge.http-server",
    "zmq": "bmforge.zmq-server",
    "db-server": "bmforge.db-server",
}


class ComponentBlueprintTests(unittest.TestCase):
    def test_specs_have_unique_versioned_identities(self):
        home = (ROOT / "index.md").read_text()
        guide = (ROOT / "pages/component-blueprints.md").read_text()
        for name, component_id in COMPONENTS.items():
            path = ROOT / f"pages/component-{name}.md"
            self.assertTrue(path.is_file(), path)
            body = path.read_text()
            self.assertIn(f"pages/component-{name}.md", home)
            self.assertIn(f"pages/component-{name}.md", guide)
            self.assertIn(f'component_id: "{component_id}"', body)
            self.assertRegex(body, r'(?m)^spec_version: "\d+\.\d+\.\d+"$')
            self.assertRegex(body, r'(?m)^spec_status: "(draft|published)"$')
            self.assertIn("## Acceptance checks", body)
            self.assertIn("components/reference/bmgeoip/", body)
            self.assertIn('spec_version: "0.3.0"', body)
            self.assertIn("pages/health-checks.md", body)

    def test_approved_module_inventory_is_explicit(self):
        expected = {
            "http": ("argparse", "http.server", "ipaddress", "json", "logging",
                     "pathlib", "signal", "urllib.parse", "jinja2"),
            "zmq": ("collections.abc", "dataclasses", "json", "threading",
                    "typing", "zmq"),
            "db-server": ("contextlib", "pathlib", "pymysql", "pymysql.cursors"),
        }
        for name, approved in expected.items():
            body = (ROOT / f"pages/component-{name}.md").read_text()
            section = body.split("## Approved runtime modules\n", 1)[1].split("\n## ", 1)[0]
            listed = re.findall(r"(?m)^\| (?:Python stdlib|Third-party|Third-party submodule) \| `([^`]+)` \|", section)
            self.assertEqual(listed, list(approved), name)
            self.assertIn("must pause and ask the user", section, name)
            self.assertIn("Application business logic", section, name)
            self.assertIn("## Reference snapshot", body)

    def test_homepage_jekyll_links_resolve_locally(self):
        home = (ROOT / "index.md").read_text()
        for path in re.findall(r"{%\s*link\s+([^\s%]+)\s*%}", home):
            self.assertTrue((ROOT / path).is_file(), f"broken Jekyll link: {path}")

    def test_contract_docs_and_agent_instructions_exist(self):
        home = (ROOT / "index.md").read_text()
        agent = (ROOT / "AGENTS.md").read_text()
        for path in ("pages/engineering-contract.md",
                     "pages/specification-lifecycle.md"):
            self.assertTrue((ROOT / path).is_file())
            self.assertIn(path, home)
            self.assertIn(path, agent)
        self.assertTrue((ROOT / "DECISIONS.md").is_file())
        self.assertIn("Never add BMForge", agent)
        self.assertIn("public APIs", agent)
        self.assertIn("fail visibly", agent)

    def test_health_contract_is_app_mediated(self):
        health = (ROOT / "pages/health-checks.md").read_text()
        self.assertIn("GET `/health`", health)
        self.assertIn("HTTP 200", health)
        self.assertIn("HTTP 503", health)
        self.assertIn("does **not** connect directly to MariaDB", health)
        self.assertIn("pages/health-checks.md", (ROOT / "index.md").read_text())
        for filename in ("component-http.md", "component-zmq.md", "component-db-server.md"):
            self.assertIn("health", (ROOT / "pages" / filename).read_text().lower())

    def test_git_template_has_only_approved_imports(self):
        template = (ROOT / "components/templates/git/Git.py").read_text()
        syntax = ast.parse(template)
        modules = set()
        for node in ast.walk(syntax):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.add(node.module)
        expected = {"contextlib", "fcntl", "os", "pathlib", "subprocess", "tempfile"}
        self.assertEqual(modules, expected)
        contract = (ROOT / "pages/component-git.md").read_text()
        for module in expected:
            self.assertIn(f"| `{module}` |", contract)
        self.assertIn('BMFORGE_COMPONENT = {"id": "bmforge.git", "spec_version": "0.1.0"}', template)

    def test_reference_snapshots_are_local(self):
        base = ROOT / "components/reference/bmgeoip/bmgeoip"
        paths = ("server/BMGeoIPServer.py", "server/BMGeoIPHandler.py",
                 "server/LookupHandler.py", "zmq/ZMQServer.py",
                 "zmq/ZMQMsg.py", "interface/DbMgr.py",
                 "interface/DatabaseEnvironment.py", "interface/GeoIpDb.py",
                 "constants/DZMQ.py", "constants/DGeoIp.py")
        for path in paths:
            self.assertTrue((base / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
