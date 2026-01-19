"""
API endpoints for map and routing.

Variante A (Backend-master):
- requires robot_id
- starts a route job in Simulation
- returns an HTML map that polls robot state and animates smoothly
"""

from __future__ import annotations

from flask import request, g, jsonify
import osmnx as ox

from backend.geography import Map
from backend.tram_lines import list_lines, get_line_color_by_number, get_line_color_by_id
from . import MAP_API

END_POINT = "/api/map"


def _bad_request(msg: str):
    return jsonify({"error": msg}), 400


@MAP_API.route(END_POINT, methods=["GET"])
def api_map():
    # simple demo map (no robot polling)
    web_map = Map(
        start="Karlsruhe Hauptbahnhof, Germany",
        end="Karlsruhe Durlach Bahnhof, Germany",
        robot_id=None,
    ).to_html()
    return jsonify({"map": web_map}), 200


@MAP_API.route(f"{END_POINT}/route", methods=["POST"])
def api_map_route():
    payload = request.get_json(silent=True) or {}

    start = payload.get("start")
    end = payload.get("end")

    if not isinstance(start, str) or not start.strip():
        return _bad_request("Missing or invalid 'start' (must be a non-empty string).")
    if not isinstance(end, str) or not end.strip():
        return _bad_request("Missing or invalid 'end' (must be a non-empty string).")

    # required for Variante A
    robot_id = payload.get("robot_id")
    if robot_id is None:
        return _bad_request("Missing 'robot_id'. Create a robot first and pass robot_id.")
    try:
        robot_id = int(robot_id)
    except Exception:
        return _bad_request("Invalid 'robot_id' (must be int).")

    # optional params
    duration_s = payload.get("duration_s", 25)
    show_grey = bool(payload.get("show_grey", True))
    show_km = bool(payload.get("show_km", True))

    try:
        duration_s = float(duration_s)
    except Exception:
        duration_s = 25.0
    duration_s = max(3.0, min(duration_s, 300.0))

    # tram line color
    line_number = payload.get("line_number")
    line_id = payload.get("line_id")

    route_color = "#d32f2f"
    if isinstance(line_number, str) and line_number.strip():
        route_color = get_line_color_by_number(line_number.strip(), default=route_color)
    elif isinstance(line_id, str) and line_id.strip():
        route_color = get_line_color_by_id(line_id.strip(), default=route_color)

    # compute coords once (backend uses them for simulation)
    city = Map.CITY_DEFAULT
    G = ox.graph_from_place(city, network_type="drive")
    start_lat, start_lon = ox.geocode(start.strip())
    end_lat, end_lon = ox.geocode(end.strip())
    start_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
    end_node = ox.distance.nearest_nodes(G, end_lon, end_lat)
    route = ox.shortest_path(G, start_node, end_node, weight="length")
    coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]

    # start backend route job
    try:
        route_id = g.sim.start_route_job(
            robot_id=robot_id,
            coords=coords,
            duration_s=duration_s,
            route_color=route_color,
        )
    except IndexError:
        return _bad_request("robot_id out of range. Create robot first.")
    except Exception as e:
        return jsonify({"error": f"Could not start route job: {e}"}), 500

    # return map that polls robot state
    web_map = Map(
        start=start.strip(),
        end=end.strip(),
        route_color=route_color,
        show_grey=show_grey,
        show_km=show_km,
        robot_id=robot_id,
    ).to_html()

    return jsonify(
        {
            "map": web_map,
            "start": start.strip(),
            "end": end.strip(),
            "route_color": route_color,
            "robot_id": robot_id,
            "route_id": route_id,
            "duration_s": duration_s,
        }
    ), 200


@MAP_API.route(f"{END_POINT}/lines", methods=["GET"])
def api_map_lines():
    return jsonify({"lines": list_lines()}), 200
