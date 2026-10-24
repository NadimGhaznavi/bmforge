"""Check the contract, navigation and local component reference inventory."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = {
    "http": "bmforge.http-server",
    "zmq": "bmforge.zmq-server",
    "database": "bmforge.mariadb-access",
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
