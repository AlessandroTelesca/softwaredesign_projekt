"""
TODO: Docstring
"""
from flask import g, request
from werkzeug.exceptions import BadRequestKeyError
from backend.packages import PackageSize, Package
from . import json_response, PKG_API


END_POINT = "/api/pkg"


# Packages
@PKG_API.route(f"{END_POINT}/create", methods=["POST"])
def create_new_pkg():
    """
    Creates a small or large package and assigns it to a robot with a given ID. 
    Does not do anything if it exceeds max package size.
    """
    try:
        if g.sim.robots is None or len(g.sim.robots) == 0:
            return json_response({"error": "No robots available"}, 404)
        form = request.args
        robot_id = int(form.get("robot_id"))
        pkg_size = int(form.get("pkg_size"))
        pkg_size = PackageSize(pkg_size)
        start = form.get("start")
        destination = form.get("destination")
        if not destination or not start:
            return json_response({"error": "Missing start or destination point for package"}, 400)

        robot = g.sim.robots[robot_id]
    except BadRequestKeyError:
        return json_response({"error": "Missing required parameter for package creation"}, 400)
    except IndexError:
        return json_response({"error": "Robot ID out of range"}, 400)
    except (TypeError, ValueError):
        return json_response({"error": "Invalid Robot ID or package size."}, 400)

    pkg = Package(start=start, destination=destination, size=pkg_size)

    robot.add_package(pkg)
    g.sim.robots[robot_id] = robot
    return json_response({"message": f"{pkg_size} Package added to Robot {robot_id}.", "robot_count": len(g.sim.robots)}, 200)
