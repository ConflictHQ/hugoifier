"""Tests for config.py."""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock


class TestCallAiRouting(unittest.TestCase):
    def _get_config(self):
        # Reload config to pick up env var changes
        import importlib
        import config
        importlib.reload(config)
        return config

    def test_raises_on_unknown_backend(self):
        with patch.dict(os.environ, {"HUGOIFIER_BACKEND": "unknown"}):
            cfg = self._get_config()
            with self.assertRaises(ValueError):
                cfg.call_ai("test prompt")

    def test_anthropic_raises_without_key(self):
        env = {"HUGOIFIER_BACKEND": "anthropic", "ANTHROPIC_API_KEY": ""}
        with patch.dict(os.environ, env, clear=False):
            cfg = self._get_config()
            cfg.ANTHROPIC_API_KEY = ""
            with self.assertRaises(EnvironmentError):
                cfg._call_anthropic("prompt", "system")

    def test_openai_raises_without_key(self):
        env = {"HUGOIFIER_BACKEND": "openai", "OPENAI_API_KEY": ""}
        with patch.dict(os.environ, env, clear=False):
            cfg = self._get_config()
            cfg.OPENAI_API_KEY = ""
            with self.assertRaises(EnvironmentError):
                cfg._call_openai("prompt", "system")

    def test_google_raises_without_key(self):
        env = {"HUGOIFIER_BACKEND": "google", "GOOGLE_API_KEY": ""}
        with patch.dict(os.environ, env, clear=False):
            cfg = self._get_config()
            cfg.GOOGLE_API_KEY = ""
            with self.assertRaises(EnvironmentError):
                cfg._call_google("prompt", "system")

    def test_anthropic_backend_calls_anthropic(self):
        import config
        with patch.object(config, '_call_anthropic', return_value="response") as mock_fn:
            config.BACKEND = 'anthropic'
            result = config.call_ai("hello")
            mock_fn.assert_called_once()
            self.assertEqual(result, "response")

    def test_openai_backend_calls_openai(self):
        import config
        with patch.object(config, '_call_openai', return_value="response") as mock_fn:
            config.BACKEND = 'openai'
            result = config.call_ai("hello")
            mock_fn.assert_called_once()
            self.assertEqual(result, "response")

    def test_google_backend_calls_google(self):
        import config
        with patch.object(config, '_call_google', return_value="response") as mock_fn:
            config.BACKEND = 'google'
            result = config.call_ai("hello")
            mock_fn.assert_called_once()
            self.assertEqual(result, "response")


if __name__ == "__main__":
    unittest.main()
