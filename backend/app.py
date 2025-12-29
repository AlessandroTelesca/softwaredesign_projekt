"""
The backend.
Provides API endpoints for the frontend to interact with the robot and map data.
Includes Flask app configuration and route definitions.
"""
from flask import Flask, Blueprint, g
from flask_cors import CORS

from backend.simulation import Simulation

from backend.api.debug import DEBUG_API
from backend.api.robot import ROBOT_API
from backend.api.map import MAP_API
from backend.api.pkg import PKG_API
from backend.api.sim import SIM_API


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


########################################################################################
# Middleware                                                                           #
########################################################################################
middleware: list[Blueprint] = [DEBUG_API, ROBOT_API, MAP_API, PKG_API, SIM_API]
with app.app_context():
    # Creates the middleware for all applications.
    # Files are stored within api/*.py.
    for api in middleware:
        app.register_blueprint(api)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
