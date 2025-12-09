"""
The backend.
Provides API endpoints for the frontend to interact with the robot and map data.
Includes Flask app configuration and route definitions.
"""
from flask import Flask, json, render_template_string, request
from flask_cors import CORS

from robot import Robot, Movement, Location, Lights
from packages import Package, PackageSize

from geography import Map
import route_map

#######################################################################################
# Backend Config                                                                      #
#######################################################################################
app: Flask = Flask(__name__)
CORS(app=app)


@app.route("/")
def map():
    """
    Fetches an interactive map of Karlsruhe's railways and displays it as an iframe.
    """

    html: str = Map(start="Karlsruhe Hauptbahnhof, Germany", end="Karlsruhe Durlach Bahnhof, Germany", city="Karlsruhe").web_map().get_root()._repr_html_()
    return render_template_string(html)


def json_response(payload: str) -> str:
    """
    TODO: Docstring
    """
    return json.dumps(payload)


########################################################################################
# Middleware                                                                           #
########################################################################################
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


@app.route("/api/map", methods=["GET"])
def api_map():
    """
    This creates an iframe of a map for the frontend.
    """
    web_map = Map(start="Karlsruhe Hauptbahnhof, Germany", end="Karlsruhe Durlach Bahnhof, Germany", city="Karlsruhe").build_route_map().get_root()._repr_html_()
    
    #html: str = map.web_map
    # TODO: Add input to map routes
    #html: str = geography.web_map().get_root()._repr_html_()
    #html: str = route_map.build_route_map().get_root()._repr_html_()
    #start = "Karlsruhe Hauptbahnhof, Germany"
    #end = "Karlsruhe Durlach Bahnhof, Germany"
    #route_coords = route_animation.compute_route_coords(start, end)

    #html: str = route_animation.build_html(route_coords=route_coords).get_root()._repr_html_()
    return json_response({"map": web_map})


@app.route("/api/robot/create", methods=["GET"])
def create_new_robot():
    """
    TODO: Docstring
    """
    is_parked = request.args.get("is_parked")
    is_door_opened = request.args.get("is_door_opened")
    is_reversing = request.args.get("is_reversing")
    is_charging = request.args.get("is_charging")
    battery_status = request.args.get("battery_status")
    message = request.args.get("message")
    led_rgb = request.args.get("led_rgb")
    packages = []  # TODO: Parse packages from request

    robot: Robot = Robot(
        is_parked=is_parked,
        is_door_opened=is_door_opened,
        is_reversing=is_reversing,
        is_charging=is_charging,
        battery_status=battery_status,
        message=message,
        led_rgb=led_rgb,
        packages=packages,
    )

    string = "Robot created."
    string += f" is_parked={robot.is_parked}, is_door_opened={robot.is_door_opened}, "
    string += f"is_reversing={robot.is_reversing}, is_charging={robot.is_charging}, "
    string += f"battery_status={robot.battery_status}, message={robot.message}, "
    string += f"led_rgb={robot.led_rgb}, packages={robot.packages}"
    print(string)

    return json_response({"status": string})


# Start Flask server
app.run(host="127.0.0.1", port=5000, debug=True)
