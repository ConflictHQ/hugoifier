# Quick Start

## Convert a Hugo Theme

Most Hugo themes include an `exampleSite/` directory. Hugoifier assembles a complete, working site from it:

```bash
export ANTHROPIC_API_KEY=your_key

python src/cli.py complete themes/my-hugo-theme
# → output/my-hugo-theme/
```

Then test it:

```bash
cd output/my-hugo-theme
hugo serve
# Open http://localhost:1313
```

The Decap CMS admin panel is automatically available at `http://localhost:1313/admin/`.

## Convert Raw HTML

For a plain HTML/CSS theme:

```bash
python src/cli.py complete path/to/html-theme/
# → output/html-theme/
```

Hugoifier sends the main HTML file to the AI backend and converts it to Hugo layout files (`_default/baseof.html`, `partials/header.html`, etc.).

## Custom Output Directory

```bash
python src/cli.py complete themes/my-theme --output /tmp/my-site
```

## Whitelabel Decap CMS

```bash
python src/cli.py complete themes/my-theme \
  --cms-name "My CMS" \
  --cms-color "#1a1a2e" \
  --cms-logo "https://example.com/logo.png"
```

## Switch AI Backend

```bash
# Use OpenAI instead of Anthropic
HUGOIFIER_BACKEND=openai OPENAI_API_KEY=your_key python src/cli.py complete themes/my-theme

# Or via CLI flag
python src/cli.py --backend openai complete themes/my-theme
```
