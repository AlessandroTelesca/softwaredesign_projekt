"""
The backend.
Provides API endpoints for the frontend to interact with the robot and map data.
Includes Flask app configuration and route definitions.
"""
from flask import Flask, json, render_template_string, request, g
from flask_cors import CORS
from backend.api.debug import debug
from backend.api.robot import robot_crud

from backend.robot import Robot, Movement, Location, StatusLED
from backend.packages import PackageSize
from backend.simulation import Simulation
from backend.geography import Map

#######################################################################################
# Backend Config                                                                      #
#######################################################################################
app: Flask = Flask(__name__)
CORS(app=app)
sim: Simulation = Simulation()

@app.before_request
def inject_singleton():
    """
    This injects given variable to middleware before requests.
    """
    g.sim = sim


def json_response(payload: str) -> str:
    """
    Helper function to return a JSON response.
    """
    return json.dumps(payload)


########################################################################################
# Middleware                                                                           #
########################################################################################
# Debug

with app.app_context():
    app.register_blueprint(debug)
    app.register_blueprint(robot_crud)

# Map
# TODO: Refactor into own file
@app.route("/api/map", methods=["GET"])
def api_map():
    """
    This creates an iframe of a map for the frontend.
    """
    web_map = Map(start="Karlsruhe Hauptbahnhof, Germany",
                  end="Karlsruhe Durlach Bahnhof, Germany").to_html()

    # TODO Dennisé: Add input possibilities to map routes
    return json_response({"map": web_map})


# Robot

# @app.route("/api/robot/create", methods=["POST"])
# def create_new_robot():
#     """
#     Creates a new robot with parameters from the request arguments.
#     """
#     kwargs = {}
#     params = {
#         "is_parked": None,
#         "is_door_opened": None,
#         "is_reversing": None,
#         "is_charging": None,
#         "battery_status": None,
#         "message": None,
#         "led_rgb": None,
#         "packages": None,
#     }

#     for key, _ in params.items():
#         if request.args.get(key) is not None or request.args.get(key) != "":
#             match key:
#                 case "is_parked" | "is_door_opened" | "is_reversing" | "is_charging":
#                     kwargs[key] = request.args.get(key) == "true"
#                 case "battery_status":
#                     kwargs[key] = request.args.get(key)
#                 case "packages":
#                     kwargs[key] = []  # TODO: Parse packages from request
#                 case _:
#                     kwargs[key] = request.args.get(key)
#     robot: Robot = Robot(**kwargs)
#     sim.robots.append(robot)

#     return json_response({"robot_id": len(sim.robots) - 1, "status": robot.get_robot_status(), "robot_count": len(sim.robots)})


# @app.route("/api/robot/read/<int:robot_id>", methods=["GET"])
# def get_robot_status(robot_id: int):
#     """
#     Retrieves the status of a specific robot by its ID.
#     """
#     if len(sim.robots) == 0:
#         return json_response({"error": "No robots available"}), 404
#     try:
#         robot = sim.robots[robot_id]
#     except IndexError:
#         return json_response({"error": "Robot ID out of range"}), 404
#     except TypeError:
#         return json_response({"error": "Invalid Robot ID"}), 400

#     status = {
#         "is_parked": robot.is_parked,
#         "is_door_opened": robot.is_door_opened,
#         "is_reversing": robot.is_reversing,
#         "is_charging": robot.is_charging,
#         "battery_status": robot.battery_status,
#         "message": robot.message,
#         "led_rgb": robot.led_rgb,
#         "packages": robot.packages,
#     }
#     return json_response({"robot_id": robot_id, "status": status})


# @app.route("/api/robot/update/<int:robot_id>", methods=["POST"])
# def update_robot_status(robot_id: int):
#     """
#     TODO: Docstring
#     """
#     pass




# @app.route("/api/robot/delete/<int:robot_id>", methods=["POST"])
# def delete_robot(robot_id: int):
#     """
#     Deletes a robot by its ID.
#     """
#     if len(sim.robots) == 0:
#         return json_response({"error": "No robots available"}), 404
#     try:
#         robot = sim.robots[robot_id]
#     except IndexError:
#         return json_response({"error": "Robot ID out of range"}), 404
#     except TypeError:
#         return json_response({"error": "Invalid Robot ID"}), 400

#     sim.robots.remove(robot)
#     return json_response({"message": f"Robot {robot_id} deleted successfully.", "robot_count": len(sim.robots)})


# Packages
@app.route("/api/pkg/create", methods=["POST"])
def create_package(robot_id: int, pkg_size: PackageSize, start: str, destination: str):
    """
    Creates a small or large package and assigns it to a robot with a given ID. 
    Does not do anything if it exceeds max package size.
    """
    if len(sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot = sim.robots[robot_id]
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400
    robot.add_new_package(size=pkg_size, start=start, destination=destination)
    sim.robots[robot_id] = robot
    return json_response({"message": f"{pkg_size.name} Package added to Robot {robot_id}. {len(robot._packages)}", "robot_count": len(sim.robots)})


# Simulation
@app.route("/api/sim/reset", methods=["POST"])
def reset_simulation():
    """
    Resets the simulation to its initial state.
    """
    sim = Simulation()
    return json_response({"message": "Simulation reset successfully."})


@app.route("/api/sim/heartbeat", methods=["GET"])
def heartbeat():
    """
    TODO: Docstring.
    """
    pass


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
