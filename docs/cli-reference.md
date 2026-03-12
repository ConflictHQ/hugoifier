# CLI Reference

All commands are invoked via `python src/cli.py`.

## Global Options

```
python src/cli.py [--backend {anthropic,openai,google}] <command> ...
```

| Flag | Description |
|------|-------------|
| `--backend` | Override `HUGOIFIER_BACKEND` env var for this run |

---

## `complete` — Full Pipeline

Runs the full pipeline: detect → copy/convert → patch → decapify.

```bash
python src/cli.py complete <path> [options]
```

| Argument | Description |
|----------|-------------|
| `path` | Path to a Hugo theme directory or raw HTML directory |
| `--output`, `-o` | Output directory (default: `output/{theme-name}`) |
| `--cms-name` | Whitelabel CMS name shown in admin UI |
| `--cms-logo` | URL to a logo image for the admin UI |
| `--cms-color` | Hex color for the admin top bar (e.g. `#1a1a2e`) |

**Examples:**

```bash
# Hugo theme with exampleSite
python src/cli.py complete themes/revolve-hugo

# Custom output path
python src/cli.py complete themes/revolve-hugo --output /var/www/mysite

# With whitelabel CMS
python src/cli.py complete themes/revolve-hugo \
  --cms-name "My Studio" \
  --cms-color "#0d1117"
```

---

## `analyze` — Inspect Theme Structure

Analyzes a theme and reports its layout files, content types, and exampleSite location. For raw HTML, uses AI to suggest partials and Hugo template tags.

```bash
python src/cli.py analyze <path>
```

---

## `hugoify` — HTML → Hugo Conversion

Converts a raw HTML file or directory to Hugo layout files. For an existing Hugo theme, validates its structure.

```bash
python src/cli.py hugoify <path>
```

---

## `decapify` — Add Decap CMS

Adds Decap CMS to an already-assembled Hugo site. Introspects `content/` to auto-generate `static/admin/config.yml`.

```bash
python src/cli.py decapify <path> [options]
```

| Argument | Description |
|----------|-------------|
| `path` | Path to an assembled Hugo site (contains `hugo.toml`, `content/`, `themes/`) |
| `--cms-name` | Whitelabel CMS name |
| `--cms-logo` | Logo URL |
| `--cms-color` | Top-bar hex color |

---

## `translate` — Translate Content

Translates a content file to another language using the configured AI backend.

```bash
python src/cli.py translate <path> [--target-language LANGUAGE]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `path` | — | Path to the content file |
| `--target-language` | `Spanish` | Language to translate into |

---

## `deploy` — Deploy to Cloudflare _(stub)_

```bash
python src/cli.py deploy <path> <zone>
```

---

## `cloudflare` — Configure Cloudflare _(stub)_

```bash
python src/cli.py cloudflare <path> <zone>
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (bad input path, missing API key, etc.) — message printed to stderr |
