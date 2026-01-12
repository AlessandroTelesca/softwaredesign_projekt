"""
API for the simulation.
"""
from flask import g, request
from backend.simulation import Simulation
from . import json_response, SIM_API


END_POINT = "/api/sim"
  

@SIM_API.route(f"{END_POINT}/reset", methods=["POST"])
def reset_simulation():
    """
    Resets the simulation to its initial state.
    """
    g.sim.reset()
    return json_response({"message": "Simulation reset successfully."})

@SIM_API.route(f"{END_POINT}/set_time", methods=["POST"])
def set_time():
    hours = request.args.get("hours")
    minutes = request.args.get("minutes")
    seconds = request.args.get("seconds")

    if hours is None or minutes is None:
        return json_response({"error": "No hours or minutes specified."}, 400)
    if seconds is None:
        seconds = 0
    try:
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
    except TypeError:
        return json_response({"error": "No valid data type specified; must be integer."}, 400)
    if hours < 0 or minutes < 0 or seconds < 0 or hours > 24 or minutes > 60 or seconds > 60:
        return json_response({"error": "Invalid time selected."}, 400)
    
    return json_response({"message": "TODO"})


@SIM_API.route("/api/sim/heartbeat", methods=["GET"])
def heartbeat():
    """
    TODO: Docstring.
    """
