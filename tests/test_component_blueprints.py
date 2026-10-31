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
VERSIONS = {"http": "0.5.0", "zmq": "0.4.0", "db-server": "0.5.0"}


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
            self.assertIn(f'spec_version: "{VERSIONS[name]}"', body)
            self.assertIn("pages/health-checks.md", body)

    def test_approved_module_inventory_is_explicit(self):
        expected = {
            "http": ("argparse", "datetime", "http.server", "ipaddress", "json", "logging",
                     "pathlib", "signal", "urllib.parse", "zoneinfo", "jinja2"),
            "zmq": ("collections.abc", "dataclasses", "json", "threading",
                    "typing", "zmq"),
            "db-server": ("contextlib", "pymysql", "pymysql.cursors"),
        }
        for name, approved in expected.items():
            body = (ROOT / f"pages/component-{name}.md").read_text()
            section = body.split("## Approved runtime modules\n", 1)[1].split("\n## ", 1)[0]
            listed = re.findall(r"(?m)^\| (?:Python stdlib|Third-party|Third-party submodule) \| `([^`]+)` \|", section)
            self.assertEqual(listed, list(approved), name)
            self.assertIn("must pause and ask the user", section, name)
            self.assertIn("Application business logic", section, name)
            self.assertIn("## Reference snapshot", body)

    def test_http_gui_dark_style_contract_and_bmdynip_references(self):
        spec = (ROOT / "pages/component-http.md").read_text()
        skill = (ROOT / "skills/bmforge-http/SKILL.md").read_text()
        self.assertIn("## GUI design contract (human-facing HTML only)", spec)
        for word in ("dark", "saturated", "pastels", "4.5:1", "3:1",
                     "keyboard focus", "mobile", "API-only", "BMDynIP"):
            self.assertIn(word, spec)
        self.assertIn("spec version `0.5.0`", skill)
        self.assertIn("no pastels", skill)
        source = ROOT / "components/reference/bmdynip/bmdynip/server/static"
        css, html = source / "style.css", source / "index.html"
        self.assertTrue(css.is_file())
        self.assertTrue(html.is_file())
        self.assertIn("color-scheme: dark", css.read_text())
        self.assertIn("--background:", css.read_text())
        self.assertIn(".control-panel", css.read_text())
        self.assertIn('class="masthead"', html.read_text())
        self.assertIn('aria-live="polite"', html.read_text())

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

    def test_canonical_db_manager_and_classifications(self):
        canonical = ROOT / "components/templates/db-server/interface/DbMgr.py"
        self.assertTrue(canonical.is_file())
        code = canonical.read_text()
        syntax = ast.parse(code)
        imports = set()
        for node in ast.walk(syntax):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
        self.assertEqual(imports, {"contextlib", "pymysql", "pymysql.cursors"})
        self.assertIn('BMFORGE_COMPONENT = {"id": "bmforge.db-server", "spec_version": "0.5.0"}', code)
        self.assertNotIn("from bmgeoip", code)
        self.assertNotIn("from mycount", code)
        spec = (ROOT / "pages/component-db-server.md").read_text()
        self.assertIn("components/templates/db-server/interface/DbMgr.py", spec)
        self.assertIn("## Canonical implementation and layered DAL", spec)
        roles = (ROOT / "pages/classification.md").read_text()
        for role in ("Activity", "Interface", "Entity"):
            self.assertIn(role, roles)
        self.assertIn("pages/classification.md", (ROOT / "AGENTS.md").read_text())
        self.assertIn("pages/classification.md", (ROOT / "index.md").read_text())
        for path in ("mycount/activity/CollectVisit.py", "mycount/interface/VisitDb.py",
                     "mycount/entity/Visit.py"):
            self.assertTrue((ROOT / "components/reference/mycount" / path).is_file(), path)

    def test_zmq_rejects_bad_unicode_without_worker_failure(self):
        spec = (ROOT / "pages/component-zmq.md").read_text()
        self.assertIn("lone UTF-16 surrogates", spec)
        self.assertIn("same server", spec)
        skill = (ROOT / "skills/bmforge-zmq/SKILL.md").read_text()
        self.assertIn("escaped lone Unicode surrogates", skill)
        self.assertIn(VERSIONS["zmq"], skill)

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
