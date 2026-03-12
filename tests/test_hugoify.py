"""Tests for utils.hugoify."""
import os
import tempfile
import unittest

from hugoifier.utils.hugoify import _fallback_baseof, _parse_layout_json, hugoify_dir


class TestParseLayoutJson(unittest.TestCase):
    def test_parses_valid_json(self):
        response = '{"_default/baseof.html": "<!doctype html>", "index.html": "{{ define \\"main\\" }}{{ end }}"}'
        result = _parse_layout_json(response)
        self.assertIn("_default/baseof.html", result)
        self.assertEqual(result["_default/baseof.html"], "<!doctype html>")

    def test_extracts_json_from_prose(self):
        response = 'Here is the converted theme:\n{"_default/baseof.html": "<html></html>"}\nDone.'
        result = _parse_layout_json(response)
        self.assertIn("_default/baseof.html", result)

    def test_falls_back_on_invalid_json(self):
        result = _parse_layout_json("This is not JSON at all.")
        self.assertIn("_default/baseof.html", result)
        self.assertIn("partials/header.html", result)
        self.assertIn("partials/footer.html", result)
        self.assertIn("index.html", result)

    def test_fallback_contains_valid_hugo_syntax(self):
        result = _parse_layout_json("not json")
        baseof = result["_default/baseof.html"]
        self.assertIn("block", baseof)
        self.assertIn("partial", baseof)


class TestFallbackBaseof(unittest.TestCase):
    def test_contains_required_hugo_blocks(self):
        result = _fallback_baseof()
        self.assertIn('block "main"', result)
        self.assertIn('partial "header.html"', result)
        self.assertIn('partial "footer.html"', result)
        self.assertIn("<!DOCTYPE html>", result)

    def test_contains_language_code(self):
        result = _fallback_baseof()
        self.assertIn(".Site.LanguageCode", result)


class TestHugoifyDir(unittest.TestCase):
    def test_valid_theme_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseof = os.path.join(tmp, "layouts", "_default", "baseof.html")
            os.makedirs(os.path.dirname(baseof))
            open(baseof, "w").close()
            result = hugoify_dir(tmp)
            self.assertIn("Valid", result)

    def test_missing_layouts_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = hugoify_dir(tmp)
            self.assertIn("failed", result.lower())

    def test_missing_baseof_reports_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "layouts", "_default"))
            result = hugoify_dir(tmp)
            self.assertIn("baseof.html", result)


if __name__ == "__main__":
    unittest.main()
