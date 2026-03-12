"""
AI-powered HTML → Hugo template conversion.

For already-Hugo themes, use hugoify_dir() to validate/augment.
For raw HTML, use hugoify_html() to produce Hugo layout files.
"""

import json
import logging
import os
import re

from ..config import call_ai

SYSTEM = (
    "You are an expert Hugo theme developer. Convert HTML templates to valid Hugo Go template files. "
    "Output only valid Hugo template syntax — no explanations, no markdown fences."
)


def hugoify_html(html_path: str) -> dict:
    """
    Convert a raw HTML file to a set of Hugo layout files.

    Returns dict mapping relative layout paths to their content, e.g.:
      {
        "_default/baseof.html": "<!DOCTYPE html>...",
        "partials/header.html": "<header>...",
        "partials/footer.html": "<footer>...",
        "index.html": "{{ define \"main\" }}...",
      }
    """
    logging.info(f"Hugoifying {html_path} ...")

    with open(html_path, 'r', errors='replace') as f:
        html = f.read()

    # Truncate very large files to avoid token limits
    if len(html) > 30000:
        logging.warning(f"HTML is large ({len(html)} chars), truncating to 30000 for AI analysis")
        html = html[:30000]

    prompt = f"""Convert the following HTML file into Hugo layout files.

Return a JSON object where keys are relative file paths under layouts/ and values are the Hugo template content.

Required keys to produce:
- "_default/baseof.html" — base template with blocks for head, header, main, footer
- "partials/header.html" — site header/nav extracted as partial
- "partials/footer.html" — footer extracted as partial
- "index.html" — homepage using {{ define "main" }} ... {{ end }}

Rules:
- Replace hardcoded page titles with {{ .Title }}
- Replace hardcoded site name with {{ .Site.Title }}
- Replace hardcoded URLs with {{ .Site.BaseURL }} or {{ .Permalink }}
- Replace nav links with {{ range .Site.Menus.main }}<a href="{{ .URL }}">{{ .Name }}</a>{{ end }}
- Replace blog post lists with {{ range .Pages }} ... {{ end }}
- Replace copyright year with {{ now.Year }}
- Keep all CSS classes and HTML structure intact
- Use {{ partial "header.html" . }} and {{ partial "footer.html" . }} in baseof.html

HTML to convert:
{html}

Return ONLY a valid JSON object, no explanation."""

    response = call_ai(prompt, SYSTEM)
    return _parse_layout_json(response)


def hugoify_dir(theme_dir: str) -> str:
    """
    Validate and optionally augment an existing Hugo theme directory.
    Returns a status message.
    """
    logging.info(f"Validating Hugo theme at {theme_dir} ...")

    issues = []
    layouts_dir = os.path.join(theme_dir, 'layouts')

    if not os.path.isdir(layouts_dir):
        issues.append("Missing layouts/ directory")
        return f"Validation failed: {'; '.join(issues)}"

    required = [
        os.path.join(layouts_dir, '_default', 'baseof.html'),
    ]
    for f in required:
        if not os.path.exists(f):
            issues.append(f"Missing {os.path.relpath(f, theme_dir)}")

    if issues:
        logging.warning(f"Issues found: {issues}")
        return f"Issues: {'; '.join(issues)}"

    logging.info("Hugo theme validation passed.")
    return "Valid Hugo theme"


# CLI entry point (used by cli.py)
def hugoify(path: str) -> str:
    """
    Entry point for the CLI 'hugoify' command.
    If path is a Hugo theme dir: validate it.
    If path is an HTML file or raw HTML dir: convert it.
    """
    from .theme_finder import find_hugo_theme, find_raw_html_files

    info = find_hugo_theme(path)
    if info:
        return hugoify_dir(info['theme_dir'])

    if os.path.isfile(path) and path.endswith('.html'):
        layouts = hugoify_html(path)
        return f"Converted to {len(layouts)} layout files: {list(layouts.keys())}"

    html_files = find_raw_html_files(path)
    if html_files:
        main = next(
            (f for f in html_files if os.path.basename(f).lower() == 'index.html'),
            html_files[0]
        )
        layouts = hugoify_html(main)
        return f"Converted to {len(layouts)} layout files"

    return f"Nothing to hugoify at {path}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_layout_json(response: str) -> dict:
    """Extract JSON from AI response, even if surrounded by prose."""
    # Try to find JSON block
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback: return a minimal layout
    logging.warning("Could not parse AI response as JSON, using fallback layouts")
    return {
        "_default/baseof.html": _fallback_baseof(),
        "partials/header.html": "<header><!-- header --></header>",
        "partials/footer.html": "<footer>{{ .Site.Params.copyright }}</footer>",
        "index.html": '{{ define "main" }}<main>{{ .Content }}</main>{{ end }}',
    }


def _fallback_baseof() -> str:
    return '''<!DOCTYPE html>
<html lang="{{ with .Site.LanguageCode }}{{ . }}{{ else }}en-US{{ end }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} | {{ .Site.Title }}{{ end }}</title>
</head>
<body>
  {{- partial "header.html" . -}}
  {{- block "main" . }}{{- end }}
  {{- partial "footer.html" . -}}
</body>
</html>'''
