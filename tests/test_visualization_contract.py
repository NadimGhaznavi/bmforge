"""Static verification of the browser visualization contract and pinned references."""

from hashlib import sha1
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "pages/component-visualization.md"
REFERENCES = {
    "mycount/mycount/server/ControlPages.py": "a1c070413c368156a6b78838ee5669f58023d0a4",
    "mycount/mycount/server/templates/base.html": "f0bbb26697ba744f8593414f023bb920e72e4ecb",
    "mycount/mycount/server/templates/chart_theme.html": "3ab811be552fddb454bcda222d031fa905bfa0ba",
    "mycount/mycount/server/templates/all_traffic.html": "1154d48d409022ea46fa97242ded7b56fe23f315",
    "mycount/mycount/server/templates/pie_charts.html": "f5cfaade3987501151c32827a362d25f3a77e7a6",
    "mycount/mycount/server/templates/marketing_chart.html": "e24e81f48d67e072e9d65f73645e43b39f94a9ea",
    "mycount/mycount/server/templates/visitor_map.html": "baf2b5b630644f966deba018ef12b090a8bd012a",
    "cmdb/cmdb/server/templates/home.html": "8e7c15d09b89cb1af851d3e48d2a99c79ee325c7",
    "cmdb/cmdb/server/static/machines.js": "fc46c0780b9d3532f4dbba85597dd20d8e6e2976",
    "cmdb/cmdb/server/static/vendor/cytoscape-3.34.3.min.js":
        "bab26b7665cbaa4307cf26755fa0fd69dc7d6aad",
    "cmdb/cmdb/server/static/vendor/cytoscape-LICENSE":
        "aac05f201cb14147da8c5ffcbc56ddbf9c954ccc",
}


def git_blob_id(data: bytes) -> str:
    return sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class VisualizationContractTests(unittest.TestCase):
    def test_approved_libraries_and_exact_versions(self):
        spec = SPEC.read_text()
        self.assertIn('component_id: "bmforge.visualization"', spec)
        self.assertIn('spec_version: "0.1.0"', spec)
        self.assertIn('spec_status: "draft"', spec)
        self.assertIn("## Approved runtime modules", spec)
        for capability, library, version in (
            ("Charts:", "Plotly.js", "4.1.1"),
            ("Geographic map:", "Leaflet", "1.9.4"),
            ("Relationship, network or topology graph:", "Cytoscape.js", "3.34.3"),
        ):
            line = next(line for line in spec.splitlines() if line.startswith("| " + capability))
            self.assertIn(f"**{library}**", line)
            self.assertIn(f"**{version}**", line)
        self.assertIn("not a requirement to load all three", spec)
        self.assertIn("stop and ask the user", spec)
        self.assertIn("Python `plotly` package is not required", spec)

    def test_reference_snapshots_are_exactly_pinned(self):
        spec = SPEC.read_text()
        self.assertIn("90574cd838ba43499a825c6a193b43cbc485c91c", spec)
        self.assertIn("43438d9c41949ef70a635884a9bd6885d5c5f22c", spec)
        for relative, checksum in REFERENCES.items():
            path = ROOT / "components/reference" / relative
            self.assertTrue(path.is_file(), relative)
            self.assertEqual(git_blob_id(path.read_bytes()), checksum, relative)

    def test_current_sources_match_library_choices(self):
        base = ROOT / "components/reference/mycount/mycount/server/templates"
        plot = (base / "chart_theme.html").read_text()
        self.assertIn("https://cdn.plot.ly/plotly-4.1.1.min.js", plot)
        for template in ("all_traffic.html", "pie_charts.html", "marketing_chart.html"):
            self.assertIn("Plotly.newPlot", (base / template).read_text())
        leaflet = (base / "visitor_map.html").read_text()
        self.assertIn("leaflet@1.9.4/dist/leaflet.js", leaflet)
        self.assertIn("leaflet@1.9.4/dist/leaflet.css", leaflet)
        self.assertIn("L.map(", leaflet)
        self.assertIn("tile.openstreetmap.org", leaflet)
        cmdb = ROOT / "components/reference/cmdb/cmdb/server"
        self.assertIn("cytoscape-3.34.3.min.js", (cmdb / "templates/home.html").read_text())
        self.assertIn("cytoscape({", (cmdb / "static/machines.js").read_text())
        self.assertIn("Permission is hereby granted", (cmdb / "static/vendor/cytoscape-LICENSE").read_text())
        self.assertIn("from jinja2 import", (ROOT / "components/reference/mycount/mycount/server/ControlPages.py").read_text())

    def test_codex_navigation_and_jekyll_links(self):
        paths = ("index.md", "AGENTS.md", "pages/component-blueprints.md",
                 "pages/component-http.md", "pages/engineering-contract.md",
                 "pages/component-visualization.md")
        for relative in paths:
            content = (ROOT / relative).read_text()
            if relative != "pages/component-visualization.md":
                self.assertIn("pages/component-visualization.md", content, relative)
            for match in re.findall(r"{%\s*link\s+([^\s%]+)\s*%}", content):
                self.assertTrue((ROOT / match).is_file(), f"{relative} -> {match}")


if __name__ == "__main__":
    unittest.main()
