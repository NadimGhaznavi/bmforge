"""Validate the standalone component-blueprint documentation and source inventory."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ComponentBlueprintTests(unittest.TestCase):
    def test_all_blueprints_exist_and_are_linked(self):
        home = (ROOT / "index.md").read_text()
        guide = (ROOT / "pages/component-blueprints.md").read_text()
        for name in ("http", "zmq", "database"):
            path = ROOT / f"pages/component-{name}.md"
            self.assertTrue(path.is_file(), path)
            self.assertIn(f"pages/component-{name}.md", home)
            self.assertIn(f"pages/component-{name}.md", guide)
            body = path.read_text()
            self.assertIn("## Acceptance checks", body)
            self.assertIn("components/reference/bmgeoip/", body)

    def test_reference_snapshots_are_local(self):
        base = ROOT / "components/reference/bmgeoip/bmgeoip"
        paths = ("server/BMGeoIPServer.py", "server/BMGeoIPHandler.py",
                 "server/LookupHandler.py", "zmq/ZMQServer.py",
                 "zmq/ZMQMsg.py", "interface/DbMgr.py",
                 "interface/DatabaseEnvironment.py", "interface/GeoIpDb.py",
                 "constants/DZMQ.py", "constants/DGeoIp.py")
        for path in paths:
            self.assertTrue((base / path).is_file(), path)

    def test_agent_contract_mentions_no_runtime_linkage(self):
        agent = (ROOT / "AGENTS.md").read_text()
        self.assertIn("Never add BMForge", agent)
        self.assertIn("public APIs", agent)

if __name__ == "__main__":
    unittest.main()
