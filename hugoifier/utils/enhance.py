"""
AI-powered post-conversion enhancements for Hugo sites.

Individual commands:
  hugoifier generate <path> --prompt "..." or --from-file example.md
  hugoifier seo <path>
  hugoifier alt-text <path>

Meta command:
  hugoifier enhance <path>  (runs seo + alt-text)
"""

import json
import logging
import os
import re

import yaml

from ..config import call_ai

SYSTEM = "You are an expert Hugo site developer, SEO specialist, and content strategist."


# ---------------------------------------------------------------------------
# Meta command
# ---------------------------------------------------------------------------

def enhance(site_dir: str) -> str:
    """Run all non-destructive enhancements (SEO + alt-text)."""
    context = _read_site_context(site_dir)
    results = []
    results.append(seo(site_dir, context=context))
    results.append(alt_text(site_dir, context=context))
    return "\n".join(results)


# ---------------------------------------------------------------------------
# Content generation
# ---------------------------------------------------------------------------

def generate(
    site_dir: str,
    prompt: str = None,
    from_file: str = None,
) -> str:
    """Generate new Hugo content pages using AI."""
    context = _read_site_context(site_dir)

    # Build the instruction
    if from_file:
        with open(from_file, 'r', errors='replace') as f:
            example = f.read()
        instruction = (
            f"Use the following file as a style and structure example. "
            f"Generate 2-3 new content pages that follow the same format and tone.\n\n"
            f"Example file:\n{example[:5000]}"
        )
    elif prompt:
        instruction = prompt
    else:
        instruction = (
            "Generate 2-3 new content pages that fit this site's theme and purpose. "
            "Create pages for sections that exist in the navigation but are missing content."
        )

    ai_prompt = f"""You are generating content for a Hugo website.

Site title: {context['title']}
Site description: {context['description']}
Existing content sections: {', '.join(context['content_sections']) or 'none'}

Sample existing content:
{context['sample_content'][:3000]}

Instruction: {instruction}

Return a JSON object mapping relative file paths (under content/) to full markdown files.
Each file MUST start with YAML frontmatter (--- delimiters) including: title, date, description.
IMPORTANT: Always quote title and description values in frontmatter with double quotes to handle colons and special characters.
Example: {{"blog/my-first-post.md": "---\\ntitle: \\"My First Post\\"\\ndate: 2026-03-17\\ndescription: \\"A great post about things\\"\\n---\\n\\nContent here..."}}

Return ONLY valid JSON, no explanation."""

    response = call_ai(ai_prompt, SYSTEM, max_tokens=8192)
    files = _parse_ai_json(response)

    if not files:
        return "Could not generate content — AI response was not valid JSON"

    content_dir = os.path.join(site_dir, 'content')
    written = []
    for rel_path, content in files.items():
        content = _fix_frontmatter_quoting(content)
        dest = os.path.join(content_dir, rel_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w') as f:
            f.write(content)
        written.append(rel_path)
        logging.info(f"Generated {rel_path}")

    return f"Generated {len(written)} content pages: {written}"


# ---------------------------------------------------------------------------
# SEO optimization
# ---------------------------------------------------------------------------

def seo(site_dir: str, context: dict = None) -> str:
    """Add missing meta descriptions to content + OG tags to baseof."""
    if context is None:
        context = _read_site_context(site_dir)

    results = []
    results.append(_seo_descriptions(site_dir, context))
    results.append(_seo_og_tags(site_dir))
    return "\n".join(r for r in results if r)


def _seo_descriptions(site_dir: str, context: dict) -> str:
    """Add missing meta descriptions to content files."""
    content_dir = os.path.join(site_dir, 'content')
    if not os.path.isdir(content_dir):
        return "No content/ directory found"

    # Find files missing descriptions
    missing = []
    for root, dirs, files in os.walk(content_dir):
        for f in files:
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            fm = _parse_frontmatter(path)
            if not fm.get('description'):
                title = fm.get('title', f)
                body = _read_body(path)
                missing.append((path, title, body[:500]))

    if not missing:
        return "All content files already have descriptions"

    # Batch AI call — up to 10 at a time
    updated = 0
    for batch in _chunks(missing, 10):
        items = "\n".join(
            f'- "{title}": {excerpt[:200]}' for _, title, excerpt in batch
        )
        ai_prompt = f"""Generate concise SEO meta descriptions (1-2 sentences, under 160 chars) for these Hugo content pages.

Site: {context['title']}

Pages:
{items}

Return a JSON object mapping the exact title to the description.
Return ONLY valid JSON."""

        try:
            response = call_ai(ai_prompt, SYSTEM, max_tokens=2048)
            descriptions = _parse_ai_json(response)
            if not descriptions:
                continue

            for path, title, _ in batch:
                desc = descriptions.get(title)
                if desc:
                    _update_frontmatter(path, {'description': desc})
                    updated += 1
        except Exception as e:
            logging.warning(f"SEO description batch failed: {e}")

    return f"Added meta descriptions to {updated} content files"


def _seo_og_tags(site_dir: str) -> str:
    """Add Open Graph tags to baseof.html if missing."""
    baseof = _find_baseof(site_dir)
    if not baseof:
        return "No baseof.html found"

    with open(baseof, 'r') as f:
        html = f.read()

    if 'og:title' in html:
        return "OG tags already present in baseof.html"

    og_block = '''
  <!-- Open Graph -->
  <meta property="og:title" content="{{ .Title }}" />
  <meta property="og:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}" />
  <meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}" />
  <meta property="og:url" content="{{ .Permalink }}" />
  {{ with .Params.image }}<meta property="og:image" content="{{ . | absURL }}" />{{ end }}'''

    # Insert before </head>
    html = html.replace('</head>', og_block + '\n</head>')
    with open(baseof, 'w') as f:
        f.write(html)

    return f"Added OG tags to {os.path.relpath(baseof, site_dir)}"


# ---------------------------------------------------------------------------
# Image alt text
# ---------------------------------------------------------------------------

def alt_text(site_dir: str, context: dict = None) -> str:
    """Generate alt text for images missing it in templates."""
    if context is None:
        context = _read_site_context(site_dir)

    # Find all template files
    templates = []
    for search_dir in [
        os.path.join(site_dir, 'layouts'),
        *_glob_dirs(site_dir, 'themes/*/layouts'),
    ]:
        if not os.path.isdir(search_dir):
            continue
        for root, dirs, files in os.walk(search_dir):
            for f in files:
                if f.endswith('.html'):
                    templates.append(os.path.join(root, f))

    # Find images with empty or missing alt text
    missing = []
    img_pattern = re.compile(r'<img\b([^>]*)/?>', re.DOTALL)
    alt_pattern = re.compile(r'alt\s*=\s*["\']([^"\']*)["\']')

    for tpl_path in templates:
        with open(tpl_path, 'r', errors='replace') as f:
            content = f.read()
        for m in img_pattern.finditer(content):
            attrs = m.group(1)
            alt_match = alt_pattern.search(attrs)
            # Skip if has meaningful alt text (including Hugo template vars)
            if alt_match and alt_match.group(1).strip():
                continue
            # Extract src for context
            src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', attrs)
            src = src_match.group(1) if src_match else 'unknown'
            # Get surrounding context
            start = max(0, m.start() - 100)
            end = min(len(content), m.end() + 100)
            ctx = content[start:end]
            missing.append((tpl_path, m.group(0), src, ctx))

    if not missing:
        return "All images already have alt text"

    # Batch AI call
    items = "\n".join(
        f'- src="{src}" context: {ctx[:150]}' for _, _, src, ctx in missing[:20]
    )
    ai_prompt = f"""Generate descriptive alt text for these images on a Hugo site called "{context['title']}".

Images:
{items}

Return a JSON object mapping the src value to a short descriptive alt text string.
For images with Hugo template src attributes, use a Hugo template for the alt text too.
Return ONLY valid JSON."""

    try:
        response = call_ai(ai_prompt, SYSTEM, max_tokens=2048)
        alts = _parse_ai_json(response)
    except Exception as e:
        return f"Alt text generation failed: {e}"

    if not alts:
        return "Could not parse alt text suggestions from AI"

    updated_files = set()
    for tpl_path, img_tag, src, _ in missing:
        suggested = alts.get(src)
        if not suggested:
            continue
        with open(tpl_path, 'r') as f:
            content = f.read()

        safe_alt = suggested.replace('"', '&quot;')
        if 'alt=' in img_tag:
            new_tag = re.sub(r'alt\s*=\s*["\'][^"\']*["\']', f'alt="{safe_alt}"', img_tag)
        else:
            new_tag = img_tag.replace('<img ', f'<img alt="{safe_alt}" ', 1)

        content = content.replace(img_tag, new_tag, 1)
        with open(tpl_path, 'w') as f:
            f.write(content)
        updated_files.add(tpl_path)

    return f"Added alt text to {len(updated_files)} template files"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_site_context(site_dir: str) -> dict:
    """Read basic site info for AI context."""
    context = {
        'title': 'My Hugo Site',
        'description': '',
        'content_sections': [],
        'sample_content': '',
    }

    # Read hugo.toml
    for config_name in ('hugo.toml', 'config.toml'):
        config_path = os.path.join(site_dir, config_name)
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_text = f.read()
            title_match = re.search(r'^title\s*=\s*"([^"]*)"', config_text, re.MULTILINE)
            if title_match:
                context['title'] = title_match.group(1)
            desc_match = re.search(r'description\s*=\s*"([^"]*)"', config_text, re.MULTILINE)
            if desc_match:
                context['description'] = desc_match.group(1)
            break

    # Read content sections
    content_dir = os.path.join(site_dir, 'content')
    if os.path.isdir(content_dir):
        context['content_sections'] = [
            d for d in os.listdir(content_dir)
            if os.path.isdir(os.path.join(content_dir, d))
        ]

        # Sample content
        samples = []
        for root, dirs, files in os.walk(content_dir):
            for f in files:
                if f.endswith('.md') and len(samples) < 3:
                    path = os.path.join(root, f)
                    with open(path, 'r', errors='replace') as fh:
                        samples.append(fh.read()[:1000])
        context['sample_content'] = "\n---\n".join(samples)

    return context


def _parse_frontmatter(md_path: str) -> dict:
    """Parse YAML frontmatter from a .md file."""
    try:
        with open(md_path, 'r', errors='replace') as f:
            content = f.read()
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1)) or {}
    except Exception:
        pass
    return {}


def _read_body(md_path: str) -> str:
    """Read the body content (after frontmatter) of a .md file."""
    try:
        with open(md_path, 'r', errors='replace') as f:
            content = f.read()
        match = re.match(r'^---\n.*?\n---\n?(.*)', content, re.DOTALL)
        return match.group(1).strip() if match else content
    except Exception:
        return ""


def _update_frontmatter(md_path: str, updates: dict):
    """Add/update keys in a markdown file's YAML frontmatter."""
    with open(md_path, 'r', errors='replace') as f:
        content = f.read()

    match = re.match(r'^(---\n)(.*?)(\n---\n?)(.*)', content, re.DOTALL)
    if not match:
        return

    fm_text = match.group(2)
    body = match.group(4)

    fm = yaml.safe_load(fm_text) or {}
    fm.update(updates)

    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    with open(md_path, 'w') as f:
        f.write(f"---\n{new_fm}---\n{body}")


def _find_baseof(site_dir: str) -> str | None:
    """Find baseof.html in the site."""
    candidates = [
        os.path.join(site_dir, 'layouts', '_default', 'baseof.html'),
    ]
    # Also check themes
    themes_dir = os.path.join(site_dir, 'themes')
    if os.path.isdir(themes_dir):
        for theme in os.listdir(themes_dir):
            candidates.append(
                os.path.join(themes_dir, theme, 'layouts', '_default', 'baseof.html')
            )
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def _glob_dirs(base: str, pattern: str) -> list:
    """Simple glob for directory patterns like 'themes/*/layouts'."""
    parts = pattern.split('*')
    if len(parts) != 2:
        return []
    prefix = os.path.join(base, parts[0])
    suffix = parts[1]
    if not os.path.isdir(prefix):
        return []
    return [
        os.path.join(prefix, d, suffix.lstrip('/'))
        for d in os.listdir(prefix)
        if os.path.isdir(os.path.join(prefix, d))
    ]


def _parse_ai_json(response: str) -> dict | None:
    """Extract JSON dict from AI response, stripping markdown fences."""
    stripped = re.sub(r'```(?:json)?\s*', '', response)
    stripped = re.sub(r'```\s*$', '', stripped.strip())
    try:
        result = json.loads(stripped)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass
    match = re.search(r'\{.*\}', stripped, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group(0))
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass
    return None


def _fix_frontmatter_quoting(content: str) -> str:
    """Quote YAML frontmatter values that contain colons (Hugo/YAML safety)."""
    match = re.match(r'^(---\n)(.*?)(\n---)', content, re.DOTALL)
    if not match:
        return content
    fm_lines = match.group(2).split('\n')
    fixed = []
    for line in fm_lines:
        kv = re.match(r'^(\w+):\s+(.+)$', line)
        if kv:
            key, val = kv.group(1), kv.group(2)
            # Quote if value contains a colon and isn't already quoted
            if ':' in val and not (val.startswith('"') or val.startswith("'")):
                val = f'"{val}"'
            fixed.append(f'{key}: {val}')
        else:
            fixed.append(line)
    return f"---\n{chr(10).join(fixed)}\n---{content[match.end():]}"


def _chunks(lst, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
