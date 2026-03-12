"""Tests for utils.parser."""
import unittest

from hugoifier.utils.parser import parse


class TestParse(unittest.TestCase):
    def test_returns_complete_message(self):
        result = parse("/some/path")
        self.assertIn("complete", result.lower())

    def test_accepts_path(self):
        result = parse("/tmp/site")
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
