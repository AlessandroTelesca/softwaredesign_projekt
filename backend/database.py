"""
Control for the SQLite database.
"""

import sqlite3
from sqlite3 import Connection, Cursor


class SQL:
    """
    Handles all CRUD requests within the SQLite database.
    """
    file: str

    def __init__(self, file: str = "backend/data.db"):
        """
        TODO: Docstring
        """
        self.file = file
        con = sqlite3.connect(file)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS test(a, b, c)")

    def connection(self) -> tuple[Connection, Cursor]:
        """
        Establishes a connection with the SQLite database.
        Returns the connection as well as the query cursor.
        """
        con = sqlite3.connect(self.file)
        cur = con. cursor()
        return (con, cur)

    def create_tables(self):
        """
        Creates the data tables. Right now only creates a demo table.
        """
        con: tuple[Connection, Cursor] = self.connection()
        con[1].execute(
            "CREATE TABLE IF NOT EXISTS test(a, b, c)"
        )

