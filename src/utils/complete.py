"""
Full end-to-end pipeline: detect → copy → configure → decap.

For already-Hugo themes: assembles a clean, standalone site.
For raw HTML themes: calls hugoify first, then assembles.
"""

import logging
import os
import shutil

from utils.theme_finder import find_hugo_theme, find_raw_html_files
from utils.hugoify import hugoify_html
from utils.decapify import decapify
from utils.theme_patcher import patch_theme, patch_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def complete(
    input_path: str,
    output_dir: str = None,
    cms_name: str = None,
    cms_logo: str = None,
    cms_color: str = None,
) -> str:
    """
    Run the full pipeline for a theme.

    Args:
        input_path: Path to a theme directory (from themes/) or raw HTML dir.
        output_dir: Where to write the output site. Defaults to output/{theme-name}.
        cms_name:   Whitelabel CMS name for Decap admin UI.
        cms_logo:   Whitelabel logo URL for Decap admin UI.
        cms_color:  Whitelabel top-bar color for Decap admin UI.

    Returns:
        Path to the generated site, or error message.
    """
    logging.info(f"Starting pipeline for {input_path} ...")

    branding = {'cms_name': cms_name, 'cms_logo': cms_logo, 'cms_color': cms_color}
    info = find_hugo_theme(input_path)

    if info:
        return _assemble_hugo_site(info, output_dir, branding)
    else:
        # Raw HTML path
        html_files = find_raw_html_files(input_path)
        if not html_files:
            return f"No Hugo theme or HTML files found in {input_path}"
        return _convert_raw_html(input_path, html_files, output_dir, branding)


# ---------------------------------------------------------------------------
# Hugo theme path
# ---------------------------------------------------------------------------

def _assemble_hugo_site(info: dict, output_dir: str = None, branding: dict = None) -> str:
    theme_dir = info['theme_dir']
    example_site = info['example_site']
    theme_name = info['theme_name']

    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'output',
            theme_name,
        )

    logging.info(f"Building site at {output_dir} ...")
    os.makedirs(output_dir, exist_ok=True)

    # 1. Copy theme files → themes/{theme_name}/
    dest_theme = os.path.join(output_dir, 'themes', theme_name)
    _copy_dir(theme_dir, dest_theme, exclude={'exampleSite', '__MACOSX', '.DS_Store'})
    logging.info(f"Copied theme to {dest_theme}")
    patch_theme(dest_theme)

    # 2. Copy exampleSite content/static/data → site root
    if example_site:
        for subdir in ('content', 'data', 'i18n'):
            src = os.path.join(example_site, subdir)
            if os.path.isdir(src):
                _copy_dir(src, os.path.join(output_dir, subdir))
                logging.info(f"Copied {subdir}/ from exampleSite")

        # Static: merge exampleSite/static into output/static
        src_static = os.path.join(example_site, 'static')
        if os.path.isdir(src_static):
            _copy_dir(src_static, os.path.join(output_dir, 'static'))
            logging.info("Copied static/ from exampleSite")

        # Write hugo.toml from exampleSite config
        config_toml = _find_config(example_site)
        if config_toml:
            _write_hugo_toml(config_toml, output_dir, theme_name)
        else:
            _write_minimal_hugo_toml(output_dir, theme_name)
    else:
        _write_minimal_hugo_toml(output_dir, theme_name)
        # Create minimal content/_index.md
        content_dir = os.path.join(output_dir, 'content')
        os.makedirs(content_dir, exist_ok=True)
        index_md = os.path.join(content_dir, '_index.md')
        if not os.path.exists(index_md):
            with open(index_md, 'w') as f:
                f.write('---\ntitle: Home\n---\n')

    # 3. Generate Decap CMS config
    b = branding or {}
    decapify(output_dir, cms_name=b.get('cms_name'), cms_logo=b.get('cms_logo'), cms_color=b.get('cms_color'))

    logging.info(f"Done. Site ready at: {output_dir}")
    logging.info(f"Run: cd {output_dir} && hugo serve")
    return output_dir


# ---------------------------------------------------------------------------
# Raw HTML path
# ---------------------------------------------------------------------------

def _convert_raw_html(input_path: str, html_files: list, output_dir: str = None, branding: dict = None) -> str:
    theme_name = os.path.basename(os.path.abspath(input_path))

    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'output',
            theme_name,
        )

    logging.info(f"Converting raw HTML theme: {theme_name}")

    # Use AI to convert the main HTML file to Hugo layouts
    main_html = _pick_main_html(html_files)
    logging.info(f"Converting {main_html} ...")
    hugo_layouts = hugoify_html(main_html)

    os.makedirs(output_dir, exist_ok=True)

    # Write converted layouts
    theme_layouts_dir = os.path.join(output_dir, 'themes', theme_name, 'layouts')
    os.makedirs(os.path.join(theme_layouts_dir, '_default'), exist_ok=True)
    os.makedirs(os.path.join(theme_layouts_dir, 'partials'), exist_ok=True)

    for filename, content in hugo_layouts.items():
        dest = os.path.join(theme_layouts_dir, filename)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w') as f:
            f.write(content)

    # Copy CSS/JS/images
    for ext_dir in ('css', 'js', 'images', 'img', 'assets', 'fonts'):
        src = os.path.join(input_path, ext_dir)
        if os.path.isdir(src):
            _copy_dir(src, os.path.join(output_dir, 'themes', theme_name, 'static', ext_dir))

    _write_minimal_hugo_toml(output_dir, theme_name)

    # Create minimal content
    content_dir = os.path.join(output_dir, 'content')
    os.makedirs(content_dir, exist_ok=True)
    with open(os.path.join(content_dir, '_index.md'), 'w') as f:
        f.write('---\ntitle: Home\n---\n')

    b = branding or {}
    decapify(output_dir, cms_name=b.get('cms_name'), cms_logo=b.get('cms_logo'), cms_color=b.get('cms_color'))

    logging.info(f"Done. Site ready at: {output_dir}")
    return output_dir


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _copy_dir(src: str, dest: str, exclude: set = None):
    """Copy src → dest, skipping excluded names."""
    exclude = exclude or set()
    if not os.path.isdir(src):
        return
    os.makedirs(dest, exist_ok=True)
    for item in os.listdir(src):
        if item in exclude or item.startswith('._'):
            continue
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            _copy_dir(s, d, exclude)
        else:
            shutil.copy2(s, d)


def _find_config(example_site: str) -> str | None:
    """Find config.toml or hugo.toml in exampleSite."""
    for name in ('hugo.toml', 'config.toml'):
        p = os.path.join(example_site, name)
        if os.path.exists(p):
            return p
    # config/_default/config.toml pattern
    p = os.path.join(example_site, 'config', '_default', 'config.toml')
    if os.path.exists(p):
        return p
    return None


def _write_hugo_toml(source_config: str, output_dir: str, theme_name: str):
    """Copy source config to hugo.toml, ensuring theme = theme_name and modern key names."""
    import re
    with open(source_config, 'r') as f:
        content = f.read()

    # Fix deprecated keys for Hugo >= v0.128
    content = re.sub(r'^paginate\s*=\s*(\d+)', r'[pagination]\n  pagerSize = \1', content, flags=re.MULTILINE)

    # Suppress noisy but harmless warnings from example content
    if 'ignoreLogs' not in content:
        content += "\nignorelogs = ['warning-goldmark-raw-html']\n"

    # Ensure theme is set correctly
    if re.search(r'^theme\s*=', content, re.MULTILINE):
        content = re.sub(r'^theme\s*=.*$', f'theme = "{theme_name}"', content, flags=re.MULTILINE)
    else:
        content = f'theme = "{theme_name}"\n' + content

    dest = os.path.join(output_dir, 'hugo.toml')
    with open(dest, 'w') as f:
        f.write(content)
    patch_config(dest)
    logging.info("Wrote hugo.toml")


def _write_minimal_hugo_toml(output_dir: str, theme_name: str):
    dest = os.path.join(output_dir, 'hugo.toml')
    with open(dest, 'w') as f:
        f.write(f'''baseURL = "http://localhost:1313/"
languageCode = "en-us"
title = "{theme_name.replace('-', ' ').title()}"
theme = "{theme_name}"
''')
    logging.info("Wrote minimal hugo.toml")


def _pick_main_html(html_files: list) -> str:
    """Pick the most likely 'main' HTML file (index.html or first one)."""
    for f in html_files:
        if os.path.basename(f).lower() in ('index.html', 'home.html', 'main.html'):
            return f
    return html_files[0]
