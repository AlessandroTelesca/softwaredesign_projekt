"""
API for managing robots within the simulation.
"""
from . import json_response
from flask import g, Blueprint, request
from backend.robot import Robot

robot_crud = Blueprint("robot_api", __name__)
endpoint = "/api/robot"


@robot_crud.route(f"{endpoint}/create", methods=["POST"])
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
        "message": None,
        "led_rgb": None,
        "packages": None,
    }

    for key, _ in params.items():
        if request.args.get(key) is not None or request.args.get(key) != "":
            match key:
                case "is_parked" | "is_door_opened" | "is_reversing" | "is_charging":
                    kwargs[key] = request.args.get(key) == "true"
                case "battery_status":
                    kwargs[key] = request.args.get(key)
                case "packages":
                    kwargs[key] = []  # TODO: Parse packages from request
                case _:
                    kwargs[key] = request.args.get(key)
    robot: Robot = Robot(**kwargs)
    g.sim.robots.append(robot)

    return json_response({"robot_id": len(g.sim.robots) - 1, "status": robot.get_robot_status(), "robot_count": len(g.sim.robots)})


@robot_crud.route(f"{endpoint}/read/<int:robot_id>", methods=["GET"])
def get_robot_status(robot_id: int):
    """
    Retrieves the status of a specific robot by its ID.
    """
    if len(g.sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot = g.sim.robots[robot_id]
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400

    status = {
        "is_parked": robot.is_parked,
        "is_door_opened": robot.is_door_opened,
        "is_reversing": robot.is_reversing,
        "is_charging": robot.is_charging,
        "battery_status": robot.battery_status,
        "message": robot.message,
        "led_rgb": robot.led_rgb,
        "packages": robot.packages,
    }
    return json_response({"robot_id": robot_id, "status": status})


@robot_crud.route("/api/robot/update/<int:robot_id>", methods=["POST"])
def update_robot_status(robot_id: int):
    """
    TODO: Docstring
    """
    pass


@robot_crud.route("/api/robot/delete/<int:robot_id>", methods=["POST"])
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
    return json_response({"message": f"Robot {robot_id} deleted successfully.", "robot_count": len(g.sim.robots)})
