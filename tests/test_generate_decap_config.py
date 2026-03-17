"""Tests for utils.generate_decap_config (thin wrapper around decapify)."""
import os
import tempfile
import unittest

from hugoifier.utils.generate_decap_config import generate_decap_config


class TestGenerateDecapConfig(unittest.TestCase):
    def test_creates_admin_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            generate_decap_config(tmp)
            self.assertTrue(os.path.isdir(os.path.join(tmp, "static", "admin")))

    def test_creates_index_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            generate_decap_config(tmp)
            self.assertTrue(os.path.exists(os.path.join(tmp, "static", "admin", "index.html")))

    def test_creates_config_yml(self):
        with tempfile.TemporaryDirectory() as tmp:
            generate_decap_config(tmp)
            self.assertTrue(os.path.exists(os.path.join(tmp, "static", "admin", "config.yml")))

    def test_returns_status_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = generate_decap_config(tmp)
            self.assertIsInstance(result, str)
            self.assertIn("complete", result.lower())

    def test_config_yml_has_backend(self):
        with tempfile.TemporaryDirectory() as tmp:
            generate_decap_config(tmp)
            with open(os.path.join(tmp, "static", "admin", "config.yml")) as f:
                content = f.read()
            self.assertIn("backend", content)
            self.assertIn("github", content)


if __name__ == "__main__":
    unittest.main()
