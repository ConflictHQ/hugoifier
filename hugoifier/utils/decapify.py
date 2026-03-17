"""
Generates Decap CMS integration for a Hugo site.

Writes:
  static/admin/index.html  — Decap CMS admin panel
  static/admin/config.yml  — CMS config mapped to actual content structure
"""

import logging
import os
import re

import yaml

DECAP_CDN = "https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"

# Whitelabel defaults — override via decapify() kwargs or env vars
DEFAULT_CMS_NAME = os.getenv('CMS_NAME', 'Content Manager')
DEFAULT_CMS_LOGO = os.getenv('CMS_LOGO_URL', '')     # URL or empty
DEFAULT_CMS_COLOR = os.getenv('CMS_COLOR', '#2e3748')  # top-bar background


def decapify(
    site_dir: str,
    cms_name: str = None,
    cms_logo: str = None,
    cms_color: str = None,
    github_repo: str = None,
) -> str:
    """
    Add Decap CMS to a Hugo site directory.

    Args:
        site_dir:    Root of the assembled Hugo site (has hugo.toml, content/, themes/).
        cms_name:    Whitelabel name shown in the admin UI (default: 'Content Manager').
        cms_logo:    URL to a logo image for the admin UI (optional).
        cms_color:   Hex color for the admin top bar (default: '#2e3748').
        github_repo: GitHub repo slug e.g. 'ConflictHQ/my-site' (optional, for GitHub backend).

    Returns:
        Status message.
    """
    logging.info(f"Adding Decap CMS to {site_dir} ...")

    admin_dir = os.path.join(site_dir, 'static', 'admin')
    os.makedirs(admin_dir, exist_ok=True)

    branding = {
        'name': cms_name or DEFAULT_CMS_NAME,
        'logo': cms_logo or DEFAULT_CMS_LOGO,
        'color': cms_color or DEFAULT_CMS_COLOR,
    }

    _write_admin_index(admin_dir, branding)
    _write_decap_config(site_dir, admin_dir, github_repo=github_repo)
    _write_oauth_functions(site_dir)
    _create_media_dir(site_dir)

    logging.info("Decap CMS integration complete.")
    return "Decap CMS integration complete"


# ---------------------------------------------------------------------------
# Admin index.html
# ---------------------------------------------------------------------------

def _sanitize_color(color: str) -> str:
    """Allow only valid CSS hex colors (#rgb or #rrggbb) to prevent style injection."""
    if re.fullmatch(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?', color):
        return color
    return '#2e3748'  # fall back to default


def _write_admin_index(admin_dir: str, branding: dict):
    import html as html_mod
    name = html_mod.escape(branding['name'])
    logo_html = ''
    if branding['logo']:
        logo_url = html_mod.escape(branding['logo'])
        logo_html = f'\n  <img src="{logo_url}" alt="{name}" style="max-height:40px;margin:8px 0;">'

    color_css = ''
    if branding['color']:
        safe_color = _sanitize_color(branding['color'])
        color_css = f"""
  <style>
    [class^="AppHeader"] {{ background-color: {safe_color} !important; }}
  </style>"""

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex" />
  <title>{name}</title>{color_css}
</head>
<body>{logo_html}
  <script src="{DECAP_CDN}"></script>
</body>
</html>
"""
    with open(os.path.join(admin_dir, 'index.html'), 'w') as f:
        f.write(html)


# ---------------------------------------------------------------------------
# config.yml
# ---------------------------------------------------------------------------

def _write_decap_config(site_dir: str, admin_dir: str, github_repo: str = None):
    content_dir = os.path.join(site_dir, 'content')
    collections = _build_collections(content_dir)

    backend = {
        'name': 'github',
        'branch': 'main',
    }
    if github_repo:
        backend['repo'] = github_repo
    backend['base_url'] = ''  # placeholder — set to deployed site URL
    backend['auth_endpoint'] = '/api/auth'

    config = {
        'backend': backend,
        'media_folder': 'static/images/uploads',
        'public_folder': '/images/uploads',
        'collections': collections,
    }

    config_path = os.path.join(admin_dir, 'config.yml')
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    logging.info(f"Wrote Decap CMS config to {config_path}")


def _collect_md_files(dirpath: str) -> list:
    """Recursively collect all .md files under dirpath (excluding _index.md)."""
    found = []
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            if f.endswith('.md') and f != '_index.md':
                found.append(os.path.join(root, f))
    return found


def _build_collections(content_dir: str) -> list:
    """
    Inspect content/ to build Decap CMS collections.
    - Subdirs with any .md files (at any depth) → folder collection (e.g. blog)
    - Subdirs with only a top-level _index.md → file collection (e.g. about, contact)
    """
    if not os.path.isdir(content_dir):
        return [_default_pages_collection()]

    collections = []

    entries = sorted(os.listdir(content_dir))
    for entry in entries:
        subdir = os.path.join(content_dir, entry)
        if not os.path.isdir(subdir):
            continue

        # Collect all .md files at any depth (excluding _index.md)
        non_index = _collect_md_files(subdir)
        has_index = os.path.exists(os.path.join(subdir, '_index.md'))

        if non_index:
            # Folder collection (blog, posts, etc.) — use shallowest sample for field inference
            rel_files = [os.path.relpath(f, subdir) for f in non_index]
            fields = _infer_fields_for_folder(subdir, rel_files)
            collections.append({
                'name': entry,
                'label': entry.replace('-', ' ').title(),
                'folder': f'content/{entry}',
                'create': True,
                'slug': '{{slug}}',
                'fields': fields,
            })
        elif has_index:
            # File collection (single page)
            fields = _infer_fields_for_file(os.path.join(subdir, '_index.md'))
            collections.append({
                'name': entry,
                'label': entry.replace('-', ' ').title(),
                'files': [{
                    'name': entry,
                    'label': entry.replace('-', ' ').title(),
                    'file': f'content/{entry}/_index.md',
                    'fields': fields,
                }],
            })

    if not collections:
        collections.append(_default_pages_collection())

    return collections


def _infer_fields_for_folder(subdir: str, md_files: list) -> list:
    """Read a sample .md file and extract frontmatter keys as fields."""
    # md_files may be relative paths (from _collect_md_files); resolve to absolute
    first = md_files[0]
    sample = first if os.path.isabs(first) else os.path.join(subdir, first)
    frontmatter = _parse_frontmatter(sample)

    fields = []
    field_map = {
        'title': {'label': 'Title', 'name': 'title', 'widget': 'string'},
        'date': {'label': 'Date', 'name': 'date', 'widget': 'datetime'},
        'description': {'label': 'Description', 'name': 'description', 'widget': 'text'},
        'image': {'label': 'Image', 'name': 'image', 'widget': 'image', 'required': False},
        'categories': {'label': 'Categories', 'name': 'categories', 'widget': 'list',
                       'required': False},
        'tags': {'label': 'Tags', 'name': 'tags', 'widget': 'list', 'required': False},
        'draft': {'label': 'Draft', 'name': 'draft', 'widget': 'boolean', 'default': False},
        'author': {'label': 'Author', 'name': 'author', 'widget': 'string', 'required': False},
    }

    # Add known fields in a logical order
    for key in ['title', 'date', 'description', 'image', 'categories', 'tags', 'author', 'draft']:
        if key in frontmatter:
            fields.append(field_map[key])

    # Add any remaining frontmatter keys not in our map
    for key, value in frontmatter.items():
        if key not in field_map and key not in ('type', 'layout', 'url'):
            widget = _widget_for_value(value)
            fields.append({'label': key.title(), 'name': key, 'widget': widget, 'required': False})

    # Always include body
    fields.append({'label': 'Body', 'name': 'body', 'widget': 'markdown'})

    return fields


def _infer_fields_for_file(md_path: str) -> list:
    """For a single page (_index.md), infer fields from frontmatter."""
    frontmatter = _parse_frontmatter(md_path)
    fields = []
    for key, value in frontmatter.items():
        widget = _widget_for_value(value)
        fields.append({'label': key.title(), 'name': key, 'widget': widget, 'required': False})
    fields.append({'label': 'Body', 'name': 'body', 'widget': 'markdown'})
    return fields


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


def _widget_for_value(value) -> str:
    if isinstance(value, bool):
        return 'boolean'
    if isinstance(value, (int, float)):
        return 'number'
    if isinstance(value, list):
        return 'list'
    return 'string'


def _default_pages_collection() -> dict:
    return {
        'name': 'pages',
        'label': 'Pages',
        'folder': 'content',
        'create': True,
        'slug': '{{slug}}',
        'fields': [
            {'label': 'Title', 'name': 'title', 'widget': 'string'},
            {'label': 'Body', 'name': 'body', 'widget': 'markdown'},
        ],
    }


# ---------------------------------------------------------------------------
# OAuth functions (Cloudflare Pages Functions)
# ---------------------------------------------------------------------------

_AUTH_JS = """\
export async function onRequest(context) {
    const { request, env } = context;
    const client_id = env.GITHUB_CLIENT_ID;

    try {
        const url = new URL(request.url);
        const redirectUrl = new URL('https://github.com/login/oauth/authorize');
        redirectUrl.searchParams.set('client_id', client_id);
        redirectUrl.searchParams.set('redirect_uri', url.origin + '/api/callback');
        redirectUrl.searchParams.set('scope', 'repo user');
        redirectUrl.searchParams.set(
            'state',
            crypto.getRandomValues(new Uint8Array(12)).join(''),
        );
        return Response.redirect(redirectUrl.href, 301);
    } catch (error) {
        console.error(error);
        return new Response(error.message, { status: 500 });
    }
}
"""

_CALLBACK_JS = """\
function renderBody(status, content) {
    const html = `
    <script>
      const receiveMessage = (message) => {
        window.opener.postMessage(
          'authorization:github:${status}:${JSON.stringify(content)}',
          message.origin
        );
        window.removeEventListener("message", receiveMessage, false);
      }
      window.addEventListener("message", receiveMessage, false);
      window.opener.postMessage("authorizing:github", "*");
    </script>
    `;
    const blob = new Blob([html]);
    return blob;
}

export async function onRequest(context) {
    const { request, env } = context;
    const client_id = env.GITHUB_CLIENT_ID;
    const client_secret = env.GITHUB_CLIENT_SECRET;

    try {
        const url = new URL(request.url);
        const code = url.searchParams.get('code');
        const response = await fetch(
            'https://github.com/login/oauth/access_token',
            {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                    'user-agent': 'hugoifier-cms-oauth',
                    'accept': 'application/json',
                },
                body: JSON.stringify({ client_id, client_secret, code }),
            },
        );
        const result = await response.json();
        if (result.error) {
            return new Response(renderBody('error', result), {
                headers: { 'content-type': 'text/html;charset=UTF-8' },
                status: 401
            });
        }
        const token = result.access_token;
        const provider = 'github';
        const responseBody = renderBody('success', { token, provider });
        return new Response(responseBody, {
            headers: { 'content-type': 'text/html;charset=UTF-8' },
            status: 200
        });
    } catch (error) {
        console.error(error);
        return new Response(error.message, {
            headers: { 'content-type': 'text/html;charset=UTF-8' },
            status: 500,
        });
    }
}
"""


def _write_oauth_functions(site_dir: str):
    """Write Cloudflare Pages Functions for GitHub OAuth (Decap CMS auth)."""
    functions_dir = os.path.join(site_dir, 'functions', 'api')
    os.makedirs(functions_dir, exist_ok=True)

    with open(os.path.join(functions_dir, 'auth.js'), 'w') as f:
        f.write(_AUTH_JS)

    with open(os.path.join(functions_dir, 'callback.js'), 'w') as f:
        f.write(_CALLBACK_JS)

    logging.info("Wrote OAuth functions to functions/api/")


def _create_media_dir(site_dir: str):
    """Create the media uploads directory so Decap doesn't 404."""
    media_dir = os.path.join(site_dir, 'static', 'images', 'uploads')
    os.makedirs(media_dir, exist_ok=True)
    gitkeep = os.path.join(media_dir, '.gitkeep')
    if not os.path.exists(gitkeep):
        with open(gitkeep, 'w') as f:
            pass
