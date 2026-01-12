"""
API endpoints for map and routing.
"""

from __future__ import annotations

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


@MAP_API.route(END_POINT, methods=["GET"])
def api_map():
    web_map = Map(
        start="Karlsruhe Hauptbahnhof, Germany",
        end="Karlsruhe Durlach Bahnhof, Germany",
    ).to_html()
    return jsonify({"map": web_map}), 200


@MAP_API.route(f"{END_POINT}/route", methods=["POST"])
def api_map_route():
    payload = request.get_json(silent=True) or {}
    start = request.form["start"]
    end = request.form["end"]

    if not isinstance(start, str) or not start.strip():
        return _bad_request("Missing or invalid 'start' (must be a non-empty string).")
    if not isinstance(end, str) or not end.strip():
        return _bad_request("Missing or invalid 'end' (must be a non-empty string).")

    line_number = payload.get("line_number")
    line_id = payload.get("line_id")

    route_color = "#d32f2f"
    if isinstance(line_number, str) and line_number.strip():
        route_color = get_line_color_by_number(line_number.strip(), default=route_color)
    elif isinstance(line_id, str) and line_id.strip():
        route_color = get_line_color_by_id(line_id.strip(), default=route_color)

    web_map = Map(
        start=start.strip(),
        end=end.strip(),
        route_color=route_color,
    ).to_html()

    return jsonify(
        {
            "map": web_map,
            "start": start.strip(),
            "end": end.strip(),
            "route_color": route_color,
        }
    ), 200


@MAP_API.route(f"{END_POINT}/lines", methods=["GET"])
def api_map_lines():
    return jsonify({"lines": list_lines()}), 200
