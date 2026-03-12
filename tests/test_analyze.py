"""Tests for utils.analyze."""
import os
import tempfile
import unittest

from hugoifier.utils.analyze import _analyze_hugo_theme


class TestAnalyzeHugoTheme(unittest.TestCase):
    def _make_theme_info(self, tmp, layouts=None, example_site=None):
        theme_dir = os.path.join(tmp, "test-theme")
        layouts_dir = os.path.join(theme_dir, "layouts", "_default")
        os.makedirs(layouts_dir)
        for name in (layouts or ["baseof.html", "single.html"]):
            open(os.path.join(layouts_dir, name), "w").close()
        return {
            "theme_dir": theme_dir,
            "theme_name": "test-theme",
            "example_site": example_site,
            "is_hugo_theme": True,
        }

    def test_reports_theme_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            info = self._make_theme_info(tmp)
            result = _analyze_hugo_theme(info)
            self.assertIn("test-theme", result)

    def test_lists_layout_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            info = self._make_theme_info(tmp, layouts=["baseof.html", "single.html"])
            result = _analyze_hugo_theme(info)
            self.assertIn("baseof.html", result)
            self.assertIn("single.html", result)

    def test_reports_no_example_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            info = self._make_theme_info(tmp, example_site=None)
            result = _analyze_hugo_theme(info)
            self.assertIn("none", result.lower())

    def test_reports_content_types_from_example_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            info = self._make_theme_info(tmp)
            example = os.path.join(tmp, "exampleSite")
            content = os.path.join(example, "content", "blog")
            os.makedirs(content)
            info["example_site"] = example
            result = _analyze_hugo_theme(info)
            self.assertIn("blog", result)

    def test_suggests_complete_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            info = self._make_theme_info(tmp)
            result = _analyze_hugo_theme(info)
            self.assertIn("complete", result)


if __name__ == "__main__":
    unittest.main()
