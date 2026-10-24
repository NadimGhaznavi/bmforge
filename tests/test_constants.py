"""Keep the canonical message-key declaration aligned with English catalogue."""

import ast
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DTEXT = ROOT / "components/templates/constants/DText.py"
CATALOGUE = ROOT / "components/templates/localization/locales/en.json"
LOCALIZER = ROOT / "components/templates/localization/interface/Localizer.py"


class ConstantsTests(unittest.TestCase):
    def test_dtext_keys_match_english_catalogue(self):
        source = ast.parse(DTEXT.read_text(encoding="utf-8"))
        cls = next(node for node in source.body if isinstance(node, ast.ClassDef) and node.name == "DText")
        values = {node.value.value for node in cls.body if isinstance(node, ast.Assign)
                  and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)}
        # StrEnum members use simple assignments, not handwritten UI labels.
        self.assertEqual(values, set(json.loads(CATALOGUE.read_text(encoding="utf-8"))))

    def test_module_import_allowlist(self):
        expected = {"json", "pathlib", "re", "string"}
        imported = set()
        for item in ast.walk(ast.parse(LOCALIZER.read_text(encoding="utf-8"))):
            if isinstance(item, ast.Import):
                imported.update(alias.name for alias in item.names)
            elif isinstance(item, ast.ImportFrom):
                imported.add(item.module)
        self.assertEqual(imported, expected)
        self.assertIn('BMFORGE_COMPONENT = {"id": "bmforge.localization", "spec_version": "0.1.0"}',
                      LOCALIZER.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
