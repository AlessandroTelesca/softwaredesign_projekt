"""
The backend.
Provides API endpoints for the frontend to interact with the robot and map data.
Includes Flask app configuration and route definitions.
"""
from flask import Flask, json, render_template_string, request
from flask_cors import CORS

from robot import Robot, Movement, Location, StatusLED
from packages import Package, PackageSize
from simulation import Simulation
from geography import Map

#######################################################################################
# Backend Config                                                                      #
#######################################################################################
app: Flask = Flask(__name__)
CORS(app=app)
sim: Simulation = Simulation()


@app.route("/")
def map():
    """
    Fetches an interactive map of Karlsruhe's railways and displays it as an iframe.
    """
    web_map = Map(start="Karlsruhe Hauptbahnhof, Germany",
                  end="Karlsruhe Durlach Bahnhof, Germany").to_html()
    return render_template_string(web_map)


def json_response(payload: str) -> str:
    """
    Helper function to return a JSON response.
    """
    return json.dumps(payload)


########################################################################################
# Middleware                                                                           #
########################################################################################
# Debug
@app.route("/api/hello", methods=["GET"])
def api_hello():
    """
    Simple endpoint for frontend connectivity test.
    Returns: { "message": "Hello World" }
    """
    return json_response({"message": "Hello World"})


@app.route("/api/string/<text>", methods=["GET"])
def api_string(text):
    """
    Returns any string the frontend sends.
    Example: /api/string/test → { "received": "test" }
    """
    return json_response({"received": text})


# Map
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
@app.route("/api/robot/create", methods=["GET", "POST"])
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
    sim.robots.append(robot)

    return json_response({"robot_id": len(sim.robots) - 1, "status": kwargs, "robot_count": len(sim.robots)})


@app.route("/api/robot/read/<int:robot_id>", methods=["GET"])
def get_robot_status(robot_id: int):
    """
    Retrieves the status of a specific robot by its ID.
    """
    if len(sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot = sim.robots[robot_id]
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


@app.route("/api/robot/delete/<int:robot_id>", methods=["POST"])
def delete_robot(robot_id: int):
    """
    Deletes a robot by its ID.
    """
    if len(sim.robots) == 0:
        return json_response({"error": "No robots available"}), 404
    try:
        robot = sim.robots[robot_id]
    except IndexError:
        return json_response({"error": "Robot ID out of range"}), 404
    except TypeError:
        return json_response({"error": "Invalid Robot ID"}), 400

    sim.robots.remove(robot)
    return json_response({"message": f"Robot {robot_id} deleted successfully.", "robot_count": len(sim.robots)})


# Simulation
@app.route("/api/sim/reset", methods=["POST"])
def reset_simulation():
    """
    Resets the simulation to its initial state.
    """
    sim = Simulation()
    return json_response({"message": "Simulation reset successfully."})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
