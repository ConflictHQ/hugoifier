"""
Patches common Hugo deprecations in theme layout files so they work with Hugo >= v0.128.

Call patch_theme(theme_dir) after copying theme files to the output directory.
"""

import logging
import os
import re

# Map of (pattern, replacement) for deprecated Hugo template variables/functions
TEMPLATE_PATCHES = [
    # .Site.DisqusShortname → .Site.Config.Services.Disqus.Shortname
    (r'\.Site\.DisqusShortname', '.Site.Config.Services.Disqus.Shortname'),
    # .Site.GoogleAnalytics → .Site.Config.Services.GoogleAnalytics.ID
    (r'\.Site\.GoogleAnalytics\b', '.Site.Config.Services.GoogleAnalytics.ID'),
    # absLangURL → absLangURL still works but absURL is preferred for simple cases
    # safeHTMLAttr is fine, no change needed
]

# Config key patches: (old_pattern, replacement)
CONFIG_PATCHES = [
    # paginate → [pagination] pagerSize
    (r'^paginate\s*=\s*(\d+)$', r'[pagination]\n  pagerSize = \1'),
    # googleAnalytics = "UA-xxx" → [services.googleAnalytics] id = "UA-xxx"
    (r'^googleAnalytics\s*=\s*"([^"]+)"', r'[services.googleAnalytics]\n  id = "\1"'),
    # disqusShortname = "xxx" → [services.disqus] shortname = "xxx"
    (r'^disqusShortname\s*=\s*"([^"]+)"', r'[services.disqus]\n  shortname = "\1"'),
]


def patch_theme(theme_dir: str):
    """Patch deprecated Hugo APIs in all layout files under theme_dir/layouts/."""
    layouts_dir = os.path.join(theme_dir, 'layouts')
    if not os.path.isdir(layouts_dir):
        return

    patched = 0
    for root, dirs, files in os.walk(layouts_dir):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            path = os.path.join(root, fname)
            with open(path, 'r', errors='replace') as f:
                content = f.read()

            new_content = content
            for pattern, replacement in TEMPLATE_PATCHES:
                new_content = re.sub(pattern, replacement, new_content)

            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                patched += 1

    if patched:
        logging.info(f"Patched {patched} template file(s) in {theme_dir}")


def patch_config(config_path: str):
    """Patch deprecated keys in a hugo.toml / config.toml file."""
    with open(config_path, 'r') as f:
        content = f.read()

    new_content = content
    for pattern, replacement in CONFIG_PATCHES:
        new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)

    if new_content != content:
        with open(config_path, 'w') as f:
            f.write(new_content)
        logging.info(f"Patched deprecated config keys in {config_path}")
