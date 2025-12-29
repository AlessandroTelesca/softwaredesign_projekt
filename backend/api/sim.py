"""
API for the simulation.
"""
from . import json_response
from flask import g, Blueprint, render_template_string
from backend.simulation import Simulation

sim_api = Blueprint("sim", __name__)
endpoint = "/api/sim"

@sim_api.route(f"{endpoint}/reset", methods=["POST"])
def reset_simulation():
    """
    Resets the simulation to its initial state.
    """
    g.sim = Simulation()
    return json_response({"message": "Simulation reset successfully."})


@sim_api.route("/api/sim/heartbeat", methods=["GET"])
def heartbeat():
    """
    TODO: Docstring.
    """
    pass