"""
Low-level HTML analysis utility.
For the CLI, use utils/analyze.py instead.
"""

from config import call_ai

SYSTEM = "You are an expert Hugo theme developer analyzing HTML files for conversion."


def analyze_html(html_content: str) -> str:
    """Analyze an HTML string and suggest Hugo template tags and partials."""
    prompt = f"""Analyze this HTML and provide:
1. Reusable components to extract as partials (header, footer, nav, sidebar, etc.)
2. Hugo template tags to replace hardcoded content
3. Recommended Hugo partial splits
4. Content sections suitable for data/ YAML files

HTML:
{html_content[:20000]}"""

    return call_ai(prompt, SYSTEM)
