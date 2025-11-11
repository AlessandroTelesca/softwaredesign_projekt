"""
Backend.
TODO: Docstring
"""

from flask import Flask, json
from flask_cors import CORS
import sqlite3

#######################################################################################
# Backend Config                                                                      #
#######################################################################################
# TODO: Add RESTful API for Angular frontend
app: Flask = Flask(__name__)
CORS(app=app)


@app.route("/test")
def test():
    """
    TODO: Docstring
    """
    pass


def json_response(payload: str, status: int = 200) -> str:
    """
    TODO: Docstring
    """
    return json.dumps(payload)


#######################################################################################
# SQLite Config                                                                       #
#######################################################################################
# TODO: Actual DB interactions
con = sqlite3.connect("backend/data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS test(a, b, c)")

res = cur.execute("SELECT name FROM sqlite_master").fetchall()
print(res)
