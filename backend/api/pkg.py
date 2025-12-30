"""
TODO: Docstring
"""
from flask import g, request
from werkzeug.exceptions import BadRequestKeyError
from backend.packages import PackageSize
from . import json_response, PKG_API


END_POINT = "/api/pkg"


# Packages
@PKG_API.route(f"{END_POINT}/create", methods=["POST"])
def create_new_pkg():
    """
    Creates a small or large package and assigns it to a robot with a given ID. 
    Does not do anything if it exceeds max package size.
    """

    if len(g.sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        form = request.form
        robot_id = int(form["robot_id"])
        pkg_size = PackageSize(int(form["pkg_size"]))
        start = form["start"]
        destination = form["destination"]

        robot = g.sim.robots[robot_id]
    except BadRequestKeyError:
        return json_response({"error": "Missing required parameter for package creation"}), 400
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400
    robot.add_new_package(size=pkg_size, start=start, destination=destination)
    # g.sim.robots[robot_id] = robot
    return json_response({"message": f"{
        pkg_size.name} Package added to Robot {robot_id}. {len(robot._packages)}",
        "robot_count": len(g.sim.robots)})
