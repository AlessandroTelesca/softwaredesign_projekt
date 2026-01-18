"""
API for managing robots within the simulation.
"""

from __future__ import annotations

from flask import g, request

from backend.robot import Robot
from . import json_response, ROBOT_API

END_POINT = "/api/robot"


@ROBOT_API.route(f"{END_POINT}/create", methods=["POST"])
def create_new_robot():
    """
    Creates a new robot.
    Params can be provided via query string (simple approach).
    """
    robot_id = len(g.sim.robots)

    # defaults
    kwargs = {
        "robot_id": robot_id,
        "is_parked": True,
        "is_door_opened": False,
        "is_reversing": False,
        "is_charging": False,
        "battery_status": 100.0,
        "led_rgb": (0, 255, 0),
    }

    # optional overrides
    for key in ("is_parked", "is_door_opened", "is_reversing", "is_charging"):
        v = request.args.get(key)
        if v is not None and v != "":
            kwargs[key] = (v.lower() == "true")

    v = request.args.get("battery_status")
    if v is not None and v != "":
        try:
            kwargs["battery_status"] = float(v)
        except Exception:
            pass

    # led_rgb as "r,g,b"
    v = request.args.get("led_rgb")
    if v is not None and v != "":
        try:
            parts = [int(x.strip()) for x in v.split(",")]
            if len(parts) == 3:
                kwargs["led_rgb"] = (parts[0], parts[1], parts[2])
        except Exception:
            pass

    robot: Robot = Robot(**kwargs)
    g.sim.robots.append(robot)

    return json_response(
        {
            "robot_id": robot_id,
            "status": robot.to_dict(),
            "robot_count": len(g.sim.robots),
        }
    )


@ROBOT_API.route(f"{END_POINT}/read", methods=["GET"])
def get_robot_status():
    """
    Read robot state + message log.

    Query:
      - robot_id: required int
      - since_message_id: optional int (only return newer messages)
    """
    if len(g.sim.robots) == 0:
        return json_response({"error": "No robots available"}, 404)

    # robot_id
    try:
        robot_id: int = int(request.args["robot_id"])
        robot: Robot = g.sim.robots[robot_id]
    except KeyError:
        return json_response({"error": "Missing robot_id"}, 400)
    except IndexError:
        return json_response({"error": "Robot ID out of range"}, 404)
    except Exception:
        return json_response({"error": "Invalid robot_id"}, 400)

    # since_message_id (optional)
    since = request.args.get("since_message_id")
    since_id = 0
    if since is not None and since != "":
        try:
            since_id = int(since)
        except Exception:
            since_id = 0

    last_id, msgs = robot.get_messages_since(since_id)

    return json_response(
        {
            "robot_id": robot_id,
            "status": robot.to_dict(),
            "last_message_id": last_id,
            "messages": msgs,
        }
    )
