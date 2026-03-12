"""Tests for utils.complete helpers."""
import os
import tempfile
import unittest

from utils.complete import _pick_main_html, _copy_dir, _find_config, _write_minimal_hugo_toml


class TestPickMainHtml(unittest.TestCase):
    def test_prefers_index_html(self):
        files = ["/path/about.html", "/path/index.html", "/path/contact.html"]
        self.assertEqual(_pick_main_html(files), "/path/index.html")

    def test_prefers_home_html(self):
        files = ["/path/about.html", "/path/home.html"]
        self.assertEqual(_pick_main_html(files), "/path/home.html")

    def test_falls_back_to_first(self):
        files = ["/path/about.html", "/path/services.html"]
        self.assertEqual(_pick_main_html(files), "/path/about.html")


class TestCopyDir(unittest.TestCase):
    def test_copies_files(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
            open(os.path.join(src, "file.txt"), "w").close()
            _copy_dir(src, dst)
            self.assertTrue(os.path.exists(os.path.join(dst, "file.txt")))

    def test_excludes_specified_names(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
            open(os.path.join(src, "keep.txt"), "w").close()
            open(os.path.join(src, "skip.txt"), "w").close()
            _copy_dir(src, dst, exclude={"skip.txt"})
            self.assertTrue(os.path.exists(os.path.join(dst, "keep.txt")))
            self.assertFalse(os.path.exists(os.path.join(dst, "skip.txt")))

    def test_excludes_dotfiles_starting_with_dot_underscore(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
            open(os.path.join(src, "._junk"), "w").close()
            open(os.path.join(src, "real.txt"), "w").close()
            _copy_dir(src, dst)
            self.assertFalse(os.path.exists(os.path.join(dst, "._junk")))
            self.assertTrue(os.path.exists(os.path.join(dst, "real.txt")))

    def test_nonexistent_src_is_safe(self):
        with tempfile.TemporaryDirectory() as dst:
            _copy_dir("/nonexistent/src", dst)  # should not raise

    def test_recurses_into_subdirs(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
            nested = os.path.join(src, "sub")
            os.makedirs(nested)
            open(os.path.join(nested, "nested.txt"), "w").close()
            _copy_dir(src, dst)
            self.assertTrue(os.path.exists(os.path.join(dst, "sub", "nested.txt")))


class TestFindConfig(unittest.TestCase):
    def test_finds_hugo_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "hugo.toml")
            open(path, "w").close()
            self.assertEqual(_find_config(tmp), path)

    def test_finds_config_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "config.toml")
            open(path, "w").close()
            self.assertEqual(_find_config(tmp), path)

    def test_prefers_hugo_toml_over_config_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            hugo = os.path.join(tmp, "hugo.toml")
            config = os.path.join(tmp, "config.toml")
            open(hugo, "w").close()
            open(config, "w").close()
            self.assertEqual(_find_config(tmp), hugo)

    def test_finds_nested_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = os.path.join(tmp, "config", "_default")
            os.makedirs(nested)
            path = os.path.join(nested, "config.toml")
            open(path, "w").close()
            self.assertEqual(_find_config(tmp), path)

    def test_returns_none_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(_find_config(tmp))


class TestWriteMinimalHugoToml(unittest.TestCase):
    def test_writes_valid_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_minimal_hugo_toml(tmp, "my-theme")
            path = os.path.join(tmp, "hugo.toml")
            self.assertTrue(os.path.exists(path))
            with open(path) as f:
                content = f.read()
            self.assertIn('theme = "my-theme"', content)
            self.assertIn("My Theme", content)

    def test_sanitizes_quotes_in_theme_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            _write_minimal_hugo_toml(tmp, 'evil"theme')
            with open(os.path.join(tmp, "hugo.toml")) as f:
                content = f.read()
            # Should not contain unescaped quote that breaks TOML
            self.assertNotIn('theme = "evil"theme"', content)


if __name__ == "__main__":
    unittest.main()
