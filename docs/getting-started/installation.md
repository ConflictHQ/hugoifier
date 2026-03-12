# Installation

## Prerequisites

- **Python 3.11+**
- **Hugo extended** — for building the generated site locally (`brew install hugo` on macOS)
- **At least one AI API key**

## From Source

```bash
git clone https://github.com/ConflictHQ/hugoifier.git
cd hugoifier
pip install -r requirements.txt
```

## Docker

```bash
git clone https://github.com/ConflictHQ/hugoifier.git
cd hugoifier
```

Then run with your preferred backend:

=== "Anthropic (default)"

    ```bash
    ANTHROPIC_API_KEY=your_key docker compose up
    ```

=== "OpenAI"

    ```bash
    OPENAI_API_KEY=your_key HUGOIFIER_BACKEND=openai docker compose up
    ```

=== "Google"

    ```bash
    GOOGLE_API_KEY=your_key HUGOIFIER_BACKEND=google docker compose up
    ```

## API Keys

Set the key for your chosen backend:

| Backend | Environment Variable | Model |
|---------|---------------------|-------|
| Anthropic (default) | `ANTHROPIC_API_KEY` | `claude-sonnet-4-6` |
| OpenAI | `OPENAI_API_KEY` | `gpt-4-turbo` |
| Google | `GOOGLE_API_KEY` | `gemini-1.5-pro` |

Override the model with `ANTHROPIC_MODEL`, `OPENAI_MODEL`, or `GOOGLE_MODEL`.
