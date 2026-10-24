"""Test the standalone localizer without external services or packages."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "components/templates/localization/interface/Localizer.py"
spec = importlib.util.spec_from_file_location("bmforge_localizer", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Localizer = module.Localizer


class LocalizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bmforge-locales-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.catalog("en", {"app.title": "Application", "welcome": "Hello {name}",
                            "status.running": "Running", "language.name": "English"})
        self.catalog("fr", {"app.title": "Application FR", "welcome": "Bonjour {name}"})
        self.catalog("zh-CN", {"app.title": "简体中文"})
        self.catalog("zh-TW", {"app.title": "繁體中文"})
        self.translations = Localizer(self.folder)

    def catalog(self, language, contents):
        (self.folder / (language + ".json")).write_text(
            json.dumps(contents, ensure_ascii=False), encoding="utf-8")

    def test_catalogues_load_and_do_not_mutate(self):
        self.assertEqual(self.translations.default_language, "en")
        self.assertEqual(set(self.translations.languages), {"en", "fr", "zh-CN", "zh-TW"})
        self.assertEqual(self.translations.text("app.title", locale="zh-CN"), "简体中文")
        self.assertEqual(self.translations.text("welcome", locale="fr", name="Claude"), "Bonjour Claude")
        self.assertEqual(self.translations.text("status.running", locale="fr"), "Running")

    def test_explicit_choice_overrides_browser(self):
        self.assertEqual(self.translations.select(explicit="zh-TW", accept_language="fr,zh-CN"), "zh-TW")
        self.assertEqual(self.translations.select(explicit="it", accept_language="fr"), "en")

    def test_browser_language_quality_and_order(self):
        self.assertEqual(self.translations.select(accept_language="it, fr-CA;q=0.6, zh-CN;q=0.8"), "zh-CN")
        self.assertEqual(self.translations.select(accept_language="it, fr-CA;q=0.8, zh-TW;q=0.2"), "fr")
        self.assertEqual(self.translations.select(accept_language="fr;q=0,zh-CN;q=0.5"), "zh-CN")
        self.assertEqual(self.translations.select(accept_language="it,fr;q=invalid"), "en")

    def test_parents_not_sibling_locales(self):
        self.assertEqual(self.translations.select(explicit="ZH_cn"), "zh-CN")
        self.assertEqual(self.translations.select(explicit="zh-Hant-HK"), "en")
        self.assertEqual(self.translations.select(explicit="fr-CA"), "fr")
        self.assertEqual(self.translations.select(explicit="zh-MO"), "en")

    def test_missing_default_fails(self):
        (self.folder / "en.json").unlink()
        with self.assertRaisesRegex(ValueError, "Missing default language"):
            Localizer(self.folder)

    def test_unknown_english_key_is_error(self):
        with self.assertRaises(KeyError):
            self.translations.text("unknown", locale="fr")

    def test_missing_placeholder_values_are_errors(self):
        with self.assertRaises(KeyError):
            self.translations.text("welcome", locale="en")

    def test_translated_placeholder_mismatch_is_rejected(self):
        self.catalog("fr", {"welcome": "Bonjour {first}"})
        with self.assertRaisesRegex(ValueError, "placeholders differ"):
            Localizer(self.folder)

    def test_unsafe_placeholder_expressions_rejected(self):
        self.catalog("en", {"app.title": "Application", "welcome": "Hello {name.__class__}",
                            "status.running": "Running", "language.name": "English"})
        with self.assertRaisesRegex(ValueError, "Unsupported translation placeholder"):
            Localizer(self.folder)

    def test_unexpected_translation_keys_are_rejected(self):
        self.catalog("fr", {"unrecognized": "Oops"})
        with self.assertRaisesRegex(ValueError, "Unexpected translation keys"):
            Localizer(self.folder)

    def test_invalid_locale_catalogue_is_rejected(self):
        self.catalog("what a language", {"app.title": "Wrong"})
        with self.assertRaisesRegex(ValueError, "Invalid or duplicate"):
            Localizer(self.folder)

    def test_exact_no_cross_request_locale_state(self):
        self.assertEqual(self.translations.text("app.title", locale="fr"), "Application FR")
        self.assertEqual(self.translations.text("app.title", locale="zh-CN"), "简体中文")
        self.assertEqual(self.translations.text("app.title"), "Application")
        self.assertEqual(module.BMFORGE_COMPONENT["id"], "bmforge.localization")


if __name__ == "__main__":
    unittest.main()
