"""Tests for utils.translate."""
import os
import tempfile
import unittest
from unittest.mock import patch


class TestTranslate(unittest.TestCase):
    def test_translates_file_content(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<p>Hello world</p>")
            path = f.name
        try:
            from utils.translate import translate
            with patch("utils.translate.call_ai", return_value="<p>Hola mundo</p>") as mock_ai:
                result = translate(path, target_language="Spanish")
                self.assertEqual(result, "<p>Hola mundo</p>")
                call_args = mock_ai.call_args[0][0]
                self.assertIn("Spanish", call_args)
                self.assertIn("Hello world", call_args)
        finally:
            os.unlink(path)

    def test_uses_target_language_param(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            f.write("<p>Bonjour</p>")
            path = f.name
        try:
            from utils.translate import translate
            with patch("utils.translate.call_ai", return_value="<p>Hallo</p>") as mock_ai:
                translate(path, target_language="German")
                call_args = mock_ai.call_args[0][0]
                self.assertIn("German", call_args)
        finally:
            os.unlink(path)

    def test_returns_error_on_missing_file(self):
        from utils.translate import translate
        result = translate("/nonexistent/file.html")
        self.assertIn("failed", result.lower())


if __name__ == "__main__":
    unittest.main()
