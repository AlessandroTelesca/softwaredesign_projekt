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
    return json_response({"message": "Simulation reset successfully."}, 200)


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


@SIM_API.route(f"{END_POINT}/set_seconds_per_tick", methods=["POST"])
def set_seconds_per_tick():
    param = request.form["seconds_per_tick"]
    try:
        param = int(param)
        if param < 1:
            return json_response({"error": "Invalid time selected; must be >= 1."}, 400)
        g.sim.seconds_per_tick = param
        return json_response({"message": f"Changed simulation seconds per tick to {param} seconds."}, 200)
    except TypeError:
        return json_response({"error": "No valid data type specified; must be integer."}, 400)


@SIM_API.route(f"{END_POINT}/heartbeat", methods=["GET"])
def heartbeat():
    """
    Returns the current ticks, date, and time.
    """
    return json_response({"ticks": g.sim.ticks, "date": g.sim.date, "time": g.sim.time}, 200)
