"""Tests for utils.cloudflare."""
import unittest

from hugoifier.utils.cloudflare import configure_cloudflare


class TestConfigureCloudflare(unittest.TestCase):
    def test_returns_complete_message(self):
        result = configure_cloudflare("/some/path", "example.com")
        self.assertIn("complete", result.lower())

    def test_accepts_path_and_zone(self):
        result = configure_cloudflare("/tmp/site", "zone-id-123")
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
