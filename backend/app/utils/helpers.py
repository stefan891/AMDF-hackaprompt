"""Miscellaneous utility functions."""

from datetime import datetime


def parse_iso(value: str):
    """Safely parse an ISO-8601 string; return None on failure."""
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
