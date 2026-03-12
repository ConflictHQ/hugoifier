"""Tests for utils.theme_finder."""
import os
import tempfile
import unittest

from utils.theme_finder import find_hugo_theme, find_raw_html_files


def _make_hugo_theme(base_dir, theme_name="test-theme"):
    """Create a minimal Hugo theme structure."""
    layouts = os.path.join(base_dir, theme_name, "layouts", "_default")
    os.makedirs(layouts)
    open(os.path.join(layouts, "baseof.html"), "w").close()
    return os.path.join(base_dir, theme_name)


class TestFindHugoTheme(unittest.TestCase):
    def test_finds_theme_with_layouts(self):
        with tempfile.TemporaryDirectory() as tmp:
            theme_path = _make_hugo_theme(tmp)
            result = find_hugo_theme(theme_path)
            self.assertIsNotNone(result)
            self.assertTrue(result["is_hugo_theme"])
            self.assertEqual(result["theme_name"], "test-theme")

    def test_finds_example_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            theme_path = _make_hugo_theme(tmp)
            example = os.path.join(theme_path, "exampleSite")
            os.makedirs(example)
            result = find_hugo_theme(theme_path)
            self.assertEqual(result["example_site"], example)

    def test_returns_none_for_non_hugo_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "css"))
            open(os.path.join(tmp, "index.html"), "w").close()
            result = find_hugo_theme(tmp)
            self.assertIsNone(result)

    def test_skips_macosx_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            # MACOSX junk should not be mistaken for a theme
            junk = os.path.join(tmp, "__MACOSX", "layouts", "_default")
            os.makedirs(junk)
            result = find_hugo_theme(tmp)
            self.assertIsNone(result)


class TestFindRawHtmlFiles(unittest.TestCase):
    def test_finds_html_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "index.html"), "w").close()
            open(os.path.join(tmp, "about.html"), "w").close()
            result = find_raw_html_files(tmp)
            self.assertEqual(len(result), 2)
            basenames = {os.path.basename(f) for f in result}
            self.assertIn("index.html", basenames)
            self.assertIn("about.html", basenames)

    def test_excludes_example_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            example = os.path.join(tmp, "exampleSite")
            os.makedirs(example)
            open(os.path.join(example, "index.html"), "w").close()
            open(os.path.join(tmp, "page.html"), "w").close()
            result = find_raw_html_files(tmp)
            self.assertEqual(len(result), 1)
            self.assertEqual(os.path.basename(result[0]), "page.html")

    def test_returns_empty_for_no_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, "style.css"), "w").close()
            result = find_raw_html_files(tmp)
            self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
