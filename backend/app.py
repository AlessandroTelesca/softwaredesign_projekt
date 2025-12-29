"""
The backend.
Provides API endpoints for the frontend to interact with the robot and map data.
Includes Flask app configuration and route definitions.
"""
from flask import Flask, Blueprint, json, g
from flask_cors import CORS

from backend.simulation import Simulation

from backend.api.debug import debug
from backend.api.robot import robot_crud
from backend.api.map import map_api
from backend.api.pkg import pkg_api
from backend.api.sim import sim_api


#######################################################################################
# Backend Config                                                                      #
#######################################################################################
app: Flask = Flask(__name__)
CORS(app=app)
sim: Simulation = Simulation()


@app.before_request
def inject_singleton():
    """
    This injects any given variable to middleware before requests.
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
middleware: list[Blueprint] = [debug, robot_crud, map_api, pkg_api, sim_api]
with app.app_context():
    # Creates the middleware for all applications.
    # Files are stored within api/*.py.
    for api in middleware:
        app.register_blueprint(api)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
