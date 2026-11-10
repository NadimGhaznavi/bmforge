"""Smoke checks for the ZeroMQ documentation/skill contract split."""

from pathlib import Path
import unittest
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


class ZeroMQDocumentationTest(unittest.TestCase):
    def test_machine_contract_is_still_authoritative(self):
        manager = (ROOT / "skills/bmforge/scripts/manage.py").read_text()
        contract = (ROOT / "pages/component-zmq-contract.md").read_text()
        overview = (ROOT / "pages/component-zmq.md").read_text()

        self.assertIn('"bmforge-zmq": ("pages/component-zmq-contract.md"', manager)
        for required in ('component_id: "bmforge.zmq-server"',
                         'spec_version: "0.4.0"',
                         "## Approved runtime modules",
                         "## Required contract",
                         "## Acceptance checks"):
            self.assertIn(required, contract)
        self.assertNotIn("## Required contract", overview)
        self.assertIn("{% link pages/component-zmq-contract.md %}", overview)

    def test_architecture_view_has_each_layer_and_source_links(self):
        overview = (ROOT / "pages/component-zmq.md").read_text()
        for section in ("## Use cases", "## Analysis model", "## Design model",
                        "## Implementation and source", "## Traceability"):
            self.assertIn(section, overview)
        for path in ("zmq/ZMQServer.py", "zmq/ZMQMsg.py",
                     "server/LookupHandler.py", "constants/DZMQ.py"):
            self.assertIn(path, overview)
        self.assertIn("no pinned client snapshot yet", overview)

    def test_diagrams_are_valid_accessible_svg(self):
        for name in ("zmq-architecture.svg", "zmq-exchange.svg"):
            path = ROOT / "pages/images" / name
            root = ElementTree.parse(path).getroot()
            self.assertTrue(root.tag.endswith("svg"))
            self.assertEqual(root.get("role"), "img")
            self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"))
            self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}desc"))


if __name__ == "__main__":
    unittest.main()
