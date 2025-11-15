"""
Control for the SQLite database.
"""

import sqlite3
import os
from sqlite3 import Connection, Cursor


class SQL:
    """
    Handles all CRUD requests within the SQLite database.
    """

    def __init__(self, file: str | None = None):
        """
        Initializes the SQLite database.
        Creates db/data.db next to this file if it does not exist yet.
        """
        # Basis-Verzeichnis dieser Datei (backend-Ordner)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # db-Unterordner innerhalb von backend
        db_dir = os.path.join(base_dir, "db")
        os.makedirs(db_dir, exist_ok=True)

        # Standardpfad: backend/db/data.db
        if file is None:
            file = os.path.join(db_dir, "data.db")

        self.file = file

        # DB-Datei anlegen und Testtabelle erstellen
        con = sqlite3.connect(self.file)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS test(a, b, c)")
        con.commit()
        con.close()

    def connection(self) -> tuple[Connection, Cursor]:
        """
        Establishes a connection with the SQLite database.
        Returns the connection as well as the query cursor.
        """
        con = sqlite3.connect(self.file)
        cur = con.cursor()
        return con, cur

    def create_tables(self):
        """
        Creates the data tables. Right now only creates a demo table.
        """
        con, cur = self.connection()
        cur.execute("CREATE TABLE IF NOT EXISTS test(a, b, c)")
        con.commit()
        con.close()