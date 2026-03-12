"""
Translates web content using the configured AI backend.
"""

import logging

from ..config import call_ai


def translate(path: str, target_language: str = "Spanish") -> str:
    logging.info(f"Translating content in {path} ...")
    try:
        with open(path, 'r', errors='replace') as f:
            content = f.read()

        prompt = f"""Translate the following web content to {target_language}.
Preserve all HTML tags and formatting. Only translate visible text.

Content:
{content[:20000]}"""

        return call_ai(prompt, "You are a professional translator.")
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return f"Translation failed: {e}"
