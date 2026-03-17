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

    Uses direct HTML extraction (no AI) to preserve content exactly as-is.
    Splits the HTML into Hugo's baseof.html (head/shell) and index.html (body content).

    Returns dict mapping relative layout paths to their content.
    """
    logging.info(f"Hugoifying {html_path} ...")

    with open(html_path, 'r', errors='replace') as f:
        html = f.read()

    logging.info(f"Read {len(html)} chars from {html_path}")

    # Extract <head> content (CSS links, meta, fonts, etc.)
    head_extras = _extract_head_content(html)

    # Extract and rewrite CSS/JS paths to be relative to Hugo static/
    css_links = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*/?>',
                           html, re.DOTALL | re.IGNORECASE)
    js_links = re.findall(r'<script[^>]+src=["\'][^"\']+["\'][^>]*>.*?</script>',
                          html, re.DOTALL)

    # Extract <body> content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    body_content = body_match.group(1).strip() if body_match else html

    # Extract body attributes (class, style, etc.)
    body_attrs_match = re.search(r'<body([^>]*)>', html)
    body_attrs = body_attrs_match.group(1).strip() if body_attrs_match else ''

    # Build baseof.html preserving the original <head> structure
    head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL)
    if head_match:
        head_content = head_match.group(1).strip()
        # Replace hardcoded <title> with Hugo template
        head_content = re.sub(
            r'<title>[^<]*</title>',
            '<title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} | {{ .Site.Title }}{{ end }}</title>',
            head_content
        )
        baseof = f'''<!DOCTYPE html>
<html lang="{{{{ with .Site.LanguageCode }}}}{{{{ . }}}}{{{{ else }}}}en{{{{ end }}}}">
<head>
{head_content}
</head>
<body{" " + body_attrs if body_attrs else ""}>
  {{{{- block "main" . }}}}{{{{- end }}}}
</body>
</html>'''
    else:
        baseof = _fallback_baseof()

    index_html = f'{{{{ define "main" }}}}\n{body_content}\n{{{{ end }}}}'

    layouts = {
        "_default/baseof.html": baseof,
        "index.html": index_html,
    }

    logging.info(f"Extracted {len(layouts)} layout files directly from HTML (no AI)")
    return layouts


def hugoify_nextjs(info: dict, dev_url: str = None) -> dict:
    """
    Convert a Next.js app to a set of Hugo layout files.

    If dev_url is provided (or auto-detected), captures the actual rendered HTML
    from the running Next.js dev server for pixel-perfect conversion.
    Otherwise falls back to AI-powered TSX source conversion.

    Args:
        info: dict from find_nextjs_app() with app_dir, router_type, etc.
        dev_url: URL of a running Next.js dev server (e.g. http://localhost:3000)

    Returns:
        dict mapping relative layout paths to their content, plus
        a '_captured_assets' key with any downloaded CSS/JS files.
    """
    app_dir = info['app_dir']
    logging.info(f"Hugoifying Next.js app at {app_dir} ...")

    # Try to auto-detect a running dev server
    if not dev_url:
        dev_url = _detect_nextjs_server(info)

    if dev_url:
        return _capture_rendered_html(dev_url, info)

    # Fallback: AI-powered source conversion (less faithful)
    return _ai_convert_nextjs_sources(info)


def _detect_nextjs_server(info: dict) -> str | None:
    """Check if a Next.js dev server is running on common ports."""
    import urllib.request
    for port in [3000, 3001, 3002]:
        url = f"http://localhost:{port}"
        try:
            req = urllib.request.Request(url, method='HEAD')
            resp = urllib.request.urlopen(req, timeout=2)
            if resp.status == 200:
                logging.info(f"Detected running Next.js server at {url}")
                return url
        except Exception:
            continue
    return None


def _capture_rendered_html(dev_url: str, info: dict) -> dict:
    """
    Capture the actual server-rendered HTML from a running Next.js app
    and convert it into Hugo layout files. This gives pixel-perfect results.
    """
    import urllib.request
    import urllib.parse

    logging.info(f"Capturing rendered HTML from {dev_url} ...")

    # Fetch the full rendered page
    resp = urllib.request.urlopen(dev_url)
    html = resp.read().decode('utf-8')
    logging.info(f"Captured {len(html)} chars of rendered HTML")

    # Download compiled CSS
    css_urls = re.findall(r'href="(/_next/static/[^"]+\.css)"', html)
    captured_css = {}
    for css_path in css_urls:
        css_url = f"{dev_url}{css_path}"
        try:
            css_resp = urllib.request.urlopen(css_url)
            css_content = css_resp.read().decode('utf-8')
            captured_css['compiled.css'] = css_content
            logging.info(f"Captured CSS: {len(css_content)} chars")
            break  # Usually just one CSS file
        except Exception as e:
            logging.warning(f"Failed to fetch CSS {css_url}: {e}")

    # Strip Next.js scripts, dev tooling, and React hydration markers
    body_html = _extract_and_clean_body(html)

    # Extract <head> content we want to keep (fonts, meta, etc.)
    head_extras = _extract_head_content(html)

    # Build Hugo layouts
    baseof = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{{{ if .IsHome }}}}{{{{ .Site.Title }}}}{{{{ else }}}}{{{{ .Title }}}} | {{{{ .Site.Title }}}}{{{{ end }}}}</title>
{head_extras}
  <link rel="stylesheet" href="/css/compiled.css">
  <link rel="stylesheet" href="/css/globals.css">
</head>
<body class="antialiased">
  {{{{- block "main" . }}}}{{{{- end }}}}
</body>
</html>'''

    index_html = f'{{{{ define "main" }}}}\n{body_html}\n{{{{ end }}}}'

    layouts = {
        "_default/baseof.html": baseof,
        "index.html": index_html,
    }

    # Attach captured CSS as metadata for the pipeline to handle
    if captured_css:
        layouts['_captured_css'] = captured_css

    return layouts


def _extract_and_clean_body(html: str) -> str:
    """Extract <body> content and strip Next.js scripts/dev tooling."""
    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not body_match:
        return html

    body = body_match.group(1)

    # Strip all <script> tags (Next.js runtime, React hydration, HMR, etc.)
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script\b[^>]*/?>', '', body)

    # Strip Next.js dev overlay and error boundary elements
    body = re.sub(r'<next-route-announcer[^>]*>.*?</next-route-announcer>', '', body, flags=re.DOTALL)
    body = re.sub(r'<nextjs-portal[^>]*>.*?</nextjs-portal>', '', body, flags=re.DOTALL)

    # Strip data-reactroot, data-nextjs, and other React/Next.js attributes
    body = re.sub(r'\s*data-(?:reactroot|nextjs[^=]*|rsc[^=]*)(?:="[^"]*")?', '', body)

    # Fix FadeIn components: they render with opacity:0 and translateY(32px)
    # because the IntersectionObserver JS isn't running. Force them visible.
    body = re.sub(r'opacity:\s*0', 'opacity:1', body)
    body = re.sub(r'translateY\(32px\)', 'translateY(0px)', body)

    # Replace /_next/static/ asset references with /static/ for Hugo
    body = re.sub(r'/_next/static/media/([^"]+)', r'/\1', body)

    return body.strip()


def _extract_head_content(html: str) -> str:
    """Extract useful <head> elements (fonts, preloads) from rendered HTML."""
    head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL)
    if not head_match:
        return ""

    head = head_match.group(1)
    lines = []

    # Keep font preload/stylesheet links
    for match in re.finditer(r'<link[^>]+(?:fonts\.googleapis|fonts\.gstatic|preload[^>]+font)[^>]*/?>',
                              head, re.DOTALL):
        lines.append(f"  {match.group(0)}")

    # Keep image preloads
    for match in re.finditer(r'<link[^>]+rel="preload"[^>]+as="image"[^>]*/?>',
                              head, re.DOTALL):
        tag = match.group(0)
        # Fix /_next paths to local paths
        tag = re.sub(r'/_next/static/media/', '/', tag)
        lines.append(f"  {tag}")

    return "\n".join(lines)


def _ai_convert_nextjs_sources(info: dict) -> dict:
    """
    Fallback: AI-powered conversion from TSX source files.
    Used when no running dev server is available.
    """
    sources = _collect_nextjs_sources(info)
    if not sources:
        logging.warning("No source files collected from Next.js app")
        return _fallback_layouts()

    layouts = {}

    # Identify component vs structural files
    component_sources = {}
    layout_sources = {}
    for rel_path, content in sources.items():
        if rel_path.endswith('.css'):
            continue
        elif 'layout.' in rel_path or 'page.' in rel_path:
            layout_sources[rel_path] = content
        else:
            component_sources[rel_path] = content

    # Convert each component individually
    for rel_path, content in component_sources.items():
        basename = os.path.splitext(os.path.basename(rel_path))[0]
        partial_name = f"partials/{basename}.html"
        logging.info(f"  Converting {rel_path} → {partial_name}")
        html = _convert_single_component(basename, content)
        if html:
            layouts[partial_name] = html

    # Build baseof and index
    partial_names = [os.path.splitext(os.path.basename(k))[0] for k in layouts.keys()]
    baseof, index_html = _convert_layout_and_page(layout_sources, component_sources, partial_names)
    layouts["_default/baseof.html"] = baseof
    layouts["index.html"] = index_html

    logging.info(f"Generated {len(layouts)} layout files via AI conversion")
    return layouts


_COMPONENT_PROMPT = """Convert this React/Next.js component to static Hugo-compatible HTML.

CRITICAL RULES:
- Output ONLY the raw HTML. No markdown fences, no explanation, no JSON wrapping.
- Convert ALL JSX `className` to HTML `class`
- Unroll ALL `.map()` calls into full static HTML — every single item
- Preserve EVERY Tailwind CSS class and inline style EXACTLY
- Preserve ALL text content — do NOT summarize or shorten
- Preserve ALL SVG content inline
- Strip React hooks and event handlers, keep static HTML structure

Component name: {name}

Source code:
{source}"""


def _convert_single_component(name: str, source: str) -> str | None:
    """Convert a single React component to Hugo-compatible HTML via AI."""
    prompt = _COMPONENT_PROMPT.format(name=name, source=source)
    try:
        response = call_ai(prompt, NEXTJS_SYSTEM, max_tokens=16384)
        html = re.sub(r'^```(?:html)?\s*', '', response.strip())
        html = re.sub(r'```\s*$', '', html.strip())
        return html
    except Exception as e:
        logging.warning(f"Failed to convert component {name}: {e}")
        return None


def _convert_layout_and_page(layout_sources, component_sources, partial_names):
    """Build baseof.html and index.html from layout files and partial list."""
    partial_includes = "\n".join(
        f'  {{{{ partial "{name}.html" . }}}}' for name in partial_names
    )
    baseof = _fallback_baseof()
    index_html = f'{{% define "main" %}}\n<div class="bg-[#121517] flex flex-col w-full">\n{partial_includes}\n</div>\n{{% end %}}'
    return baseof, index_html


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
