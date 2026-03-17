"""
Locates the actual Hugo theme and exampleSite within the messy zip-extracted structure.
Also detects Next.js applications for conversion.
Themes in themes/ are structured as: {name}/{name}/themes/{theme-name}/
"""

import json
import logging
import os


def find_hugo_theme(input_path):
    """
    Given a path like themes/revolve-hugo or the inner extracted dir,
    find the Hugo theme directory (has layouts/), the exampleSite, and the theme name.

    Returns dict with:
        theme_dir: path to the Hugo theme (has layouts/, archetypes/, etc.)
        example_site: path to exampleSite dir (may be None)
        theme_name: name of the theme (used in hugo.toml)
        is_hugo_theme: True if input is already a Hugo theme
    """
    input_path = os.path.abspath(input_path)

    # Walk up to find the theme dir containing layouts/
    candidates = []
    for root, dirs, files in os.walk(input_path):
        # Skip __MACOSX junk
        if '__MACOSX' in root:
            continue
        if 'layouts' in dirs and '_default' in os.listdir(os.path.join(root, 'layouts')):
            candidates.append(root)

    if not candidates:
        return None

    # Pick the deepest match (most likely the actual theme dir)
    theme_dir = max(candidates, key=lambda p: p.count(os.sep))
    if len(candidates) > 1:
        logging.warning(
            f"Multiple Hugo theme candidates found; using {theme_dir!r}. "
            f"Others: {[c for c in candidates if c != theme_dir]}"
        )

    # Detect exampleSite
    example_site = None
    for candidate in [
        os.path.join(theme_dir, 'exampleSite'),
        os.path.join(os.path.dirname(theme_dir), 'exampleSite'),
    ]:
        if os.path.isdir(candidate):
            example_site = candidate
            break

    theme_name = os.path.basename(theme_dir)

    return {
        'theme_dir': theme_dir,
        'example_site': example_site,
        'theme_name': theme_name,
        'is_hugo_theme': True,
    }


def find_nextjs_app(input_path):
    """
    Detect a Next.js application in the given path.

    Walks up to 2 levels deep to find package.json with "next" in dependencies,
    similar to how find_hugo_theme handles zip-extracted double-folder structure.

    Returns dict with:
        app_dir: root of the Next.js project (where package.json lives)
        app_name: name from package.json or directory name
        router_type: 'app' or 'pages'
        has_src_dir: whether components live under src/
        layout_file: path to app/layout.tsx/jsx (App Router) or None
        page_file: path to app/page.tsx/jsx or pages/index.tsx/jsx
        css_files: list of global CSS files found
        is_nextjs_app: True
    """
    input_path = os.path.abspath(input_path)

    # Look for package.json at root or one level deep (zip-extracted pattern)
    candidates = []
    for pkg in _find_file_up_to_depth(input_path, 'package.json', max_depth=2):
        try:
            with open(pkg, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
        if 'next' in deps:
            candidates.append((os.path.dirname(pkg), data))

    if not candidates:
        return None

    # Pick the deepest match (most specific, like find_hugo_theme)
    app_dir, pkg_data = max(candidates, key=lambda x: x[0].count(os.sep))
    app_name = pkg_data.get('name', os.path.basename(app_dir))

    # Detect router type
    app_router_dir = os.path.join(app_dir, 'app')
    pages_dir = os.path.join(app_dir, 'pages')
    if os.path.isdir(app_router_dir):
        router_type = 'app'
    elif os.path.isdir(pages_dir):
        router_type = 'pages'
    else:
        return None  # Has next dep but no recognizable router

    # Detect src/ directory
    src_dir = os.path.join(app_dir, 'src')
    has_src_dir = os.path.isdir(src_dir)

    # Find layout and page files
    layout_file = _find_tsx_or_jsx(app_dir, 'app', 'layout')
    if router_type == 'app':
        page_file = _find_tsx_or_jsx(app_dir, 'app', 'page')
    else:
        page_file = _find_tsx_or_jsx(app_dir, 'pages', 'index')

    # Find CSS files
    css_files = []
    for search_dir in [app_router_dir, os.path.join(app_dir, 'src'), app_dir]:
        if not os.path.isdir(search_dir):
            continue
        for f in os.listdir(search_dir):
            if f.endswith('.css'):
                css_files.append(os.path.join(search_dir, f))

    return {
        'app_dir': app_dir,
        'app_name': app_name,
        'router_type': router_type,
        'has_src_dir': has_src_dir,
        'layout_file': layout_file,
        'page_file': page_file,
        'css_files': css_files,
        'is_nextjs_app': True,
    }


def _find_file_up_to_depth(root, filename, max_depth=2):
    """Yield paths to `filename` found up to max_depth levels under root."""
    for depth_root, dirs, files in os.walk(root):
        rel = os.path.relpath(depth_root, root)
        depth = 0 if rel == '.' else rel.count(os.sep) + 1
        if depth > max_depth:
            dirs.clear()
            continue
        if '__MACOSX' in depth_root or 'node_modules' in depth_root:
            dirs.clear()
            continue
        if filename in files:
            yield os.path.join(depth_root, filename)


def _find_tsx_or_jsx(base, subdir, name):
    """Find {name}.tsx or {name}.jsx in base/subdir/."""
    d = os.path.join(base, subdir)
    for ext in ('.tsx', '.jsx', '.ts', '.js'):
        p = os.path.join(d, name + ext)
        if os.path.isfile(p):
            return p
    return None


def find_raw_html_files(input_path):
    """Find HTML files in a raw HTML theme (not a Hugo theme)."""
    html_files = []
    for root, dirs, files in os.walk(input_path):
        if '__MACOSX' in root:
            continue
        for f in files:
            if f.endswith('.html') and 'exampleSite' not in root:
                html_files.append(os.path.join(root, f))
    return html_files
