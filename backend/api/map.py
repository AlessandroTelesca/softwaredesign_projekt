"""
API for the map.
"""
from . import json_response
from flask import g, Blueprint, render_template_string
from backend.geography import Map

map_api = Blueprint("map", __name__)
endpoint = "/api/map"

@map_api.route(endpoint, methods=["GET"])
def api_map():
    """
    This creates an iframe of a map for the frontend.
    """
    web_map = Map(start="Karlsruhe Hauptbahnhof, Germany",
                  end="Karlsruhe Durlach Bahnhof, Germany").to_html()

    # TODO Dennisé: Add input possibilities to map routes
    return json_response({"map": web_map})