"""
API for the simulation.
"""
from flask import g
from backend.simulation import Simulation
from . import json_response, SIM_API


END_POINT = "/api/sim"


@SIM_API.route(f"{END_POINT}/reset", methods=["POST"])
def reset_simulation():
    """
    Resets the simulation to its initial state.
    """
    g.sim.robots = []
    return json_response({"message": "Simulation reset successfully."})


@SIM_API.route("/api/sim/heartbeat", methods=["GET"])
def heartbeat():
    """
    TODO: Docstring.
    """
