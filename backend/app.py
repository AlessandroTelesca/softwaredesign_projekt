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


@app.route("/test")
def test():
    """
    TODO: Docstring
    """
    return render_template_string(geography.web_map().get_root()._repr_html_())


def json_response(payload: str, status: int = 200) -> str:
    """
    TODO: Docstring
    """
    return json.dumps(payload)


#######################################################################################
# SQLite Config                                                                       #
#######################################################################################
# TODO: Actual DB interactions
data = SQL()
con = sqlite3.connect("backend/data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS test(a, b, c)")

res = cur.execute("SELECT name FROM sqlite_master").fetchall()
print(res)
