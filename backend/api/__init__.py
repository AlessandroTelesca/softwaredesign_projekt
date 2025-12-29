"""
Has the json response and Flask blueprints for all API modules.
"""
import json
from flask import Blueprint

DEBUG_API = Blueprint("debug", __name__)
MAP_API = Blueprint("map", __name__)
PKG_API = Blueprint("package", __name__)
ROBOT_API = Blueprint("robot", __name__)
SIM_API = Blueprint("sim", __name__)

def json_response(payload: str) -> str:
    """
    Helper function to return a JSON response for the middleware.
    """
    return json.dumps(payload)
