"""
API endpoints for map and routing.
"""

from __future__ import annotations
from typing import Any, Optional

from flask import request, jsonify

from backend.geography import Map
from backend.tram_lines import (
    list_lines,
    get_line_color_by_number,
    get_line_color_by_id,
)
from . import MAP_API

END_POINT = "/api/map"


def _bad_request(msg: str):
    return jsonify({"error": msg}), 400


def _as_bool(v: Any) -> Optional[bool]:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("true", "1", "yes", "on"):
            return True
        if s in ("false", "0", "no", "off"):
            return False
    return None


@MAP_API.route(END_POINT, methods=["GET"])
def api_map():
    """
    Default map with default start/end.
    Vehicle icon is DISABLED by default.
    """
    web_map = Map(
        start="Karlsruhe Hauptbahnhof, Germany",
        end="Karlsruhe Durlach Bahnhof, Germany",
        use_vehicle_icon=False,  # 🔴 DEFAULT
    ).to_html()

    return jsonify({"map": web_map}), 200


@MAP_API.route(f"{END_POINT}/route", methods=["POST"])
def api_map_route():
    payload = request.get_json(silent=True) or {}

    start = payload.get("start")
    end = payload.get("end")

    if not isinstance(start, str) or not start.strip():
        return _bad_request("Missing or invalid 'start'")
    if not isinstance(end, str) or not end.strip():
        return _bad_request("Missing or invalid 'end'")

    # Route color
    route_color = "#d32f2f"
    if isinstance(payload.get("line_number"), str):
        route_color = get_line_color_by_number(payload["line_number"], route_color)
    elif isinstance(payload.get("line_id"), str):
        route_color = get_line_color_by_id(payload["line_id"], route_color)

    # 🔴 DEFAULT: False (POINT)
    use_vehicle_icon = _as_bool(payload.get("use_vehicle_icon"))
    if use_vehicle_icon is None:
        use_vehicle_icon = False

    web_map = Map(
        start=start.strip(),
        end=end.strip(),
        route_color=route_color,
        use_vehicle_icon=use_vehicle_icon,
    ).to_html()

    return jsonify(
        {
            "map": web_map,
            "use_vehicle_icon": use_vehicle_icon,
        }
    ), 200


@MAP_API.route(f"{END_POINT}/lines", methods=["GET"])
def api_map_lines():
    return jsonify({"lines": list_lines()}), 200
