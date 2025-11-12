"""
Backend.
TODO: Docstring
"""

from flask import Flask, json, render_template_string
from flask_cors import CORS
import sqlite3
from database import SQL
import geography

#######################################################################################
# Backend Config                                                                      #
#######################################################################################
# TODO: Dennis: Add RESTful API for Angular frontend
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
    # TODO: Dennis: Generate API responses here
    return json.dumps(payload)


#######################################################################################
# SQLite Config                                                                       #
#######################################################################################
# TODO: Actual DB interactions
data = SQL()
con, cur = data.connection()

res = cur.execute("SELECT name FROM sqlite_master").fetchall()
print(res)
