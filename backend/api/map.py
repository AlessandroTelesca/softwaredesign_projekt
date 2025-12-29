"""
API for the map.
"""
from backend.geography import Map
from . import json_response, MAP_API

END_POINT = "/api/map"


@MAP_API.route(END_POINT, methods=["GET"])
def api_map():
    """
    This creates an iframe of a map for the frontend.
    """
    web_map = Map(start="Karlsruhe Hauptbahnhof, Germany",
                  end="Karlsruhe Durlach Bahnhof, Germany").to_html()

    # TODO Dennisé: Add input possibilities to map routes
    return json_response({"map": web_map})
