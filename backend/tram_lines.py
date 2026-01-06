"""
tram_lines.py

Load and query KVV tram line metadata from backend/db/KVV_Lines_v2.json.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any, Dict, List, Optional


_DB_PATH = os.path.join(os.path.dirname(__file__), "db", "KVV_Lines_v2.json")


@lru_cache(maxsize=1)
def load_kvv_lines() -> Dict[str, Any]:
    """
    Load the full KVV lines JSON structure.

    Returns:
        The parsed JSON dict (top-level contains key 'lines').
    """
    with open(_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def list_lines() -> List[Dict[str, Any]]:
    """
    Return the list of all line objects.

    Returns:
        A list of dicts, each representing a tram line.
    """
    data = load_kvv_lines()
    lines = data.get("lines", [])
    return lines if isinstance(lines, list) else []


def get_line_by_number(number: str) -> Optional[Dict[str, Any]]:
    """
    Find a tram line by its public number (e.g. "1", "2").

    Args:
        number: Line number as string.

    Returns:
        The matching line dict or None.
    """
    number = str(number).strip()
    for line in list_lines():
        if str(line.get("number", "")).strip() == number:
            return line
    return None


def get_line_by_id(line_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a tram line by its internal KVV id (e.g. 'kvv:21001:E:R:j20').

    Args:
        line_id: Full line id.

    Returns:
        The matching line dict or None.
    """
    line_id = str(line_id).strip()
    for line in list_lines():
        if str(line.get("id", "")).strip() == line_id:
            return line
    return None


def get_line_color_by_number(number: str, default: str = "#d32f2f") -> str:
    """
    Return the official hex color for a line by its public number (e.g. "1").

    Args:
        number: Public line number as string.
        default: Fallback color if line/field is missing.

    Returns:
        Hex color string (e.g. "#ED1C24") or default.
    """
    line = get_line_by_number(number)
    if not line:
        return default
    color = line.get("color")
    return color if isinstance(color, str) and color.startswith("#") else default


def get_line_color_by_id(line_id: str, default: str = "#d32f2f") -> str:
    """
    Return the official hex color for a line by its internal KVV id.

    Args:
        line_id: Internal line id.
        default: Fallback color if line/field is missing.

    Returns:
        Hex color string or default.
    """
    line = get_line_by_id(line_id)
    if not line:
        return default
    color = line.get("color")
    return color if isinstance(color, str) and color.startswith("#") else default
