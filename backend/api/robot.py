"""
API for managing robots within the simulation.
"""
from flask import g, request
from backend.robot import Robot
from . import json_response, ROBOT_API


END_POINT = "/api/robot"


@ROBOT_API.route(f"{END_POINT}/create", methods=["POST"])
def create_new_robot():
    """
    Creates a new robot with parameters from the request arguments.
    """
    kwargs = {}
    params = {
        "is_parked": None,
        "is_door_opened": None,
        "is_reversing": None,
        "is_charging": None,
        "battery_status": None,
        "led_rgb": None
    }

    for key, _ in params.items():
        if request.args.get(key) is not None or request.args.get(key) != "":
            match key:
                case "is_parked" | "is_door_opened" | "is_reversing" | "is_charging":
                    kwargs[key] = request.args.get(key) == "true"
                case "battery_status":
                    kwargs[key] = request.args.get(key)
                case _:
                    kwargs[key] = request.args.get(key)
    robot: Robot = Robot(**kwargs)
    g.sim.robots.append(robot)

    return json_response({"robot_id": len(g.sim.robots) - 1, "status": robot.get_robot_status(),
                          "robot_count": len(g.sim.robots)})


@ROBOT_API.route(f"{END_POINT}/read", methods=["GET"])
def get_robot_status():
    """
    Retrieves the status of a specific robot by its ID.
    """
    if len(g.sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot_id: int = int(request.args["robot_id"])
        robot = g.sim.robots[robot_id]
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400

    status = {
        "status": robot.status,
        "battery_status": robot.battery_status,
        "led_rgb": robot.led_rgb,
        "packages": robot.packages,
    }
    return json_response({"robot_id": robot_id, "status": status})


@ROBOT_API.route("/api/robot/update/<int:robot_id>", methods=["POST"])
def update_robot_status(robot_id: int):
    """
    TODO: Docstring
    """
    if len(g.sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot: Robot = g.sim.robots[int(robot_id)]
        # TODO: Change robot
        

        g.sim.robots[robot_id] = robot
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400


@ROBOT_API.route("/api/robot/delete/<int:robot_id>", methods=["POST"])
def delete_robot(robot_id: int):
    """
    Deletes a robot by its ID.
    """
    if len(g.sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot = g.sim.robots[robot_id]
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400

    g.sim.robots.remove(robot)
    return json_response({"message": f"Robot {robot_id} deleted successfully.",
                          "robot_count": len(g.sim.robots)})
