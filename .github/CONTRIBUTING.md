# Contributing to Hugoifier

Thank you for your interest in contributing to Hugoifier!

## Development Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/hugoifier.git
   cd hugoifier
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install ruff pytest
   ```

4. **Set up at least one AI provider API key:**

   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   # or
   export OPENAI_API_KEY="sk-..."
   # or
   export GOOGLE_API_KEY="..."
   ```

## Running Tests

```bash
pytest tests/
```

Tests are written to avoid real AI calls — they mock the `call_ai` function or test pure functions only. Keep it that way.

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting.

```bash
# Check for issues
ruff check src/ tests/

# Auto-fix
ruff check --fix src/ tests/
```

All contributions must pass `ruff check` with no errors before merging.

## Commit Conventions

Use the imperative mood, prefix with a type:

- `fix(module): description` — bug fixes
- `feat(module): description` — new features
- `docs: description` — documentation only
- `test: description` — tests only
- `chore: description` — maintenance, deps, tooling

Keep subject lines under 72 characters.

## Pull Request Process

1. Branch from `main`
2. Write or update tests for your changes
3. Run `pytest tests/` and `ruff check src/ tests/` — both must be clean
4. Open a PR against `main` and fill out the template
5. A maintainer will review within a few business days

## Reporting Bugs and Requesting Features

- **Bugs:** [Bug Report](https://github.com/ConflictHQ/hugoifier/issues/new?template=bug_report.yml)
- **Features:** [Feature Request](https://github.com/ConflictHQ/hugoifier/issues/new?template=feature_request.yml)
- **Questions:** [Discussions](https://github.com/ConflictHQ/hugoifier/discussions)

## Security

Do **not** open a public issue for security vulnerabilities. See [SECURITY.md](SECURITY.md).

## License

By contributing to Hugoifier, you agree that your contributions will be licensed under the [MIT License](../LICENSE).
