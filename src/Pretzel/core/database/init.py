import os
import sqlite3


def initialize_databases():
    # The data database
    if not os.path.exists("data/databases/data.db"):
        with open("data/databases/data.db", mode="x"):
            conn = sqlite3.connect("data/databases/data.db")
            c = conn.cursor()
            c.execute("CREATE TABLE items (name text, chemical_formula text, warning_label text, danger_level text, notes text, pictograms text)")
            c.execute("CREATE TABLE stock (name text, quantity real, unit text, cost real)")
            conn.commit()
            conn.close()

    return
