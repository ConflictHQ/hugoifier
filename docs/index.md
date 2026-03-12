# Hugoifier

**AI-powered Hugo theme converter with Decap CMS integration.**

Hugoifier converts any HTML/CSS theme into a production-ready Hugo site — complete with layouts, content structure, and a fully configured Decap CMS admin panel. Supports Anthropic Claude, OpenAI GPT-4, and Google Gemini as AI backends.

---

## Features

- **HTML → Hugo** — AI converts raw HTML/CSS templates into valid Hugo Go template files with proper partials, blocks, and template variables
- **Multi-backend AI** — Route to Anthropic (default), OpenAI, or Google Gemini via `HUGOIFIER_BACKEND`
- **Decap CMS out of the box** — Auto-generates `static/admin/config.yml` by introspecting your content structure, including deeply nested collections
- **Hugo API modernization** — Automatically patches deprecated Hugo APIs (`.Site.DisqusShortname`, `.Site.GoogleAnalytics`, `paginate`, etc.) for Hugo ≥ v0.128
- **Whitelabel CMS** — Customize the Decap admin panel name, logo, and color per deployment
- **Smart theme detection** — Handles messy zip-extracted directory structures, skips `__MACOSX` artifacts, detects `exampleSite` automatically
- **Docker support** — Fully containerized with `docker-compose.yml`

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your AI backend key
export ANTHROPIC_API_KEY=your_key_here

# Convert a Hugo theme
python src/cli.py complete themes/my-theme

# Convert raw HTML
python src/cli.py complete path/to/html-theme/

# Output goes to output/{theme-name}/ by default
cd output/my-theme && hugo serve
```

## Installation

=== "From source"

    ```bash
    git clone https://github.com/ConflictHQ/hugoifier.git
    cd hugoifier
    pip install -r requirements.txt
    ```

=== "Docker"

    ```bash
    git clone https://github.com/ConflictHQ/hugoifier.git
    cd hugoifier
    ANTHROPIC_API_KEY=your_key docker compose up
    ```

## Requirements

- Python 3.11+
- At least one AI API key: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY`
- Hugo extended (for building the output site)

## Pipeline Overview

```
Input (Hugo theme or raw HTML)
        ↓
[Theme Finder] — detect Hugo theme vs raw HTML
        ↓
[Hugoify] — AI converts HTML → Hugo layouts (raw HTML only)
        ↓
[Assemble] — copy theme + exampleSite, write hugo.toml
        ↓
[Theme Patcher] — fix deprecated Hugo APIs
        ↓
[Decapify] — generate Decap CMS config from content structure
        ↓
output/{theme-name}/   ← ready to run with hugo serve
```

## License

MIT License — Copyright &copy; 2026 CONFLICT LLC. All rights reserved.
