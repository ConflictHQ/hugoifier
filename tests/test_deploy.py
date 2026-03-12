"""Tests for utils.deploy."""
import unittest

from hugoifier.utils.deploy import deploy


class TestDeploy(unittest.TestCase):
    def test_returns_complete_message(self):
        result = deploy("/some/path", "example.com")
        self.assertIn("complete", result.lower())

    def test_accepts_path_and_zone(self):
        result = deploy("/tmp/site", "zone-id-123")
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
