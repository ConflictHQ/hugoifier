"""Tests for utils.theme_patcher."""
import os
import tempfile
import unittest

from utils.theme_patcher import patch_theme, patch_config


class TestPatchTheme(unittest.TestCase):
    def _write_layout(self, layouts_dir, name, content):
        path = os.path.join(layouts_dir, name)
        with open(path, "w") as f:
            f.write(content)
        return path

    def test_patches_disqus_shortname(self):
        with tempfile.TemporaryDirectory() as tmp:
            layouts = os.path.join(tmp, "layouts")
            os.makedirs(layouts)
            self._write_layout(layouts, "single.html", "{{ .Site.DisqusShortname }}")
            patch_theme(tmp)
            with open(os.path.join(layouts, "single.html")) as f:
                result = f.read()
            self.assertIn(".Site.Config.Services.Disqus.Shortname", result)
            self.assertNotIn(".Site.DisqusShortname", result)

    def test_patches_google_analytics(self):
        with tempfile.TemporaryDirectory() as tmp:
            layouts = os.path.join(tmp, "layouts")
            os.makedirs(layouts)
            self._write_layout(layouts, "head.html", "{{ .Site.GoogleAnalytics }}")
            patch_theme(tmp)
            with open(os.path.join(layouts, "head.html")) as f:
                result = f.read()
            self.assertIn(".Site.Config.Services.GoogleAnalytics.ID", result)

    def test_no_change_when_already_patched(self):
        with tempfile.TemporaryDirectory() as tmp:
            layouts = os.path.join(tmp, "layouts")
            os.makedirs(layouts)
            content = "{{ .Site.Config.Services.Disqus.Shortname }}"
            self._write_layout(layouts, "single.html", content)
            patch_theme(tmp)
            with open(os.path.join(layouts, "single.html")) as f:
                result = f.read()
            self.assertEqual(result, content)

    def test_no_layouts_dir_is_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Should not raise even if layouts/ doesn't exist
            patch_theme(tmp)


class TestPatchConfig(unittest.TestCase):
    def _write_config(self, path, content):
        with open(path, "w") as f:
            f.write(content)

    def test_patches_paginate(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = os.path.join(tmp, "hugo.toml")
            self._write_config(cfg, 'paginate = 10\ntitle = "My Site"\n')
            patch_config(cfg)
            with open(cfg) as f:
                result = f.read()
            self.assertIn("[pagination]", result)
            self.assertIn("pagerSize = 10", result)
            self.assertNotIn("paginate = 10", result)

    def test_patches_google_analytics_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = os.path.join(tmp, "hugo.toml")
            self._write_config(cfg, 'googleAnalytics = "UA-12345"\n')
            patch_config(cfg)
            with open(cfg) as f:
                result = f.read()
            self.assertIn("[services.googleAnalytics]", result)
            self.assertIn('id = "UA-12345"', result)

    def test_patches_disqus_shortname(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = os.path.join(tmp, "hugo.toml")
            self._write_config(cfg, 'disqusShortname = "mysite"\n')
            patch_config(cfg)
            with open(cfg) as f:
                result = f.read()
            self.assertIn("[services.disqus]", result)
            self.assertIn('shortname = "mysite"', result)

    def test_no_change_when_nothing_to_patch(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = os.path.join(tmp, "hugo.toml")
            content = 'title = "Clean Site"\n'
            self._write_config(cfg, content)
            patch_config(cfg)
            with open(cfg) as f:
                result = f.read()
            self.assertEqual(result, content)


if __name__ == "__main__":
    unittest.main()
