"""Add repo root to sys.path so tests can import hugoifier.*."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
