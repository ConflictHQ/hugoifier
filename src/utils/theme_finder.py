"""
Locates the actual Hugo theme and exampleSite within the messy zip-extracted structure.
Themes in themes/ are structured as: {name}/{name}/themes/{theme-name}/
"""

import logging
import os
import glob as glob_module


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
