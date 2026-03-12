"""
generate_decap_config — thin wrapper kept for backwards compatibility.
The real implementation lives in decapify.py.
"""

from .decapify import decapify


def generate_decap_config(theme_path: str) -> str:
    return decapify(theme_path)
