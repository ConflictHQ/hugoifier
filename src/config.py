"""
Multi-backend AI configuration.

Set HUGOIFIER_BACKEND env var to switch backends:
  anthropic  (default) — claude-sonnet-4-6
  openai               — gpt-4-turbo
  google               — gemini-1.5-pro

Model can be overridden per-backend:
  ANTHROPIC_MODEL, OPENAI_MODEL, GOOGLE_MODEL
"""

import os

BACKEND = os.getenv('HUGOIFIER_BACKEND', 'anthropic').lower()

# Anthropic settings
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-6')

# OpenAI settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')

# Google settings
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_MODEL = os.getenv('GOOGLE_MODEL', 'gemini-1.5-pro')

MAX_TOKENS = int(os.getenv('HUGOIFIER_MAX_TOKENS', '4096'))


def call_ai(prompt: str, system: str = "You are a helpful Hugo theme conversion assistant.") -> str:
    """
    Call the configured AI backend and return the response text.
    This is the single entry point for all AI calls in the codebase.
    """
    if BACKEND == 'anthropic':
        return _call_anthropic(prompt, system)
    elif BACKEND == 'openai':
        return _call_openai(prompt, system)
    elif BACKEND == 'google':
        return _call_google(prompt, system)
    else:
        raise ValueError(
            f"Unknown backend: {BACKEND!r}. "
            "Set HUGOIFIER_BACKEND to 'anthropic', 'openai', or 'google'."
        )


def _call_anthropic(prompt: str, system: str) -> str:
    if not ANTHROPIC_API_KEY:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set")
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _call_openai(prompt: str, system: str) -> str:
    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY is not set")
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content.strip()


def _call_google(prompt: str, system: str) -> str:
    if not GOOGLE_API_KEY:
        raise EnvironmentError("GOOGLE_API_KEY is not set")
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name=GOOGLE_MODEL,
        system_instruction=system,
    )
    response = model.generate_content(prompt)
    return response.text
