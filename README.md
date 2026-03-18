# Hugoifier

Convert any website to a production-ready [Hugo](https://gohugo.io/) site with [Decap CMS](https://decapcms.org/) — pixel-perfect, no content loss.

## How it works

Hugoifier takes three types of input and produces a deployable Hugo site with CMS:

| Input | Method | AI needed? |
|-------|--------|-----------|
| **Hugo theme** | Assembles, patches deprecated APIs, adds CMS | No |
| **Next.js app** | Captures rendered HTML from dev server | No |
| **Raw HTML** | Extracts head/body directly into Hugo templates | No |

AI is only used as a fallback (Next.js without a running dev server) or for lightweight structural analysis.

## Quick start

```bash
pip install hugoifier

# Convert a Hugo theme
hugoifier complete themes/my-theme

# Convert a Next.js app (start your dev server first)
hugoifier complete path/to/nextjs-app

# Convert a raw HTML site
hugoifier complete path/to/html-site
```

Output goes to `output/{name}/` — a complete Hugo site ready to serve:

```bash
cd output/my-site && hugo serve
```

## What you get

- Hugo site with all content, styles, and assets preserved
- Decap CMS at `/admin/` with GitHub OAuth (Cloudflare Pages Functions)
- `functions/api/auth.js` + `callback.js` for OAuth flow
- Whitelabel CMS branding (`--cms-name`, `--cms-logo`, `--cms-color`)

### Deploy to Cloudflare Pages

```bash
hugo --minify
npx wrangler pages deploy public --project-name my-site
```

Set `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` as environment variables for CMS auth.

## Configuration

```bash
# Choose AI backend (only needed for fallback conversion)
HUGOIFIER_BACKEND=anthropic  # or openai, google
ANTHROPIC_API_KEY=sk-...

# Whitelabel CMS
hugoifier complete my-site --cms-name "My CMS" --cms-logo https://... --cms-color "#515be3"
```

## Development

```bash
git clone https://github.com/ConflictHQ/hugoifier.git
cd hugoifier
pip install -e ".[dev]"
pytest
```

## Built with

Hugoifier is built on top of two excellent open-source projects:

- **[Hugo](https://gohugo.io/)** — The world's fastest static site generator. Apache 2.0 licensed. Created by [Steve Francia](https://github.com/spf13) and [Bjarne Pedersen](https://github.com/bep) and [contributors](https://github.com/gohugoio/hugo/graphs/contributors).
- **[Decap CMS](https://decapcms.org/)** (formerly Netlify CMS) — Open-source content management for Git workflows. MIT licensed. Maintained by the [Decap community](https://github.com/decaporg/decap-cms/graphs/contributors).

We're grateful to both communities for building the tools that make this project possible.

## License

MIT — see [LICENSE](LICENSE) for details.

Made by [Conflict](https://weareconflict.com).
