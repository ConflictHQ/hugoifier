# Configuration

All configuration is via environment variables.

## AI Backend

| Variable | Default | Description |
|----------|---------|-------------|
| `HUGOIFIER_BACKEND` | `anthropic` | Backend to use: `anthropic`, `openai`, or `google` |
| `ANTHROPIC_API_KEY` | — | Required when using Anthropic backend |
| `OPENAI_API_KEY` | — | Required when using OpenAI backend |
| `GOOGLE_API_KEY` | — | Required when using Google backend |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-6` | Anthropic model override |
| `OPENAI_MODEL` | `gpt-4-turbo` | OpenAI model override |
| `GOOGLE_MODEL` | `gemini-1.5-pro` | Google model override |
| `HUGOIFIER_MAX_TOKENS` | `4096` | Max tokens for AI responses |

## Decap CMS Defaults

| Variable | Default | Description |
|----------|---------|-------------|
| `CMS_NAME` | `Content Manager` | Default CMS admin panel title |
| `CMS_LOGO_URL` | _(empty)_ | Default logo URL for admin panel |
| `CMS_COLOR` | `#2e3748` | Default top-bar hex color |

These defaults apply when the corresponding CLI flags (`--cms-name`, `--cms-logo`, `--cms-color`) are not passed.

## Example `.env`

```bash
HUGOIFIER_BACKEND=anthropic
ANTHROPIC_API_KEY=sk-ant-...

CMS_NAME=My Studio
CMS_COLOR=#1a1a2e
```

!!! warning
    Never commit `.env` to version control. It is listed in `.gitignore`.
