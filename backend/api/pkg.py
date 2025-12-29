"""
TODO: Docstring
"""
from . import json_response
from flask import g, Blueprint, render_template_string
from backend.packages import PackageSize

pkg_api = Blueprint("package", __name__)
endpoint = "/api/pkg"


# Packages
@pkg_api.route("/api/pkg/create", methods=["POST"])
def create_package(robot_id: int, pkg_size: PackageSize, start: str, destination: str):
    """
    Creates a small or large package and assigns it to a robot with a given ID. 
    Does not do anything if it exceeds max package size.
    """
    if len(g.sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot = g.sim.robots[robot_id]
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400
    robot.add_new_package(size=pkg_size, start=start, destination=destination)
    g.sim.robots[robot_id] = robot
    return json_response({"message": f"{pkg_size.name} Package added to Robot {robot_id}. {len(robot._packages)}", "robot_count": len(g.sim.robots)})
