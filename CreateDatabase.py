import sqlite3

# runs the sql commands that are passed in
def runsql(*args):
    conn = sqlite3.connect("clicks.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    if len(args) == 1:
        cursor.execute(args[0])
    else:
        cursor.execute(args[0], args[1])
    conn.commit()
    return cursor.fetchall()

# runs the sql command to create the table in the database
def createDatabase():

    sqlstring = """
    CREATE TABLE IF NOT EXISTS tblhomeclicks (
    xCoord INTEGER,
    yCoord INTEGER,
    count INTEGER,
    PRIMARY KEY (xCoord, yCoord)
    )
    """
    runsql(sqlstring)

# This file only needs to be run once to create the database
createDatabase()
