"""
Shared helpers and Flask blueprints for all API modules.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from flask import Blueprint, jsonify


DEBUG_API = Blueprint("debug", __name__)
MAP_API = Blueprint("map", __name__)
PKG_API = Blueprint("package", __name__)
ROBOT_API = Blueprint("robot", __name__)
SIM_API = Blueprint("sim", __name__)


def json_response(payload: Dict[str, Any], status: int = 200):
    """
    Return a proper JSON response for API endpoints.

    Args:
        payload: JSON-serializable dictionary to return to the client.
        status: HTTP status code (default: 200).

    Returns:
        A Flask Response object with application/json content type.
    """
    return jsonify(payload), status
