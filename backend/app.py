"""
Backend.
TODO: Docstring
"""

from flask import Flask, json, render_template_string
from flask_cors import CORS
from database import SQL
import geography

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
    html: str = geography.web_map().get_root()._repr_html_()
    return render_template_string(html)


def json_response(payload: str, status: int = 200) -> str:
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
    TODO: Docstring
    """
    html: str = geography.web_map().get_root()._repr_html_()
    return json_response({"map": html})


#######################################################################################
# SQLite Config                                                                       #
#######################################################################################
# TODO: Actual DB interactions
data = SQL()
con, cur = data.connection()

res = cur.execute("SELECT name FROM sqlite_master").fetchall()
print(res)

# NOTE: Uncomment if you don't want any tables
data.create_tables()

# Start Flask server
app.run(host="127.0.0.1", port=5000, debug=True)
