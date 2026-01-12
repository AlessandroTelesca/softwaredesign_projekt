"""
API for basic debugging purposes.
"""
from flask import g, render_template
from . import json_response, DEBUG_API


@DEBUG_API.route("/")
def api_index():
    """
    Quick overview of the current Flask backend for debugging purposes.
    """
    return render_template("index.html", sim=g.sim)


@DEBUG_API.route("/api/hello", methods=["GET"])
def api_hello():
    """
    Simple endpoint for frontend connectivity test.
    Returns: { "message": "Hello World" }
    """
    return json_response({"message": "Hello World"})


@DEBUG_API.route("/api/string/<text>", methods=["GET"])
def api_string(text):
    """
    Returns any string the frontend sends.
    Example: /api/string/test → { "received": "test" }
    """
    return json_response({"received": text})

@DEBUG_API.route("/api/map", methods=["GET"])
def api_map():
    """
    TODO: Docstring
    """
    return render_template("map.html", map=map)
