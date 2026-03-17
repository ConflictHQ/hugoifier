"""
AI-powered HTML → Hugo template conversion.

For already-Hugo themes, use hugoify_dir() to validate/augment.
For raw HTML, use hugoify_html() to produce Hugo layout files.
For Next.js apps, use hugoify_nextjs() to convert React components to Hugo layouts.
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

NEXTJS_SYSTEM = (
    "You are an expert at converting React/Next.js components to Hugo Go template files. "
    "You understand JSX, TSX, React component composition, and Hugo template syntax. "
    "Convert React components to static Hugo HTML templates, preserving all CSS classes and visual structure. "
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


def hugoify_nextjs(info: dict) -> dict:
    """
    Convert a Next.js app to a set of Hugo layout files.

    Args:
        info: dict from find_nextjs_app() with app_dir, router_type, etc.

    Returns:
        dict mapping relative layout paths to their content, same format as hugoify_html().
    """
    app_dir = info['app_dir']
    logging.info(f"Hugoifying Next.js app at {app_dir} ...")

    sources = _collect_nextjs_sources(info)
    if not sources:
        logging.warning("No source files collected from Next.js app")
        return _fallback_layouts()

    # Build the source context for the AI
    source_block = ""
    for rel_path, content in sources.items():
        source_block += f"\n{'='*60}\n// FILE: {rel_path}\n{'='*60}\n{content}\n"

    prompt = f"""Convert the following Next.js React application into Hugo layout files.

The app uses the Next.js App Router with React components (TSX). Convert it to a static Hugo theme.

Return a JSON object where keys are relative file paths under layouts/ and values are the Hugo template content.

Required keys to produce:
- "_default/baseof.html" — base template with the HTML shell, <head>, and blocks
- "partials/header.html" — site header/navigation extracted as partial
- "partials/footer.html" — footer extracted as partial
- "index.html" — homepage using {{{{ define "main" }}}} ... {{{{ end }}}}
- Additional "partials/{{name}}.html" for each major section component

Conversion rules:
- JSX `className` → HTML `class`
- React component composition → Hugo partials via `{{{{ partial "name.html" . }}}}`
- `app/layout.tsx` → `_default/baseof.html` with `{{{{ block "main" . }}}}{{{{ end }}}}`
- `app/page.tsx` → `index.html` with `{{{{ define "main" }}}}...{{{{ end }}}}`
- Each section component (e.g. HeroSection, CTASection, FooterSection) → `partials/{{name}}.html`
- `<Link href="...">text</Link>` → `<a href="...">text</a>`
- `<Image src="..." alt="..." />` → `<img src="..." alt="..." />`
- next/font imports (Geist, Sora, etc.) → Google Fonts <link> tags in <head>
- Conditional rendering `{{condition && <div>...</div>}}` → render the static content
- `map()` calls over static arrays → unroll into static HTML
- Interactive elements (onClick, useState, useEffect, motion.*) → strip interactivity, keep the static HTML structure
- Animation wrappers (FadeIn, motion.div) → plain `<div>` elements preserving classes
- Preserve ALL Tailwind CSS classes and inline styles exactly as-is
- Replace hardcoded page titles with `{{{{ .Title }}}}`
- Replace hardcoded site name with `{{{{ .Site.Title }}}}`
- Replace copyright year with `{{{{ now.Year }}}}`
- For Tailwind CSS, include `<script src="https://cdn.tailwindcss.com"></script>` in the <head> of baseof.html
- Link any CSS files as `<link rel="stylesheet" href="/css/globals.css">`
- SVG content should be preserved inline as-is
- Keep all `id` attributes on sections for anchor navigation

Source files:
{source_block}

Return ONLY a valid JSON object, no explanation."""

    response = call_ai(prompt, NEXTJS_SYSTEM, max_tokens=16384)
    return _parse_layout_json(response)


def _collect_nextjs_sources(info: dict) -> dict:
    """
    Collect relevant source files from a Next.js app into a dict
    keyed by relative path. Applies priority-based context budgeting.
    """
    app_dir = info['app_dir']
    sources = {}
    budget = 80000

    # Tier 1: Layout and page entry points (always include)
    tier1 = []
    if info.get('layout_file'):
        tier1.append(info['layout_file'])
    if info.get('page_file'):
        tier1.append(info['page_file'])

    # Tier 2: Section-level components (most important for structure)
    tier2 = []
    # Tier 3: Page components
    tier3 = []
    # Tier 4: UI/marketing components
    tier4 = []
    # Tier 5: CSS and config
    tier5 = list(info.get('css_files', []))

    # Walk source directories looking for components
    for search_root in [os.path.join(app_dir, 'src'), os.path.join(app_dir, 'app'), app_dir]:
        if not os.path.isdir(search_root):
            continue
        for root, dirs, files in os.walk(search_root):
            # Skip junk
            dirs[:] = [d for d in dirs if d not in ('node_modules', '.next', '__MACOSX', '.git', '__tests__')]
            for f in files:
                if not f.endswith(('.tsx', '.jsx', '.ts', '.js')):
                    continue
                full = os.path.join(root, f)
                # Skip test files, config files, API routes
                if '.test.' in f or '.spec.' in f:
                    continue
                if '/api/' in full:
                    continue
                # Skip files already in tier 1
                if full in tier1:
                    continue

                rel = os.path.relpath(root, app_dir)
                basename = f.lower()

                if 'section' in basename or 'section' in rel.lower():
                    tier2.append(full)
                elif 'page' in basename and 'page' not in rel.lower().split('app')[-1:]:
                    tier3.append(full)
                elif any(k in rel.lower() for k in ('components', 'marketing')):
                    tier4.append(full)

    # Assemble by priority, tracking budget
    used = 0
    for tier_files in [tier1, tier2, tier3, tier4, tier5]:
        for fpath in tier_files:
            if not os.path.isfile(fpath):
                continue
            try:
                with open(fpath, 'r', errors='replace') as fh:
                    content = fh.read()
            except OSError:
                continue

            rel_path = os.path.relpath(fpath, app_dir)
            # Skip if already collected (dedup across tiers)
            if rel_path in sources:
                continue

            # Truncate individual large files
            if len(content) > 8000:
                content = content[:8000] + '\n// ... [truncated]'

            if used + len(content) > budget:
                remaining = budget - used
                if remaining > 500:
                    content = content[:remaining] + '\n// ... [truncated - budget]'
                    sources[rel_path] = content
                    used += len(content)
                break
            sources[rel_path] = content
            used += len(content)

    logging.info(f"Collected {len(sources)} source files ({used} chars) from Next.js app")
    return sources


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
    If path is a Next.js app: convert React components to Hugo.
    If path is an HTML file or raw HTML dir: convert it.
    """
    from .theme_finder import find_hugo_theme, find_nextjs_app, find_raw_html_files

    info = find_hugo_theme(path)
    if info:
        return hugoify_dir(info['theme_dir'])

    nextjs_info = find_nextjs_app(path)
    if nextjs_info:
        layouts = hugoify_nextjs(nextjs_info)
        return f"Converted Next.js app to {len(layouts)} layout files: {list(layouts.keys())}"

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
    """Extract JSON from AI response, even if surrounded by prose or markdown fences."""
    # Strip markdown fences if present
    stripped = re.sub(r'```(?:json)?\s*', '', response)
    stripped = re.sub(r'```\s*$', '', stripped.strip())

    # Try the full stripped response as JSON first
    try:
        result = json.loads(stripped)
        if isinstance(result, dict):
            logging.info(f"Parsed {len(result)} layout files from AI response")
            return result
    except json.JSONDecodeError:
        pass

    # Try to find JSON block (outermost braces)
    match = re.search(r'\{.*\}', stripped, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group(0))
            if isinstance(result, dict):
                logging.info(f"Parsed {len(result)} layout files from AI response (extracted)")
                return result
        except json.JSONDecodeError:
            pass

        # AI sometimes uses backtick-delimited values instead of JSON strings.
        # Parse with a regex-based key-value extractor.
        backtick_result = _parse_backtick_json(match.group(0))
        if backtick_result:
            logging.info(f"Parsed {len(backtick_result)} layout files from backtick-delimited response")
            return backtick_result

    # Fallback: return a minimal layout
    logging.warning("Could not parse AI response as JSON, using fallback layouts")
    logging.debug(f"AI response was: {response[:500]!r}")
    return {
        "_default/baseof.html": _fallback_baseof(),
        "partials/header.html": "<header><!-- header --></header>",
        "partials/footer.html": "<footer>{{ .Site.Params.copyright }}</footer>",
        "index.html": '{{ define "main" }}<main>{{ .Content }}</main>{{ end }}',
    }


def _parse_backtick_json(text: str) -> dict | None:
    """
    Parse a JSON-like object where values are backtick-delimited template literals
    instead of proper JSON strings. This happens when the AI uses JS template syntax.
    e.g.: { "key": `<html>...</html>` }
    """
    result = {}
    # Match "key": `value` pairs where value can span multiple lines
    pattern = re.compile(r'"([^"]+)"\s*:\s*`(.*?)`(?:\s*[,}])', re.DOTALL)
    for m in pattern.finditer(text):
        key = m.group(1)
        value = m.group(2).strip()
        result[key] = value

    return result if result else None


def _fallback_layouts() -> dict:
    """Minimal fallback when source collection fails."""
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
