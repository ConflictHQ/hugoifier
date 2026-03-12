"""Add src/ to sys.path so tests can import from utils.* directly."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
