"""
Analyzes a Hugo theme or raw HTML theme and reports structure + recommendations.
"""

import logging
import os

from config import call_ai
from utils.theme_finder import find_hugo_theme, find_raw_html_files

SYSTEM = "You are an expert Hugo theme developer analyzing themes for conversion."


def analyze(path: str) -> str:
    logging.info(f"Analyzing {path} ...")

    info = find_hugo_theme(path)

    if info:
        return _analyze_hugo_theme(info)
    else:
        return _analyze_raw_html(path)


def _analyze_hugo_theme(info: dict) -> str:
    theme_dir = info['theme_dir']
    theme_name = info['theme_name']
    example_site = info['example_site']

    # Collect layout files
    layouts = []
    for root, dirs, files in os.walk(os.path.join(theme_dir, 'layouts')):
        for f in files:
            if f.endswith('.html'):
                rel = os.path.relpath(os.path.join(root, f), theme_dir)
                layouts.append(rel)

    # Collect content types from exampleSite
    content_types = []
    if example_site:
        content_dir = os.path.join(example_site, 'content')
        if os.path.isdir(content_dir):
            content_types = [d for d in os.listdir(content_dir) if os.path.isdir(os.path.join(content_dir, d))]

    report = [
        f"Theme: {theme_name}",
        f"Theme dir: {theme_dir}",
        f"Layouts ({len(layouts)}):",
        *[f"  {l}" for l in sorted(layouts)],
        f"Content types: {content_types}",
        f"ExampleSite: {example_site or 'none'}",
        "",
        "Status: Already a Hugo theme. Use 'complete' to assemble a working site.",
    ]
    return "\n".join(report)


def _analyze_raw_html(path: str) -> str:
    html_files = find_raw_html_files(path)
    if not html_files:
        return f"No HTML files found at {path}"

    # Read main HTML file for AI analysis
    main = next((f for f in html_files if os.path.basename(f).lower() == 'index.html'), html_files[0])
    with open(main, 'r', errors='replace') as f:
        html = f.read()[:20000]

    prompt = f"""Analyze this HTML theme file and provide:
1. Identified reusable components (header, footer, nav, sidebar, etc.)
2. Recommended Hugo template tags for dynamic content
3. Suggested partial splits
4. Content sections that should be data/ YAML files for Decap CMS

HTML:
{html}"""

    try:
        return call_ai(prompt, SYSTEM)
    except Exception as e:
        logging.error(f"AI analysis failed: {e}")
        return f"HTML theme with {len(html_files)} files. AI analysis failed: {e}"
