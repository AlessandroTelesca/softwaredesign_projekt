"""
API for basic debugging purposes.
"""
from . import json_response
from flask import Blueprint, render_template_string
from backend.geography import Map

debug = Blueprint("debug", __name__)


@debug.route("/")
def map():
    """
    Fetches an interactive map of Karlsruhe's railways and displays it as an iframe.
    """
    web_map = Map(start="Karlsruhe Hauptbahnhof, Germany",
                  end="Karlsruhe Durlach Bahnhof, Germany").to_html()
    return render_template_string(web_map)


@debug.route("/api/hello", methods=["GET"])
def api_hello():
    """
    Simple endpoint for frontend connectivity test.
    Returns: { "message": "Hello World" }
    """
    return json_response({"message": "Hello World"})


@debug.route("/api/string/<text>", methods=["GET"])
def api_string(text):
    """
    Returns any string the frontend sends.
    Example: /api/string/test → { "received": "test" }
    """
    return json_response({"received": text})
